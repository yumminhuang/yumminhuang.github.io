+++
title       = "使用 Fabric 进行远程操作"
categories  = ["DevOps"]
tags        = ["DevOps", "Python", "Fabric"]
date        = "2015-04-16"
+++

## Fabric 简介

[Fabric](http://www.fabfile.org) 是一个实现远程操作和部署的 Python 模块。Fabric 主要用来作为 SSH 的替代，实现一些简单的应用部署和系统管理。
<!--more-->


### 使用 Fabric 的好处

个人觉得，Fabric 非常适合简单的、重复性的远程操作。

首先，Fabric 可以使用 Python，比 Shell 要强大、灵活。

再者，Fabric 避免远程登录，可以把远程操作放在本地运行。

最后，Fabric 非常简单，只需要编写一个 `fabfile.py`（或者像 Python 那样 [导入包来添加更多的功能](http://docs.fabfile.org/en/latest/usage/fabfiles.html)），就可以使用[`fab` 指令](http://docs.fabfile.org/en/latest/usage/fab.html) 运行了。这比 Salt、Chef 等工具轻量，更加容易上手。

基本上，代码部署，文件修改，远程执行等操作都可以使用 Fabric。

## 常用的 Fabric 函数

这里简单地介绍 Fabric 里常用的函数，具体的说明请参见 [官方文档](http://docs.fabfile.org/en/latest/index.html)。

## 常用操作

Fabric 的常用 [操作](http://docs.fabfile.org/en/latest/api/core/operations.html)

* `run`：在远程机器上执行 Shell 命令；
* `sudo`：带有 root 权限的 `run`；
* `local`：执行本地命令；
* `get`：从远程机器下载文件；
* `put`：上传文件到远程机器；
* `prompt`：可以理解为在远程机器上执行 `raw_input`
* `reboot`：重启远程机器。

### 常用上下文管理器和装饰器
上下文管理器（Context Manager）和装饰器（Decorators）是 Python 中的常用的 [「语法糖（Syntax sugar）」](http://zh.wikipedia.org/wiki / 语法糖)。Fabric 中常用的[上下文管理器](http://docs.fabfile.org/en/latest/api/core/context_managers.html) 有：

* `cd`：切换目录；
* `lcd`：在本地切换目录，即 `local cd`；
* `path`：可以添加路径到 `PATH`;
* `settings`：用来临时修改 `env` 变量，使变量只作用在一段代码中。

常用的 [装饰器](http://docs.fabfile.org/en/latest/api/core/decorators.html) 有：

* `@task`：用来把一个函数声明为 [Fabric Task](http://docs.fabfile.org/en/latest/usage/tasks.html)；
* `@hosts`：用来制定远程操作的目标机器；
* `@with_settings`：用来临时设定 `env` 变量，可以等同于 `with settings`。

Fabric Task 是我个人非常喜欢的功能。定义一个 Task 之后就可以直接使用 `fab task_name` 来执行了。

## 一个例子

在实习当中，我做了一个工具用来自动备份 AWS EBS Volume。程序运行在远程服务器上。每天早上，我都要检查一下日志文件，看看程序有没有出错。

开始，我检查的方式是使用 `ssh` 登陆之后，再使用 `grep` 检查日志文件是否包含 `ERROR`、`WARNING` 等关键字。后来，我发现检查日志文件的操作都是一些重复操作，于是就写了一个 Bash 脚本来进行检查。这样，每天检查的过程就是使用 `ssh` 登陆，再运行脚本进行检查。

但是，这样检查日志还是有一些麻烦，这促使我转而使用 Fabric。第一，每天都需要远程登录。使用 Fabric 可以直接在本地运行。第二，因为日志每天晚上会回滚，我不仅要检查当天的日志文件，还要检查昨天的日志来确保昨天下班之后程序没有出问题，而日志的名称会随着日期变化。在 Bash 里计算日期是一件相当麻烦的事情。但是，使用 Fabric 之后，因为可以利用 Python 的 `datetime`，计算日期就变得非常容易了。下面就是用来检查日志是否包含关键字的函数。

```
from fabric.api import *

def check_log_with_keyword(log_file, keyword):
    with settings(hide('warnings','output'),
                  host_string='eb101.ops',
                  warn_only=True):
        result = run('grep %s %s' % (keyword, filename))

        if result.return_code == 0:
            print(result)
```

* 使用 `with settings()` 来临时更改 `env` 变量；
* `hide('warnings', 'output')` 可以设置 Fabric 输出（不是远程执行的指令的输出），隐藏 `stderr` 和 `stdout`；
* `host_string='eb101.ops'`，设定目标机器，Fabric 可以使用 `.ssh/config` 的设置；
* `warn_only=True` 用来确保 Fabric 程序不会因为 `grep` 指令出错而退出（grep 没找到匹配内容时，返回值是 1）；
* `result = run('grep %s %s' % (keyword, filename))`, 运行 `grep` 指令并得到结果。

远程检查日志的过程很简单，并且是机械而重复的过程，因此非常适合使用 Fabric。

### 参考文献

1. [How To Use Fabric To Automate Administration Tasks And Deployments](https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments)
