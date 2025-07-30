from setuptools import setup, find_packages

setup(
    name="image-enhancer-viv",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch==1.11.0",
        "torchvision==0.12.0",
        "opencv-python",
        "Pillow",
        "numpy",
        "basicsr",
        "realesrgan",
        "gfpgan",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "image-enhancer=image_enhancer.main:main"
        ]
    },
)
