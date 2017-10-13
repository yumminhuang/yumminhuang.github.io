+++
date = "2017-09-10T11:31:51+08:00"
categories = ["Miscellaneous"]
tags = ["Gerrit"]
title = "搭建分布式 Gerrit 集群"
isCJKLanguage = true
+++

[Gerrit](https://www.gerritcodereview.com) 是由 Google为了管理 Android 项目而开发的，一款免费、开源的代码审查软件。Gerrit 使用 Git 作为底层版本控制系统，提供了代码审查、权限管理等功能。

本文将会简单介绍如何搭建分布式 Gerrit 集群，即搭建由一个可以读写的 Gerrit Master 和若干个只读的 Gerrit Slave 组成的 Gerrit 集群。Gerrit Slave 可以实时同步 Gerrit Master 的数据，保证代码的一致性。

<!--more-->

分布式的架构可以用来：

1. 分流下载：下载代码可以从只读的 Slave 下载，从而减轻 Master 的负载。如果 Slave 和 Master 在不同地区，还可以起到加速下载的功效。
2. 灾备切换：如果 Master 出现故障，可以切换到 Slave 继续工作。

## 分布式 Gerrit 架构

Gerrit 里的数据主要是两部分：

1. Git 代码库，用来存储代码；
2. 数据库[^database]，用来存储代码提交（Change），用户、分组权限等信息。

因此在实现分布式 Gerrit 时，对应两部分数据，我们需要通过：

1. [PostgreSQL](https://www.postgresql.org) [Streaming Replication](https://wiki.postgresql.org/wiki/Streaming_Replication)
2. [*Gerrit Replication* 插件](https://gerrit.googlesource.com/plugins/replication)

来实现 Gerrit Master 和 Gerrit Slave 之间的数据同步。

分布式 Gerrit 架构如下图所示。

```
+----------------------+                  +--------------------+
|                      |                  |                    |
|    Gerrit Master     |                  |    Gerrit Slave    |
|       Server         |                  |       Server       |
|                +-----+-----+            |                    |
|   +----------+ |  Gerrit   |            |     +----------+   |
|   |Repository| |Replication|  git push  |     |Repository|   |
|   |          +-+  Plugin   +----------------->+          |   |
|   +----------+ +-----+-----+            |     +----------+   |
|                      |                  |                    |
|   +--------------+   |                  |  +--------------+  |
|   |   PostgreSQL |   |  Replication     |  | PostgreSQL   |  |
|   |    PRIMARY   +------------------------>+ HOT-STANDBY  |  |
|   +--------------+   |                  |  +--------------+  |
+----------------------+                  +--------------------+
```

在 Gerrit Master 和 Slave 上都有一个相同的 Git 代码库（*Repository*），Gerrit Replication 插件可以用来将 Master 上收到的更新（新提交的 commit，`refs/meta` 分支下的变更或是创建的新代码库）同步到 Slave。

为了实现数据库的同步，需要将 PostgreSQL 运行在 [Hot Standby 模式](https://www.postgresql.org/docs/9.4/static/hot-standby.html)。 在 Gerrit Master 上运行的 PostgreSQL 是 *primary* ，可以进行读、写操作； 在 Gerrit Slave 上运行的 PostgreSQL 是 *stanby* ，可以和 *primary* 保持同步，可以接受客户端的连接，但只能进行读操作。如果 *primary* 故障了，整个系统可以迁移（ *fail over* ）到 *stanby* ，由 *stanby* 承担 *primary* 的角色。

## 分布式 Gerrit 配置

### 配置 Gerrit

对于安装和配置 Gerrit Master，分布式的搭建和单点的搭建并没有区别。

#### Gerrit Slave

安装和配置 Gerrit Slave 上的 Gerrit 的时候，需要注意在 `gerrit.config` 文件里的 `[container]` 下面添加 `slave = true` 。

```
[container]
    user = gerrit2
    javaHome = /usr/lib/jvm/java-7-oracle/jre
    javaOptions = -Xmx80g -Xms20g -Xmn2g
    slave = true
[database]
    type = postgresql
    database = reviewdb
    hostname = localhost
    username = gerrit2
...
```

这样 Gerrit 才会启动为 Slave。

### 配置 PostgreSQL 数据库

在 Master 上要配置 `/etc/postgresql/9.4/main/postgresql.conf`，打开 Hot Standby 功能。

```
...
wal_level = hot_standby
...
```

还需要在 `/etc/postgresql/9.4/main/pg_hba.conf` 添加  *stanby* 的 IP，确保 *stanby* 可以连接  *primary* 进行同步。

```
host   replication   all    POSTGRES.STANDBY.IP.ADDRESS/32       md5
```

在 Slave 上首先需要配置 `/etc/postgresql/9.4/main/postgresql.conf`，设置 PostgreSQL 运行为 *stanby* 。

```
...
hot_standby = on
...
```

接下来，添加 `/var/lib/postgresql/9.4/main/recovery.conf` 文件，配置  *primary*  信息。

```
standby_mode = on
primary_conninfo = 'host=POSTGRES.PRIMAY.IP.ADDRESS port=5432 user=replicator password=PASSWORD'
trigger_file = '/var/lib/postgresql/postgresql.trigger'
```

其中 `trigger_file` 被用来触发 *fail over* ，此时不需要创建。

配置完成后，在 *primary*  上运行命令将数据拷贝到 *standby* 。

```shell
rsync -av --exclude pg_xlog --exclude postgresql.conf data/* \
	POSTGRES.STANDBY.IP.ADDRESS:/var/lib/postgresql/data/
```

重启两端的 PostgreSQL 后，*primary* 和 *standby* 将保持同步。

关于 Hot Standby 的详细的说明，可以参见 Postgresql 的这篇[官方文档](https://wiki.postgresql.org/wiki/Hot_Standby)。

### 配置 Gerrit Replication

#### Gerrit Slave

首先需要在 Gerrit Slave 上配置 xinetd，用来提供 git daemon 服务。

```shell
$ sudo apt install xinetd
$ cat /etc/xinetd.d/git-daemon

# default: off
# description: The git server offers access to git repositories service git
service git
{
        disable = no
        type = UNLISTED
        port = 9418
        socket_type = stream
        wait = no
        env  = HOME=/home/gerrit2
        user = gerrit2
        server = /usr/bin/git
        only_from = gerrit-master.example.com
        log_type = SYSLOG daemon info
        server_args = daemon --inetd --syslog --export-all --enable=upload-pack --enable=receive-pack --base-path=/home/gerrit2/review_site/git --verbose
        log_on_success += USERID HOST DURATION EXIT
        log_on_failure += USERID HOST ATTEMPT
        cps = 150 10
}
$ sudo /etc/init.d/xinetd restart
```

重启 xinetd 之后，9418 端口将会开启，可以通过 `git://` 访问 Gerrit Slave 上的代码库。

#### Gerrit Master

在 Gerrit Master 上，首先需要安装 Gerrit Replication 插件，下载对应 Gerrit 版本的 Replication 插件 jar 文件，并添加到 `$REVIEW_SITE/plugin` 目录下。

接下来，添加 `$REVIEW_SITE/etc/replication.config` 文件，加上 Gerrit Slave 的配置

```
[remote "slave"]
  url = git://gerrit-slave.example.com/${name}.git
  mirror = true
  threads = 4
  adminUrl = ssh://gerrit-slave.example.com/home/gerrit2/review_site/git/${name}.git
```

注意，`adminUrl` 的路径要按照 Gerrit Slave 上代码库真实的存放路径设置。

这样，启动 Gerrit Master 之后，每次代码库有变更，Gerrit Replication 插件都会将变更通过 git 协议 Push 到 Slave 上。

通常，在启动 Gerrit Slave 之前，需要将代码库拷贝到 Slave 机器上，以缩短首次同步的时间。

---

分布式 Gerrit 搭建完成之后，我们可以添加 `.gitconfig` 文件来实现代码上传和下载分流。

```
[url "ssh://<username>@gerrit-slave.example.com:29418"]
    insteadOf = gerrit
    pushInsteadOf = ssh://<username>@gerrit-master.example.com:29418
```

这样，克隆代码库的时候使用命令

```shell
git clone gerrit:path/to/repo
```

可以从 Gerrit Slave 下载代码，而 `git push` 的时候会自动将代码 Push 到 Gerrit Master。

## 参考

1. [Setting Up Postgres Hot Standby](https://cloud.google.com/community/tutorials/setting-up-postgres-hot-standby#understanding-hot-standby)

[^database]: Gerrit 支持大部分主流的关系型数据库，具体的配置方法可以参见[建立数据库](https://gerrit-review.googlesource.com/Documentation/database-setup.html) 和[配置数据库](https://gerrit-review.googlesource.com/Documentation/config-gerrit.html#database)的官方文档。本文以 PostgreSQL 为例。
