+++
title       = "Travis CI"
tags        = ["DevOps", "CI"]
categories  = ["DevOps"]
date        = "2015-06-20"
+++

本文将主要介绍如何使用 [Travis CI](https://travis-ci.org) 托管 Github 上的开源项目，从而实现自动化测试、部署。同时，还将介绍使用 [Coveralls](https://coveralls.io/) 来监测测试覆盖率。
<!--more-->

## Travis CI

Travis CI 是一款 Web 端的 <ruby> 持续 <rt>Continuous</rt></ruby> <ruby> 集成 <rt>Integration</rt></ruby> 工具。

Travis CI 采用 [「Freemium」](https://en.wikipedia.org/wiki/Freemium) 的模式：对 Github 上的开源项目免费，付费的话则可以托管私有项目。Github 上很多知名的开源项目都适用 Travis CI 来进行自动化测试。

和 Jenkins 相比，Travis CI 要轻量很多。但是已经足以完成简单的自动化测试、部署。

## Coveralls

Coveralls 用来显示代码覆盖率，从而可以让程序员及时了解代码质量。

Coveralls 和 Travis CI 一样，仅对 Github 上的开源项目免费。Coveralls 支持包括 Travis CI、Jenkins 在内的绝大多数持续集成工具。

## 样例

接下来以 Python 项目为例，说明如何使用 Travis CI 和 Coveralls[^src]。

### 依赖管理和虚拟环境

我喜欢为每个项目新建一个 <ruby>virtualenv<rt> 虚拟环境 </rt></ruby>，这样可以确保每个项目的开发环境相互独立，避免发生冲突。[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) 是一个让人方便使用 virtualenv 的小工具。它把如新建 virtualenv、切换 virtualenv 等常用的操作都封装成了简单的指令。

我一般会在项目中添加一个 `requirements.txt`，里面列出项目所依赖的 Pip 库。这样在 virtualenv 中，直接运行

```
pip install -r requirements.txt
```

就可以安装所有的库。

### 单元测试和测试覆盖

对于 Python 项目，我喜欢使用 [nose](https://nose.readthedocs.org/en/latest/) 来进行单元测试。此外，我还会使用 [coverage.py](http://nedbatchelder.com/code/coverage/) 来测量代码的测试覆盖率。

nose 对 coverage.py 的支持非常好，可以在 `nosetests` 命令后添加一系列选项来生成覆盖率。

```
nosetests --with-coverage
```

就可以直接得到测试覆盖率的数据。

详细的使用方法可以参见 [nose 的官方文档](https://nose.readthedocs.org/en/latest/) 和[coverage.py 的官方文档](http://nedbatchelder.com/code/coverage/cmd.html)。

### 持续集成
在 Github 上新建项目之后，在 Travis CI 的页面上开启该项目。（新建的项目可能不会及时出现在 Travis CI 页面上，需要手动同步一下 Github 的项目。）接着，在 Github 项目里添加 Travis CI 的配置文件 `.travis.yml`。Travis CI 的配置使用的是非常易读的 YAML 文件。

```
language: python
python:
    - 2.6
    - 2.7
# command to install dependencies
install:
    - pip install -r requirements.txt
    - pip install coveralls
# command to run tests
script:
    nosetests --cover-package=project --with-coverage
# coveralls
after_success:
    coveralls

```

同样地，也需要在 Coveralls 上开启相应的项目。

这样，Github 的代码库在每次收到 `Push` 和 `Pull Request` 的时候，Travis CI 都会按照配置文件上的步骤自动运行测试（或者部署，本样例只有测试。），并且把测试覆盖率的数据发布到 Coveralls。

详细的配置说明可以参见 [Travis CI 的官方文档](http://docs.travis-ci.com/) 和[Coveralls 的官方文档](https://coveralls.zendesk.com/hc/en-us)。

### 其它
Travis CI 和 Coveralls 都可以生成 <ruby> 图章 <rt>Badge</rt></ruby>，用来显示 <ruby> 构建 <rt>Build</rt></ruby> 的结果，或者测试覆盖率。

[![Build Status](https://travis-ci.org/yumminhuang/turbo-octo-meme.svg?branch=master)](https://travis-ci.org/yumminhuang/turbo-octo-meme)

可以将这些图章（如果已经发布到 PyPi，还可以加上版本号、下载量的图章。）放在项目的 *README* 文件里。

[^src]: 详细代码可参见 [turbo-octo-meme](https://github.com/yumminhuang/turbo-octo-meme)。
