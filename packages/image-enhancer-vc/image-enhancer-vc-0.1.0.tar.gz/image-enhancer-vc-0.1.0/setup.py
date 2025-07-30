from setuptools import setup, find_packages

setup(
    name="image-enhancer-vc",
    version="0.1.0",
    author="Ahalya",
    author_email="innamuriahalya1234@gmail.com",
    description="A deep learning-powered image enhancement library using Real-ESRGAN and GPFGAN",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "torch==1.11.0",
        "opencv-python>=4.5.0",
        "torchvision==0.12.0",
        "numpy>=1.19.0,<2.0",
        "Pillow>=9.0.0",
        "basicsr>=1.4.2",
        "realesrgan>=0.3.0",
        "gfpgan>=1.3.8",
        "urllib3<2.0",
    ],
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]

)