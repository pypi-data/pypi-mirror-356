from setuptools import setup, find_packages

setup(
    name="sreeclassifier",
    version="0.1.0",
    description="Image classification using Vision Transformer (ViT)",
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
