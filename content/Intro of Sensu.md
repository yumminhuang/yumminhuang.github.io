Title: Sensu简介
Date: 2015-04-04 14:28
Modified: 2015-03-31 20:49
Category: DevOps
Tags: DevOps, Sensu

## Sensu简介
Sensu是一款开源的监控框架。

![Sensu components](http://sensuapp.org/docs/0.16/img/sensu-diagram-87a902f0.gif)

Sensu采用C/S结构，有用来发送指令、存储数据的Sensu Server和被监控的对象Sensu Client。Sensu Server和Sensu Client之间使用RabbitMQ进行通信，Server端使用Redis存储数据。每一个Sensu Client使用JSON进行设置。例如：

	:::JSON
	{
	  "client": {
	    "name": "i-424242",
	    "address": "127.0.0.1",
	    "subscriptions": [
	      "production",
	      "webserver"
	    ]
	  }
	}

其中，`subscriptions`指定了Sensu Client订阅哪些监控项目。 Sensu采用了[订阅者模式](http://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern)，相应地，定义监控项目的时候则需要指定`subscribers`（后文中将会提及）。

### Sensu 的优势

* 纯Ruby实现，核心代码不超过1000行；
* 配置简单，配置文件使用JSON；
* 结构简单，易扩展，很容易就能够上手编写插件；
* 丰富的社区支持，[Sensu Community Plugin](https://github.com/sensu/sensu-community-plugins)几乎包含了所有常用的监控项目。

### Sensu 的结构
简单来说，Sensu分为Check和Handler两个部分。Sensu经常被描述为「monitoring router」，因为它不仅可以用Check监控系统，还可以设置Handler根据当前的条件采取相应的行动。

#### Sensu Check
Sensu Check用来监控服务和资源。Check由Sensu Server发出执行指令后在Sensu Client上运行。本质上，Sensu Check是一个命令或者脚本，用来把数据输出到`STDOUT`或者`STDERR`；同时，用返回值（exit status code）来指示状态：

* `0`： OK
* `1`：WARNING
* `2`：CRITICAL
* `>3`：UNKNOWN or CUSTOM

因此，只要定义好返回值和输出，很容易就可以写出一个Sensu Check。下面就是一个用来监测`chef-client`进程是否在运行的Ruby脚本。

	:::Ruby
	procs = `ps aux`
	running = false
	procs.each_line do |proc|
	  running = true if proc.include?('chef-client')
	end
	if running
	  puts 'OK - Chef client daemon is running'
	  exit 0
	else
	  puts 'WARNING - Chef client daemon is NOT running'
	  exit 1
	end

写好一个Check的脚本，需要在配置文件中添加它。比如下面,

	:::JSON
	{
	  "checks": {
	    "chef_client": {
	      "command": "check-chef-client.rb",
	      "subscribers": [
	        "production"
	      ],
	      "interval": 60,
	      "handlers": [
	        "pagerduty",
	        "mail"
	      ]
	    }
	  }
	}

`subscribers`用来指定订阅者。`interval`定义检查的周期为`60s`，`handlers`则告诉Sensu当此Check出现异常时使用`pagerduty`和`mail`这两个Handler。

#### Sensu Handler
Sensu Handler用来处理Sensu Check产生的Event，例如发送邮件通知，将采集的数据发送到[Graphite](http://graphite.wikidot.com)，等等。 Handler有不同的类型，有常用的`Pipe`，可以将Event传入到`STDIN`（可以理解为`cat event.json | handler`）；有TCP/UDP，将Event传入到Socket发送。

下面是一个简单的Sensu Handler定义，用来将Event的内容发送到指定的邮箱地址。
	
	:::JSON
	{
	  "handlers": {
	    "mail": {
	      "type": "pipe",
	      "command": "mailx -s 'sensu event' email@address.com"
	    }
	  }
	}
		
## 基于Sensu的安全更新监控工具
接下来，结合我这次实习里的一个项目来详细地介绍一下Sensu的使用。

### 需求
我们公司在AWS上有大约350个实例[^Instance]，运行的是Ubuntu操作系统。服务器上的软件会不定期收到更新，包括非常重要的安全更新。我们希望及时知道服务器上有哪些安全更新可以安装，最好可以通过邮件的方式通知。通知里应当至少包括如下信息：

1. 更新的软件包名称；
2. 软件包当前的版本；
3. 可供安装的版本。

此外，一个邮件里包含350台机器的信息显然不方便阅读。恰好公司的350台服务器根据功能分为若干个`subnet`，如dev，tst，stg等。所以，最好可以为每一个subnet生成一份安全更新的报告。

### 实现
#### 安全更新的信息收集
使用Debian/Ubuntu的用户都知道，每次登陆都会看到类似的信息：

```
17 packages can be updated.
6 updates are security updates.
```
以此为源头，我找到了Debian系统内自带的一个Python脚本`/usr/lib/update-notifier/apt_check.py`。它可以调用[python-apt](https://apt.alioth.debian.org/python-apt-doc/index.html)库收集系统当前可以安装的安全更新。以此脚本为基础稍加改动就可以得到我们所需要的信息。

我已经把修改过的脚本做成了一个[Sensu Plugin](https://github.com/sensu/sensu-community-plugins/blob/master/plugins/system/package-updates-metric.py)提交到了Sensu社区。

####信息的汇集和通知
第一步非常顺利，但是还有问题需要解决：

1. Python脚本只能收集本地的信息，如何把350台服务器的信息汇集在一起？
2. 信息汇集完了如何进行分类、通知？

为了解决这两个问题，就需要用到本文的主角Sensu了。

第一个问题是汇集多台机器的检查结果。事实上，通常的Sensu Check也只能检查一台机器。为了解决第一个问题，我使用了[Sensu Aggregate API](http://sensuapp.org/docs/0.16/api_aggregates)。我们可以把一个Sensu Check定义成[Aggregate Check](http://sensuapp.org/docs/0.16/checks)，然后通过API可以得到所有该Check的结果。

因此，整个安全更新监控工具使用了两个Sensu Check。第一个Aggregate Check运行在所有的服务器上，用来收集本地的安全更新。第二个Check运行在一台服务器上，它会调用Aggregate API读取第一个Check的结果，再加以归类、分析。如果有安全更新可以安装，就触发Handler发送通知邮件。

第一个Check的定义：

	:::JSON
	{
	  "checks": {
	    "apt-check": {
	      "command": "package-updates-metric.py",
	      "subscribers": [
	        "production"
	      ],
	      "interval": 28800,
	      "aggregate": true,
	      "handler": false
	    }
	  }
	}

第二个Check的定义：

	:::JSON
	{
	  "checks": {
	    "aggregate_apt_check": {
	      "command": "package-updates-check.py",
	      "subscribers": [
	        "mg102.ops"
	      ],
	      "publish": false,
	      "handler": "package-updates-notify.rb",
	    }
	  }
	}

其中，`package-updates-check.py`是另外一个Python脚本，主要是访问API并且读取结果。如果发现了安全更新就输出结果并返回`1`，这样就可以触发`package-updates-notify.rb`。这是一个Ruby脚本，用来读取第二个Check的结果，再把结果分成不同的subnet发送邮件。
另外，这里设置了`"publish": false`，所以这个Check需要手工启动（因为没有必要定时调用，每天一次足矣），可以通过以下命令来手动请求Sensu Check。

	:::Bash
	curl -XPOST http://api.sensu.example.com:4567/check/request -d '{"check":"aggregate_apt_check"}'
	
我添加了一个Cron job每天早上定时调用该命令。这样每天早上一到办公室就可以及时获知所有服务器是否需要更新。

整个工具就基本完成了。剩下的内容就是写一个Chef的Recipe，把工具部署到所有的服务器上。

###总结
这就是我的第一个Sensu项目。学习一门编程语言或一个工具最好的方法就是用它来做一个项目。的确，通过这个项目让我对Sensu的功能和特性有了比较清楚的了解。

整个安全更新监控工具的实现描述得很简单，但是从立项到投入实际应用还是用了我一个月的时间，后期还花费了一些时间在修复Bug上。因为很多工具都是初次使用，包括第一次接触Sensu，第一次使用Ruby做项目，第一次使用Chef，实现的过程中边学边做，还是走了不少弯路。

本文里只列出大致的框架，有一些代码没有贴出，贴出的代码也非完全准确。但是思路和意思已经都展现清楚了。

更加详细的内容可以参阅[Sensu文档](http://sensuapp.org/docs/0.16/overview)。

[^Instance]: 「实例」（Instance）这个说法听上去非常别扭，若无特别说明下文中「服务器」即指AWS实例。