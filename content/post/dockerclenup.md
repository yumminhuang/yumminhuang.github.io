+++
title 		= "清理 Docker"
tags 		= ["Docker"]
categories	= ["Miscellaneous"]
date		= 2017-10-13T22:26:29+08:00
+++

在线上环境运行的 Docker 的时候，部署之后往往没有清理旧版本的镜像和关闭的容器。如此一来，长时间运行 Docker，尤其是频繁地更新镜像、启动容器，会消耗大量的磁盘空间。

本文汇总几条用来清理 Docker 的命令。

<!--more-->

## 清理 Docker 容器

```shell
docker ps --filter status=dead --filter status=exited -aq | xargs -r docker rm -v
```

## 清理 Docker 镜像

清理 *dangling* 的镜像。

```shell
docker images -q -f dangling=true | xargs -r docker rmi
```

清理所有当前不在运行的镜像[^exp]。

```shell
docker rmi $(grep -xvf <(docker ps -a --format '{{.Image}}') <(docker images | tail -n +2 | grep -v '<none>' | awk '{ print $1":"$2 }'))
```

清理一周前的镜像。

```shell
docker images --no-trunc --format '{{.ID}} {{.CreatedSince}}' | grep ' weeks' | awk '{ print $1 }' | \
       xargs --no-run-if-empty docker rmi
```

## 清理 Docker Volume

```shell
docker volume ls -q -f dangling=true | xargs -r docker volume rm
```

## 参考

* [comment on Github Issue](https://github.com/moby/moby/issues/9054#issuecomment-184246090)
* [Cleaning up docker to reclaim disk space](https://lebkowski.name/docker-volumes/)

[^exp]: 此命令清理效果好，却容易误删当前没有运行但未来仍会使用的镜像。
