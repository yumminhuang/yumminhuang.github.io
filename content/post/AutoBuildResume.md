+++
categories = ["Miscellaneous"]
date = "2016-04-08T15:17:48-04:00"
tags = ["CI", "Docker"]
title = "使用 Travis CI 和 Docker 自动构建 LaTeX 简历"
+++

又快到了求职季，最近一段时间总是频繁更新的简历。之前，我的简历更新流程是先修改简历，使用 MacTeX 编译，再把 PDF 版的简历同步到几个网盘备份。过程倒也不算繁琐。但再做过几个月的运维开放之后，我对自动化有着近乎偏执的热情。这几天经过不断的尝试和摸索，在 Travis-CI 上运行了十几个 Build 之后，终于使用 Docker 实现了一个便捷的自动化发布 LaTeX 简历的方法。

<!--more-->

本文中提到的简历已经放在了 [GitHub](https://github.com/yumminhuang/Resume) 上，欢迎参考。

当然，本文的主要内容集中在持续发布的流程，而非 LaTeX 和 Docker 的使用，所以对 LaTeX 简历和 Docker 命令不做细致的解释。事实上，GitHub 上有很多精美的 LaTeX 简历模板，我的简历也借鉴了其中的一个模板。

### 使用 Travis-CI 自动发布

上周在 [LaTeX 开源小屋](http://www.latexstudio.net)看到一篇[文章](http://www.latexstudio.net/archives/5892)。文章中介绍了 GitHub 上一个[北航小操作系统实验指导书](https://github.com/SivilTaram/BUAAOS-guide-book)的代码库。这个代码库里使用 Travis-CI 与 LaTeX 构建开源中文 PDF。每次提交到 GitHub 之后，可以自动运行 Travis-CI 编译，并将 PDF 文件发布到 [GitHub Release 页面](https://help.github.com/articles/about-releases/)。

于是，我以此开源项目为模板，同时参考了另一篇文章 [*Setup LaTeX PDF build using Travis CI*](http://harshjv.github.io/blog/setup-latex-pdf-build-using-travis-ci/) 及[代码](https://github.com/harshjv/travis-ci-latex-pdf)，将自己的简历实现了自动化编译与发布。

先看一下我的 `.travis.yml`。

```yaml
sudo: required
dist: trusty
before_install:
- sudo apt-get update
- sudo apt-get -y --no-install-recommends install texlive-full
- sudo wget -P /usr/share/fonts/opentype/ https://github.com/SivilTaram/BUAAOS-guide-book/raw/master/guide-book/fonts/AdobeFangsongStd-Regular.otf
- sudo wget -P /usr/share/fonts/opentype/ "https://github.com/SivilTaram/BUAAOS-guide-book/raw/master/guide-book/fonts/AdobeHeitiStd-Regular%20(v5.010).otf"
- sudo wget -P /usr/share/fonts/opentype/ "https://github.com/SivilTaram/BUAAOS-guide-book/raw/master/guide-book/fonts/AdobeKaitiStd-Regular%20(v5.010).otf"
- sudo wget -P /usr/share/fonts/opentype/ "https://github.com/SivilTaram/BUAAOS-guide-book/raw/master/guide-book/fonts/AdobeSongStd-Light%20(v5.010).otf"
- sudo mkfontscale
- sudo mkfontdir
- sudo fc-cache -f
script:
- cd resume
- make
- cd ..
- mv resume/Resume.pdf Resume.pdf
- mv resume/Resume_ZH.pdf Resume_ZH.pdf
deploy:
  provider: releases
  api_key:
    secure: [A LONG LONG TOKEN, omit it]
  file:
    - Resume.pdf
    - Resume_ZH.pdf
  skip_cleanup: true
  on:
    repo: yumminhuang/Resume
```

首先前两行声明了需要的权限和使用 [Travis CI 的 Trusty（即 Ubuntu 14.04）编译环境](https://docs.travis-ci.com/user/trusty-ci-environment/)。

接着，`before_install` 后的命令用来安装 texlive 和字体，更新系统字体列表。

然后，在 `script` 阶段，运行 `make` 命令编译，移动 PDF 文件到项目的根目录。

最后，在 `deploy` 阶段，使用 Travis-CI 的 API 将文件发布到 Github Release。这里，需要一个 `api_key`，可以运行 [Travis 命令行客户端](https://github.com/travis-ci/travis.rb#installation)来生成。关于使用 Travis-CI 将文件发布到 Github Release 的更详细内容还请参考 [Travis-CI 的官方文档](https://docs.travis-ci.com/user/deployment/releases)。

这样，我就完成了可以自动编译、自动发布的 [1.0 版](https://github.com/yumminhuang/Resume/releases/tag/v1.0)。

### 优化持续发布流程

1.0 版完成只实现了自动化，还有一些不令人满意的地方。

第一，安装过程复杂，构建花费时间长。每次构建大概需要 10 分钟左右，大部分的时间都花在安装 texlive 上。「北航实验指导书」中选择安装 texlive-full，这避免了缺少依赖的问题，但却安装了很多没有用的依赖，同时花费了大量时间。另外，下载字体也花费了一定的时间。

第二，频繁的不必要的构建。按照「北航实验指导书」中的设置，每次提交一个更新都会触发构建。事实上，这是没有必要的，因为有时候可能只是更新 README，而非 LaTeX 源码。「北航实验指导书」中为了避免这一问题，很多提交更新都加上了 `[ci skip]` 的前缀来[跳过自动构建](https://docs.travis-ci.com/user/customizing-the-build/#Skipping-a-build)。这样无形中增加了开发过程的负担。

最后，编译出来的中文简历格式令我不要满意。Ubuntu trusty 的环境中，使用 `apt-get` 只能安装 texlive 2013；而我的中文简历使用了新版 ctex 的特性，需要用到 texlive 2015。如果在 trusty 里下载 texlive 2015 的镜像安装可能又需要安装更多的工具链，很麻烦；在 Ubuntu 15.10 和 Ubuntu 16.04 中倒是可以使用 `apt-get` 安装 texlive 2015，但 Travis-CI 似乎只提供了 Ubuntu trusty，没有更新的版本。

为了解决这三个问题，我做了两点改进。

#### 使用 Docker 编译

既然 Ubuntu 16.04 可以安装运行 texlive 16.04，何不使用 Docker 容器来运行？同时，为了避免安装没用的软件包，我花了一些时间找出了编译中文 LaTeX 的必要依赖和宏包，然后将安装和编译的过程写成一个脚本 `build.sh`。

```shell
#!/bin/bash

# install texlive 2015 and dependencies
apt-get update && \
apt-get install -y --no-install-recommends \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-lang-chinese \
    texlive-formats-extra \
    lmodern \
    wget \
    xzdec

# intsall latex packages
tlmgr init-usertree
tlmgr install ulem

cd resume/
# run xelatex
xelatex Resume.tex -interaction=nonstopmode
xelatex Resume_ZH.tex -interaction=nonstopmode

rm *.aux *.log *.out
```

这样，使用一个 Ubuntu 16.04 的容器运行该脚本就可以生成简历了。接着，我把 `.travis.yml` 的 `before_install` 和 `script` 过程简化成下面的设置。

```yaml
services:
  - docker

script:
- docker run --rm -v $(pwd)/resume:/resume ubuntu:xenial bash /resume/build.sh
- mv resume/Resume.pdf Resume.pdf
- mv resume/Resume_ZH.pdf Resume_ZH.pdf
```

主要过程就是创建一个 Ubuntu xenial 容器来运行 `build.sh`。后面发布过程的设置和 1.0 版一样。

最后，使用 Docker 之后，不仅可以编译出格式满意的简历，而且我惊喜地发现整个构建过程耗时 3 分钟多，只有之前的 1/3。

#### Build tagged commits only

为了避免不必要的构建，我在 `.travis.yml` 中加入下面三行内容作为「白名单」，即使用正则表达式规定需要构建的 branches。

```yaml
branches:
  only:
    - /^v[\d.]+\d$/
```

需要注意的是，Travis-CI 把 git 的标签（tag）和分支（branch）都视作 branches，关于如何设置特定 branch 进行构建，可以参见[Travis-CI 的官方文档](https://docs.travis-ci.com/user/customizing-the-build/#Building-Specific-Branches)。

这样，我平时可以正常地提交更新而不会触发 Travis-CI。需要发布新的简历时，按照 `^v[\d.]+\d$` 的格式，比如 `v1.2.1`，加一个标签再提交即可。

```shell
git add -a
git commit -m "Message"
git tag v1.2.1
git push -u origin master --tags
```
