import os
from setuptools import setup, find_packages
from NewThread import __version__  # 确保版本一致性
#  @classmethod



setup(
    name="NewThread",
    version=__version__,
    author="孙亮",
    author_email="3028772928@qq.com",
    description="threading.Thread类的继承和拓展",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    # classifiers=[
    #     "Programming Language :: Python :: 3",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    # ],
    package_data={},
    python_requires=">=3.6",
    install_requires=[
    ],
)

