# NST_VGG19

Neural Style Transfer using VGG19.

![collage](https://github.com/user-attachments/assets/a1e2f364-d250-47b3-b10d-746731d16dbb)

Original paper [link](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf).

VGG19 weights from `torchvision`.

## Installation

```bash
pip install nst_vgg19
```

## Usage

`nst photo.jpg --style style-image.png --output result.png`

## Usage in python

```python
from nst_vgg19 import NST_VGG19

# images must be Numpy arrays. Use np.array(pil_image)

style_image = load_image('style.png')
content_image_1 = load_image('img1.jpg')
content_image_2 = load_image('img2.png')

nst = NST_VGG19(style_image)

result_1 = nst(content_image_1)
result_2 = nst(content_image_2)
```
