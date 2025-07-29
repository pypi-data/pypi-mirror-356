from setuptools import setup, find_packages

# Read README file safely
try:
    with open('README.MD', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A simple calculator package"

setup(
    name='calc_azad',
    version='0.1.2',
    author='Azad',
    description='A simple calculator package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        
    ],
    license="MIT",  # Fixed: use 'license' instead of 'licence'
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)