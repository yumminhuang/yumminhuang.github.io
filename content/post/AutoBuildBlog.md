+++
date = "2016-11-12T12:31:51+08:00"
categories = ["Miscellaneous"]
tags = ["CI", "Docker"]
title = "自动构建 Github Pages 博客"
isCJKLanguage = true
+++

之前曾经写过了一篇 [使用 Travis CI 和 Docker 自动构建 LaTeX 简历](https://yumminhuang.github.io/post/AutoBuildResume/)，介绍了使用 Travis CI 和 Docker 自动构建和发布 LaTeX 简历的方法。

以前每次写了新文章之后，都需要在笔记本上运行一下 Hugo 再将生成的网页上传到 Github。虽然使用脚本也可以做到一键发布，但总觉得不够流畅。昨天，我又使用了同样的方法，将基于 Github Pages 的博客也实现了自动构建和发布。

<!--more-->

### 整理工作

之前，为了搭建 [Github Pages](https://pages.github.com/) 的博客，我创建了两个代码库。一个是存放网站的 yumminhuang.github.io.git，另外一个是存放 Hugo 配置和文章的 Blog.git。每次发布一篇文章，都需要同步两个代码库。

两个代码库也没有必要。于是我把 Blog.git 库删除了，把 Hugo 的配置和文章都存放在了 yumminhuang.github.io.git 的 source 分支里。

当然，还是有必要保留以前提交的历史记录。大概的操作流程是：

```Bash
git clone git@github.com/yumminhuang/Blog.git
cd Blog
# Delete the old remote
git remote rm origin
# Add a new remote
git remote add origin git@github.com:yumminhuang/yumminhuang.github.io.git
# (Optional) Modify .git/config for submodules, etc
vi .git/config
# Create the new branch and switch to it
git checkout -b source
# Push the new branch to remote
git push origin source
```

这样，原来 Blog.git 里的内容和提交历史就保存到了 yumminhuang.github.io.git 的 source 分支里。

### Docker for Hugo

接下来的任务就是创建一个 Docker 容器来生成网页。参考了一些网上的 Hugo Dockerfile 之后，我写了如下的一个 [Dockerfile](https://github.com/yumminhuang/hugo-docker) 用来生成 Docker Image。 这个 Image 只安装了 Hugo，比较小巧，压缩后只有 8MB，很适合用来在 CI 系统上使用。

```dockerfile
FROM alpine:latest
MAINTAINER Yaming Huang <yumminhuang@gmail.com>

ARG HUGO_VERSION=0.17

RUN apk add --update wget ca-certificates && \
  cd /tmp/ && \
  wget https://github.com/spf13/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
  tar xzf hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
  rm -r hugo_${HUGO_VERSION}_Linux-64bit.tar.gz && \
  mv hugo*/hugo* /usr/bin/hugo && \
  apk del wget ca-certificates && \
  rm /var/cache/apk/*

VOLUME /website
VOLUME /public

WORKDIR /website
ENTRYPOINT ["/usr/bin/hugo"]

EXPOSE 1313
```

Build 之后生成 `yumminhuang/hugo-docker`， 这样每次运行一条命令，就可以生成网页到 `public` 目录下。

```
docker run --rm -v $(pwd):/website yumminhuang/hugo:latest
```

还可以运行如下的命令用来看网页生成的效果。

```
docker run --rm -p 1313:1313 -v $(pwd):/website yumminhuang/hugo:latest server --bind=0.0.0.0 -w -D
```

### Travis CI

接下来是设置 Travis CI 来进行自动构建。

首先，需要先到 Github 的[个人设置](https://github.com/settings/tokens)页面去[创建一个 “Personal Access Token”](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)。确保选择了 `repo` 下面的 `public_repo`。 创建出来的 “Personal Access Token” 可以用来读、写代码库，所以要妥善保管，不能外泄。

接着，需要使用 [Travis 命令行工具](https://github.com/travis-ci/travis.rb)来对包含新生成 “Personal Access Token”  的变量 `GIT_DEPLOY_REPO` 加密。

```
travis encrypt GIT_DEPLOY_REPO=https://GENERATED_TOKEN@github.com/username/reponame.git
```

`GIT_DEPLOY_REPO` 将用于把网页上传到 Github，后文会有提及。

完整的 `.travis.yml` 如下所示。

```yaml
env:
  global:
  - secure: " LONG TOKEN "
  - GIT_DEPLOY_DIR=public
  - GIT_DEPLOY_BRANCH=master
  - GIT_DEPLOY_USERNAME="Travis CI"
  - GIT_DEPLOY_EMAIL=yumminhuang@gmail.com

branches:
  only:
    - source

sudo: required

services:
  - docker

install:
  - rm -rf public || exit 0
  - git config --global user.email "yumminhuang@gmail.com"
  - git config --global user.name "Travis CI"

script:
  - docker run --rm -v $(pwd):/website yumminhuang/hugo:latest

after_success:
  - wget https://raw.githubusercontent.com/X1011/git-directory-deploy/master/deploy.sh -O deploy.sh
  - bash deploy.sh -m "updating blog `date`"
```

在 `after_success `，也即 Hugo 完成网页生成之后，会使用 [X1011/git-directory-deploy](https://github.com/X1011/git-directory-deploy) 里的 `deploy.sh` 将网页提交并上传到 Github。使用 `deploy.sh` 只需要设置这几个变量，就可以完成把一个目录同步到 Github 的功能。

- `GIT_DEPLOY_REPO`
- `GIT_DEPLOY_DIR`
- `GIT_DEPLOY_BRANCH`
- `GIT_DEPLOY_USERNAME`
- `GIT_DEPLOY_EMAIL`

接下来，在 Travis CI 上完成授权，就能够在每次提交到 `source` 分支后出发自动构建了。

### 参考内容
1. [Setup Hugo with Travis CI and GitHub Pages](http://speps.github.io/articles/hugo-setup/)
2. [Static Website Generation on Steriods with Docker](http://blog.hypriot.com/post/static-website-generation-on-steriods-with-docker/)
3. [jojomi/docker-hugo](https://github.com/jojomi/docker-hugo)
