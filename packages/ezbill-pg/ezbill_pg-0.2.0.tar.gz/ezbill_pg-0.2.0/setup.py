from setuptools import setup, find_packages

setup(
    name="your-package-name",           # Must be unique on PyPI
    version="0.1.0",
    author="Your Name",
    author_email="your@email.com",
    description="A simple hello package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
