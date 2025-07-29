import numpy as np
import torch
import torch.nn as nn
from torch.optim import LBFGS
import torch.nn.functional as F
import cv2

def transfer_colors(source, target, alpha=0.3):
    source_lab = cv2.cvtColor(source, cv2.COLOR_RGB2LAB).astype(np.float32)
    target_lab = cv2.cvtColor(target, cv2.COLOR_RGB2LAB).astype(np.float32)

    for i in range(3):  # L, A, B
        mean_src = source_lab[:, :, i].mean()
        std_src = source_lab[:, :, i].std()
        mean_tgt = target_lab[:, :, i].mean()
        std_tgt = target_lab[:, :, i].std()

        target_normalized = (target_lab[:, :, i] - mean_tgt) / (std_tgt + 1e-6)
        target_aligned = target_normalized * std_src + mean_src

        target_lab[:, :, i] = target_lab[:, :, i] * (1 - alpha) + np.clip(target_aligned, 0, 255) * alpha
    
    result = cv2.cvtColor(target_lab.astype(np.uint8), cv2.COLOR_LAB2RGB)
    
    return result

class ContentLoss(nn.Module):
    def __init__(self):
        super(ContentLoss, self).__init__()
        self.target = None
        self.target_mul = 1

    def forward(self, input):
        if self.target is not None:
            self.loss = F.mse_loss(input, self.target * self.target_mul)
        return input
    
    def set_target_feature(self, target_feature):
        self.target = target_feature.detach()
    
    def reset_target(self):
        self.target = None
        
    def set_target_mul(self, mul: float):
        self.target_mul = mul

class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = self.gram_matrix(target_feature).detach()
        self.target_mul = 1

    def forward(self, input):
        G = self.gram_matrix(input)
        self.loss = F.mse_loss(G, self.target * self.target_mul)

        return input
    
    def set_target_mul(self, mul: float):
        self.target_mul = mul

    @staticmethod
    def gram_matrix(input):
        a, b, c, d = input.size()
        features = input.view(a * b, c * d)  # Flatten the feature map
        G = torch.mm(features, features.t())  # Compute Gram matrix
        return G.div((a * b * c * d) ** 0.5)  # Normalize the Gram matrix
    
class Normalization(nn.Module):
    def __init__(self, mean, std):
        super(Normalization, self).__init__()
        self.mean = mean.clone().detach().view(-1, 1, 1)
        self.std = std.clone().detach().view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std  # Normalize the image

class NST_VGG19:
    """
    Neural Style Transfer using VGG19.
    :param style_image: Numpy array (H, W, C) or tensor of the style image.
    :param style_layers_weights: Dictionary of weights for style losses.
    """
    def __init__(self, 
        style_image: np.ndarray | torch.Tensor, 
        style_layers=['conv_2', 'conv_4', 'conv_6', 'conv_7', 'conv_9'], 
        content_layers=['conv_3', 'conv_6', 'conv_7'],
        gaussian_kernel_size = 3,
        gaussian_force=1.0
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if isinstance(style_image, np.ndarray):
            style_image_tensor = self.image_to_tensor(style_image)
        elif isinstance(style_image, torch.Tensor):
            style_image_tensor = style_image.clone().detach().to(self.device)
        else:
            raise TypeError("Input must be a numpy array or torch tensor.")
            
        self.style_image = style_image

        self.model, self.style_losses, self.content_losses = self.build_model(
            self.device,
            style_image_tensor,
            style_layers,
            content_layers
        )
        self.model.eval()
        
        # create gaussian kernel
        ax = torch.linspace(-(gaussian_kernel_size // 2), gaussian_kernel_size // 2, gaussian_kernel_size)
        xx, yy = torch.meshgrid(ax, ax, indexing='ij')
        kernel = torch.exp(-(xx**2 + yy**2) / (2 * gaussian_force**2))
        kernel /= kernel.sum()  # norm
        kernel = kernel.unsqueeze(0).unsqueeze(0)  # batches
        self.gaussian_kernel = kernel.to(self.device)
        self.gaussian_kernel_size = gaussian_kernel_size

    def image_to_tensor(self, numpy_image):
        image_tensor = torch.from_numpy(numpy_image).permute(2, 0, 1).float().div(255) # Convert (H, W, C) to (C, H, W)
        return image_tensor.unsqueeze(0).to(self.device).contiguous()

    def tensor_to_image(self, tensor):
        img = tensor.squeeze(0).permute(1, 2, 0).clip(0, 1).mul(255).cpu().detach().numpy().astype("uint8")
        return img

    @staticmethod
    def build_model(device, style_image_tensor, style_layers, content_layers):
        # torchvision's vgg19 trained on ImageNet dataset that uses normalized images, so we need to normalize too
        normalization_mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
        normalization_std = torch.tensor([0.229, 0.224, 0.225]).to(device)

        from torchvision.models import vgg19
        base_net = vgg19(weights='DEFAULT').features.to(device)
        model = nn.Sequential()
        model.add_module('normalization', Normalization(normalization_mean, normalization_std).to(device))

        style_losses = []
        content_losses = []
        i = 0

        for layer in base_net.children():
            if isinstance(layer, nn.Conv2d):
                i += 1
                name = f'conv_{i}'
            elif isinstance(layer, nn.ReLU):
                name = f'relu_{i}'
                layer = nn.ReLU(inplace=False)
            elif isinstance(layer, nn.MaxPool2d):
                name = f'pool_{i}'
            elif isinstance(layer, nn.BatchNorm2d):
                name = f'bn_{i}'
            else:
                raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

            model.add_module(name, layer)

            # Model does N layers then calc loss for N layers, then does other M layers and calc loss to N+M layers...

            if name in style_layers:
                target_feature = model(style_image_tensor).detach()
                style_loss = StyleLoss(target_feature)
                model.add_module(f"style_loss_{i}", style_loss)
                style_losses.append(style_loss)
            
            if name in content_layers:
                target_feature = model(style_image_tensor).detach()
                content_loss = ContentLoss()
                model.add_module(f"content_loss_{i}", content_loss)
                content_losses.append(content_loss)

        for i in range(len(model) - 1, -1, -1):
            if isinstance(model[i], (StyleLoss, ContentLoss)):
                break

        model = model[:(i + 1)]

        return model, style_losses, content_losses

    def set_content_losses(self, content_image_tensor, mul: float):
        target = content_image_tensor.clone().detach()

        for module in self.model:
            if isinstance(module, ContentLoss):
                module.reset_target()
            target = module(target).detach()
            if isinstance(module, ContentLoss):
                module.set_target_feature(target)
                module.set_target_mul(mul)
    
    def set_style_target_muls(self, mul: float):
        for module in self.model:
            if isinstance(module, StyleLoss):
                module.set_target_mul(mul)
    
    def gaussian_blur(self, img):
        batch_size, channels, height, width = img.shape
        blurred = F.conv2d(
            img.view(batch_size * channels, 1, height, width), 
            self.gaussian_kernel, 
            padding=self.gaussian_kernel_size // 2
        )
        blurred = blurred.view(batch_size, channels, height, width)

        return blurred
    
    @staticmethod
    def describe_noise_level(noise_val):
        levels = ['8==3', 'trsh', 'bad', 'poor', 'fair', 'good', 'best']
        thresholds = [1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 0]
        for i, threshold in enumerate(thresholds):
            if noise_val >= threshold:
                return levels[i]
    
    def __call__(
            self, 
            content_image: np.ndarray | torch.Tensor,
            num_steps=100,
            weight=1e-6,
            content_weight = 1e-3,
            output_type="np",
            label=None
        ):
        if isinstance(content_image, np.ndarray):
            content_image = cv2.medianBlur(content_image, 3)
            content_image = transfer_colors(self.style_image, content_image)
            input_img = self.image_to_tensor(content_image)
        elif isinstance(content_image, torch.Tensor):
            input_img = content_image.clone().detach().to(self.device)
        else:
            raise TypeError("Input must be a numpy array or torch tensor.")

        k = 4 / ((num_steps + 20) ** 0.2)
        smooth = k * 5
        fix = 28 / (num_steps ** 1.2) * 100
        
        self.set_content_losses(input_img, k)
        self.set_style_target_muls(k)
        
        optimizer = LBFGS([input_img.requires_grad_()], max_iter=num_steps)

        if label is not None:
            from tqdm import tqdm
            progress_bar = tqdm(total=num_steps, desc=label)
        
        def transfer():
            optimizer.zero_grad(set_to_none=True)

            self.model(input_img)

            total_loss = torch.tensor(0.0, device=self.device)
            
            for i, sl in enumerate(self.style_losses):
                loss = sl.loss * weight
                total_loss += loss
            
            for i, cl in enumerate(self.content_losses):
                loss = cl.loss * content_weight
                total_loss += loss
            
            noise_penalty = (torch.relu(-input_img).mean() + torch.relu(input_img - 1).mean())
            total_loss += noise_penalty * fix
            
            blurred = self.gaussian_blur(input_img)
            diff = torch.abs(blurred - input_img)
            diff_max = diff.max(dim=1, keepdim=True)[0]
            M = 1.2
            gaussian_loss = (diff_max * M) ** 2 # если умножить на M, то фильтр (0..1)**N уменьшит 1/M разниц и увеличит (M-1)/M разниц
            gaussian_loss = gaussian_loss.mean()
            total_loss += gaussian_loss * smooth / (M**2)
            
            if progress_bar is not None:
                progress_bar.set_postfix(q=self.describe_noise_level(noise_penalty.item()))
                progress_bar.update()

            total_loss.backward()
            return total_loss

        try:
            optimizer.step(transfer)
        except torch.OutOfMemoryError as e:
            print('torch.OutOfMemoryError')
            
        if output_type == 'np':
            return self.tensor_to_image(input_img)
        else:
            return input_img.detach()

def calc_rgba(rgb_white_bg_numpy, rgb_black_bg_numpy, a_orig):
    """
    Вычисляет RGBA изображение (с альфа-каналом) на основе спрайта на белом и черном фонах.

    :param rgb_white_bg_numpy: numpy массив изображения спрайта на белом фоне (RGB).
    :param rgb_black_bg_numpy: numpy массив изображения спрайта на черном фоне (RGB).
    :return: numpy массив RGBA изображения (4 канала).
    """
    
    white = rgb_white_bg_numpy.astype(np.float32) / 255.0
    black = rgb_black_bg_numpy.astype(np.float32) / 255.0

    if white.shape != black.shape:
        raise ValueError("Изображения должны иметь одинаковые размеры!")

    alpha_r = 1 - (white[:, :, 0] - black[:, :, 0])
    alpha_g = 1 - (white[:, :, 1] - black[:, :, 1])
    alpha_b = 1 - (white[:, :, 2] - black[:, :, 2])

    alpha = (alpha_r + alpha_g + alpha_b) / 3.0
    alpha = np.clip(alpha, 0, 1)

    a_orig = a_orig.astype(np.float32) / 255
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    a_orig = cv2.dilate(a_orig, kernel, iterations=2)
    
    alpha *= a_orig * a_orig
    xjesu_denoiser = lambda x, p: 1 - (1 - x) / ( x**p + (1 - x)**p )**(1/p)
    alpha = xjesu_denoiser(alpha, 4)

    sprite_r = np.zeros_like(black[:, :, 0])
    sprite_g = np.zeros_like(black[:, :, 1])
    sprite_b = np.zeros_like(black[:, :, 2])

    non_zero_alpha = alpha > 0
    sprite_r[non_zero_alpha] = black[:, :, 0][non_zero_alpha] / alpha[non_zero_alpha]
    sprite_g[non_zero_alpha] = black[:, :, 1][non_zero_alpha] / alpha[non_zero_alpha]
    sprite_b[non_zero_alpha] = black[:, :, 2][non_zero_alpha] / alpha[non_zero_alpha]

    sprite_r = np.clip(sprite_r, 0, 1)
    sprite_g = np.clip(sprite_g, 0, 1)
    sprite_b = np.clip(sprite_b, 0, 1)

    rgba = np.zeros((*alpha.shape, 4), dtype=np.float32)
    rgba[:, :, 0] = sprite_r
    rgba[:, :, 1] = sprite_g
    rgba[:, :, 2] = sprite_b
    rgba[:, :, 3] = alpha

    rgba = (rgba * 255).astype(np.uint8)

    return rgba
    
def apply_bg(rgba, background_color=(255, 255, 255)):
    r, g, b, a = cv2.split(rgba)
    aa = a.astype(np.float32) / 255
    r = ((r.astype(np.float32) * aa) + background_color[0] * (1 - aa)).astype(np.uint8)
    g = ((g.astype(np.float32) * aa) + background_color[1] * (1 - aa)).astype(np.uint8)
    b = ((b.astype(np.float32) * aa) + background_color[2] * (1 - aa)).astype(np.uint8)
    return cv2.merge((r, g, b))

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Neural style transfer.")
    parser.add_argument("image", help="Content image.")
    parser.add_argument("-s", "--style", required=True, help="Style image.")
    parser.add_argument("-n", "--num_steps", default=100, type=int, help="More steps - more deep transfer.")
    parser.add_argument("-o", "--output", default="nst_result.png", help="Output image name.")
    args = parser.parse_args()
    
    style_image = cv2.imread(args.style)
    if style_image is None:
        print('wrong style path')
        exit()
    style_image = cv2.cvtColor(style_image, cv2.COLOR_BGR2RGB)
    nst = NST_VGG19(style_image)

    init_image = cv2.imread(args.image, cv2.IMREAD_UNCHANGED)
    if init_image is None:
        print('wrong image path')
        exit()
    
    if init_image.shape[2] == 4:
        init_image = cv2.cvtColor(init_image, cv2.COLOR_BGRA2RGBA)
        _, _, _, a = cv2.split(init_image)
        
        black = apply_bg(init_image, (0,0,0))
        result_black = nst(black, num_steps=int(args.num_steps), label=args.image + ' (black)')
        
        white = apply_bg(init_image, (255,255,255))
        result_white = nst(white, num_steps=int(args.num_steps), label=args.image + ' (white)')
        
        result = calc_rgba(result_white, result_black, a)
        cv2.imwrite(args.output, cv2.cvtColor(result, cv2.COLOR_RGBA2BGRA))
    else:
        init_image = cv2.cvtColor(init_image, cv2.COLOR_BGR2RGB)
        result = nst(init_image, num_steps=int(args.num_steps), label=args.image)
        cv2.imwrite(args.output, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))
    
if __name__ == "__main__":
    main()
    
