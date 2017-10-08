+++
title       = "Graphite 和 Grafana 简介"
tags        = ["DevOps", "Graphite", "Grafana"]
categories  = ["DevOps"]
date        = "2015-04-08"
+++

## Graphite

[Graphite](http://graphite.wikidot.com/start) 是一款开源的监控绘图工具。

Graphite 可以实时收集、存储、显示时间序列类型的数据（time series data）。它主要有三个部分构成：
<!--more-->

1. **[carbon](https://github.com/graphite-project/carbon)** —— 基于 [Twisted](https://twistedmatrix.com/trac/) 的进程，用来接收数据；
2. **[whisper](https://github.com/graphite-project/whisper)** —— 专门存储时间序列类型数据的小型数据库；
3. **[graphite webapp](https://github.com/graphite-project/graphite-web)** —— 基于 Django 的网页应用程序。

![Graphite Overview](https://raw.githubusercontent.com/graphite-project/graphite-web/master/webapp/content/img/overview.png)

### 向Graphite发送数据

Graphite 的使用非常简单。我们可以定义一个被观测量（Metric）。Metric 使用键／值的数据类型。只要不断发送`观测量: 观测值`这一键值组合，就可以得到以时间为X轴，观测值为 Y 轴的图。

当我们使用诸如 collectd、Sensu 之类的工具收集到数据之后，只需要向 Graphite 的服务器发送以下格式的 TCP 报文即可：

```
<metric name> <metric value> <metric timestamp>
```

例如，有一个 Metric 叫作 `local.metric.random`，可以用下面的 Bash 命令发送当前时刻的值 `4`。

```shell
PORT=2003
SERVER=graphite.your.org
echo "local.metric.random 4 `date +%s`" | nc -q0 ${SERVER} ${PORT}
```

类似地，使用其它编程语言时，可以使用 Socket 发送数据。

另外，Graphite 的 Metric 名称支持以 `.` 作为分隔符的多级嵌套。例如我可以定义下面三个 Metric。

* `webserver.system.cpu_usage`
* `webserver.system.mem_load`
* `webserver.network.input`

Graphite 将以树型结构展示这三个 Metric。因此，使用 Graphite 的第一步就是给 Metric 选取一个合适的名称。关于如何组织 Metric 的名称，可以参阅文章 [Practical Guide to StatsD/Graphite Monitoring](http://matt.aimonetti.net/posts/2013/06/26/practical-guide-to-graphite-monitoring/)。

### Graphite Event

除了支持简单的键／值数据类型，Graphite 还可以通过 [Events](http://graphite.readthedocs.org/en/1.0/functions.html#graphite.render.functions.events) 来存储更复杂的数据。简而言之，Graphite Events 使用了 `tag` 和 `data` 两个键来存储更多的信息。

我们可以使用 HTTP POST 向 Graphite 发送一个 Event。

```shell
curl -X POST "http://graphite.your.org/events" -d '{"what": "Deployment", "tags": "webserver", "data": "Deploy webserver"}'
```

下文将会通过一个具体的实例来介绍Events的使用场景。

## Grafana

鉴于 Graphite 的界面过于简单，功能比较单一，可以使用 [Grafana](http://grafana.org/) 作为 Graphite 的控制台。 Grafana 是一款开源的图形控制台，有很多[不错的特性](http://grafana.org/features)，还可以访问官网提供的 [Live Demo](http://play.grafana.org) 来体验 Grafana。

设置 Grafana，只需编辑 `config.js` 设置数据来源[^update]。

```js
datasources: {
  graphite: {
    type: 'graphite',
    url: "http://my.graphite.server.com:8080",
  }
},
```

具体的配置教程可以参见[官方文档](http://docs.grafana.org/v1.9/installation/)。

## 实例

我实习所在公司使用 [Jenkins](https://jenkins-ci.org) 部署代码。在部署完成之后，我添加了一段 [post-build script](https://wiki.jenkins-ci.org/display/JENKINS/PostBuildScript+Plugin) 执行下面的脚本。

```shell
#!/bin/bash

HOST=http://graphite.your.org/events
echo 'Posting a deployment event to Graphite'
curl -X POST $HOST -d '{"what": "Deployment", "tags": "webserver,prd", "data": \"$BUILD_URL\"}'
```

这样，每次部署完成之后都会发送一个 Deployment Event 到 Graphite。接着，可以在 Graphite 里添加 `drawAsInfinite(events('prd'))` 或者在 Grafana 里使用 [Annotations Page](http://grafana.org/docs/features/annotations/) 来绘制一幅图显示代码部署的 Events。

利用 Graphite Events 和 Metrics，我们可以将代码部署和其他指征叠加在一幅图里，从而分析每次代码部署和其它指征的关系。

比如，在 *Tracking Every Release* 一文中，作者使用了该方法将 `PHP Warning` 和 `Code deploy` 叠加在一幅图里。

![Track Release](https://codeascraft.com/wp-content/uploads/2010/12/warnings_1hr_deploys3.png)

从图中，我们可以发现第一次代码部署之后导致了大量的警告信息，经过随后的两次 Hotfix 之后，警告信息基本消除。

## 总结
本文非常简要地介绍了 Graphite 和 Grafana 的一些特性和使用场景。我也是在实习当中第一次接触到这两个工具，很多具体的细节还在摸索之中。

总之，Graphite 是一个易扩展，使用简便的监控绘图工具，在这里推荐给大家使用。

## 参考文献
1. [Graphite Tip - A Better Way to Store Events](http://obfuscurity.com/2014/01/Graphite-Tip-A-Better-Way-to-Store-Events)
2. [Tracking Every Release](https://codeascraft.com/2010/12/08/track-every-release/)
3. [Making Annotations in Graphana](http://joshhertz.se/post/making-annotations-in-graphana)

[^update]: Grafana 最新的 2.0 较 1.9 有较大的变化，不再使用 `config.js` 来进行配置，需要将配置保存到数据库中。相应章节暂未更新，俟后补。
