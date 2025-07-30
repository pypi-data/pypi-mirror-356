from setuptools import setup, find_packages

setup(
    name="muse_lang",  # 包名称，pip install时使用的名字
    version="0.3",      # 版本号
    description="Mini language for data analysis of asset management.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Brooks Lu",
    author_email="lxc@jixunet.com",
    url="https://e.coding.net/brookslu/muse/muse.git",
    install_requires=[   # 依赖的其他包
        "numpy==2.3.0",
        "pandas==2.3.0",
        "polars==1.31.0"
    ],
    python_requires=">=3.12",  # Python版本要求
    classifiers=[       # 分类信息，可选
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)