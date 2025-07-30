# from setuptools import setup, find_packages

# setup(
#     name="image-enhancer-viv",
#     version="0.1.0",
#     packages=find_packages(),
#     include_package_data=True,
#     install_requires=[
#         "torch==1.11.0",
#         "torchvision==0.12.0",
#         "opencv-python",
#         "Pillow",
#         "numpy",
#         "basicsr",
#         "realesrgan",
#         "gfpgan",
#     ],
#     python_requires=">=3.7",
#     entry_points={
#         "console_scripts": [
#             "image-enhancer=image_enhancer.main:main"
#         ]
#     },
# )
from setuptools import setup, find_packages
import os 
setup(
    name="image-enhancer-viv",  # Must match your PyPI name
    version="0.1.1",            # Bump version if reuploading
    packages=find_packages(),   # Automatically finds `image_enhancer/`
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
    description="A tool to enhance and restore facial images using Real-ESRGAN and GFPGAN",
    long_description=open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/image-enhancer-viv",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
