from setuptools import setup, find_packages

setup(
    name="pyksh_oyb",
    version="0.1.0",
    description="将多个Python脚本文件内容以对象属性方式集中管理，便于查看和引用",
    author="sakimi",
    author_email="w9293846@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    url="",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
