from setuptools import setup, find_packages
import os

# Read README.md for long description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sreeclassifier",
    version="1.0.0",
    description="Image classification using Vision Transformer (ViT)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Manchala Sreekanth",
    author_email="manchalasreekanth999@gmail.com",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "Pillow>=9.0.0"
    ],
    include_package_data=True,
    package_data={"sreeclassifier": ["imagenet_classes.txt"]},
    python_requires='>=3.7',
)
