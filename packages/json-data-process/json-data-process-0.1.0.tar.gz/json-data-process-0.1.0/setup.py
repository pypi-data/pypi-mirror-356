from setuptools import setup, find_packages

setup(
    name='json-data-process',  # 模块名称
    version='0.1.0',      # 版本号
    packages=find_packages(),  # 包含的Python包
    python_requires='>=3.9',  # 支持的Python版本
    install_requires=[],  # 依赖的外部库
    author='wangcheng',  # 作者信息
    author_email='154443603@qq.com',
    description='去除首尾的空格，浮点数保留n位小数',  # 简短描述
    classifiers=[  # 项目分类标签
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)