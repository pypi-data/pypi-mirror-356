#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "ggbound",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ["pip", "gnn"],			# 关键字
    description = "a PyTorch-based GNN library",	# 描述
    long_description= "ggbound is a PyTorch-based GNN library, named for the idea that 'a Graph is all about nodes and how they're bound together'",
    license = "MIT Licence",		# 许可证

    url = "https://github.com/yangfa-zhang/ggbound",     #项目相关文件地址，一般是github项目地址即可
    author = "yangfa-zhang",			# 作者
    author_email = "yangfa1027@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["torch"]          #这个项目依赖的第三方库
)
