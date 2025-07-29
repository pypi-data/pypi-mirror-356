from setuptools import setup, find_packages

setup(
    name="DoerGPIO",
    version="0.2",  # Incremented version number
    packages=find_packages(),
    install_requires=[
        "pyserial",  # Required for serial communication
    ],
    author="Pasco Tang",
    author_email="jacobhere@gmail.com",  # You should add your email here
    description="USB GPIO interface for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # You should add your repository URL here
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9",
) 