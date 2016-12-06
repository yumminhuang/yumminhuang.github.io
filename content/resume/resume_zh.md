+++
date = "2015-11-13T10:19:57-05:00"
title = "简历"
+++

#### 教育经历

**东北大学**，波士顿，美国， 2013 年 9 月 —— 2015 年 12 月

计算机科学硕士学位

GPA: 3.88/4.00

**课程项目**

* 软件工程项目
	* 使用 Jersey 和 Tomcat 构建 JAX-RS 网站：WHAM (What Happened Around Me)；
	* 根据 Scrum 方法指导项目开发进程；
	* 利用 JIRA 进行项目管理和缺陷追踪，Confluence 管理文档。
* MapReduce 项目
	* 统计、分析旧金山市犯罪记录（超过 180 万条记录），并使用朴素贝叶斯算法预测一个案件的犯罪类型；
	* 编写 Hadoop 和 Spark 程序，在 AWS EMR 上运行。
*  计算机网络项目
	* *Row Sockets* ---  使用 Python 的 Row Sockets 构建 TCP/IP 栈；
	* *Roll Your Own CDN* --- 基于 AWS EC2 搭建一个简易的「内容分发网络（[Content Delivery Network](https://en.wikipedia.org/wiki/Content_delivery_network)）」。
* 数据库项目
	* 使用 JPA 为 MySQL 搭建 [OData](http://www.odata.org/) 服务（一款用来访问数据库的 RESTful API）。

**暨南大学**，广州，2009 年 9 月 —— 2013 年 7 月

软件工程工学学士学位

GPA: 84.6/100

**毕业论文**

* 《可视化的 Java 多线程程序错误定位工具》
	* 一个动态的错误定位工具,用来定位 Java 多线程程序当作的并发错误；
	* 使用 [Soot](https://sable.github.io/soot/) 分析 Java 字节码,进行插装。

----
#### 职业经历

**乐视致新**，北京，2016 年 7 月至今

IT 运维工程师

* 管理 Gerrit 集群，托管近 1TB 代码库，为超过 300 名研发人员提供服务；
* 搭建 ELK 框架，收集 Gerrit 集群日志，提供日志分析和决策支持；
* 为 Gerrit 集群编写 Ansible Playbook，实现自动化 Gerrit 部署、配置更新。

**BitSight**，剑桥，美国，2015 年 1 月 —— 8 月

实习运维工程师

* 为 Ubuntu 集群设计并构建了一套安全补丁管理系统：使用 Sensu 报告可安装补丁，利用 Jenkins 一键安装补丁；
* 改进公司持续集成框架：从 Jenkins 获取测试结果，将测试结果生成总结报告并发送到 BitBucket Pull Request 页面；
* 使用 Jenkins 和 Fabric 调用 Django API，创建了一个自动化工作流备份和还原 MySQL 测试数据库；
* 改进了一些开源项目（包括 [automated-ebs-snapshots](https://github.com/skymill/automated-ebs-snapshots), [BitBucket-api](https://github.com/CBitLabs/BitBucket-api), [sensu-community-plugins](https://github.com/sensu/sensu-community-plugins) 等）；
* 部署并对比几款日志管理系统（ELK, Logentries, Sumologic）使用 Chef 部署，创建控制面板和常用搜索。

**Locately**，波士顿，美国， 2014 年 7 月 —— 8 月

实习后端软件工程师

* 实现 AWS 的 *Auto Scaling* 功能，根据 CPU 使用率动态增减服务器，帮助公司每年节省运营成本 $3000；
* 开发 Apache access log 监视器，将 EC2 实例上收集的数据发送到 AWS CloudWatch，用来监控服务器性能；
* 重写测试代码,使得 API 测试可以并行运行,从而使测试速度提高 17%。

**Aston University**，伯明翰，英国，2012 年 3 月 —— 4月

实习软件开发

* 开发了一款名为 *Scenario Capture* 的 Eclipse 插件，可以在图形界面下操作，并自动生成 JUnit 测试代码；
* 使用 JUnit 测试代码。

----
#### 专业技能
**语言**:
Python, Java, Ruby, Shell, Racket

**工具**:
Ansible, Chef, Docker, Git, Gerrit, Jenkins, Jira, SQL, UML

**框架**:
ELK, Django, Hadoop

**方法**:
Agile, Scrum
