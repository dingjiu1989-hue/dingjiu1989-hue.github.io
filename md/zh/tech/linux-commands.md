---
title: "Linux 命令行入门：30 个最常用的命令"
description: "Linux 新手必学的 30 个命令，从文件操作、权限管理到进程查看，每个带示例，收藏这一篇就够了。"
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/tech/linux-commands.html
---

# Linux 命令行入门：30 个最常用的命令

不管你做不做运维，Linux 命令行都是程序员的必修课。这 30 个命令覆盖 80% 日常场景。

## 文件操作（10 个）

命令| 用途| 示例  
---|---|---  
ls| 列出目录| `ls -la`  
cd| 切换目录| `cd /var/log`  
pwd| 显示当前路径| `pwd`  
mkdir| 创建目录| `mkdir -p a/b/c`  
cp| 复制文件| `cp -r src dst`  
mv| 移动/重命名| `mv old.txt new.txt`  
rm| 删除| `rm -rf dir/`  
cat| 查看文件内容| `cat file.txt`  
head/tail| 查看头/尾行| `tail -f log.txt`  
find| 搜索文件| `find . -name "*.py"`  
  
## 文本处理（6 个）

命令| 用途| 示例  
---|---|---  
grep| 文本搜索| `grep "error" log.txt`  
wc| 统计行/字数| `wc -l file.txt`  
sort| 排序| `sort -n data.txt`  
uniq| 去重| `sort file.txt | uniq -c`  
sed| 流编辑器| `sed 's/old/new/g' file.txt`  
awk| 列处理| `awk '{print $1}' data.txt`  
  
## 权限管理（3 个）

命令| 用途| 示例  
---|---|---  
chmod| 修改权限| `chmod +x script.sh`  
chown| 修改所有者| `chown user:group file`  
sudo| 超级用户权限| `sudo systemctl restart nginx`  
  
## 系统信息（5 个）

命令| 用途  
---|---  
ps aux| 查看进程  
top/htop| 实时资源监控  
df -h| 磁盘空间  
free -h| 内存使用  
uname -a| 系统信息  
  
## 网络（3 个）

命令| 用途  
---|---  
curl| 发送 HTTP 请求  
ping| 测试连通性  
netstat| 网络连接状态  
  
## 管道和重定向（3 个）

符号| 用途| 示例  
---|---|---  
|| 管道| `cat log.txt | grep error | wc -l`  
>| 输出重定向| `echo "hello" > file.txt`  
>>| 追加输出| `echo "world" >> file.txt`  
  
## 推荐学习路径

先掌握文件操作 → 文本处理 → 管道重定向（这是 Linux 的精髓）→ 权限管理 → Shell 脚本编写。

### 📖 相关推荐

  * [正则表达式 30 分钟入门指南](<https://dingjiu1989-hue.github.io/tech/regex-guide.html>)
  * [Python 入门教程：从零到写出第一个程序](<https://dingjiu1989-hue.github.io/tech/python-tutorial.html>)
  * [Git 常用命令速查表](<https://dingjiu1989-hue.github.io/tech/git-cheatsheet.html>)
