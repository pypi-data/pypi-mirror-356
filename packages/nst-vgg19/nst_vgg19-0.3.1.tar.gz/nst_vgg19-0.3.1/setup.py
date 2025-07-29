from setuptools import setup

setup(
    name="nst_vgg19",
    version="0.3.1",
    author="Alexander Brodko",
    author_email="xjesus666@yandex.ru",
    description="Neural Style Transfer using VGG19",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alexanderbrodko/nst_vgg19",
    py_modules=["nst_vgg19"],
    install_requires=[
        "numpy",
        "torch>=1.13",
        "torchvision>=0.14",
        "opencv-python",
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "nst=nst_vgg19:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
