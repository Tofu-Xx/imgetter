#!/bin/bash
# Gitee 仓库设置脚本
# 用法: 在 Gitee 上手动创建仓库后，运行此脚本

# 1. 在 https://gitee.com/projects/new 创建仓库名 "imgetter"
# 2. 然后运行:

git remote add gitee git@gitee.com:tofu-xx/imgetter.git
git push gitee main

echo "Gitee 仓库同步完成！"
