Title: Jenkins简介
Date: 2015-06-02 17:10
Modified: 2015-06-02 17:10
Category: DevOps
Tags: DevOps

在[之前的一篇文章中](http://yumminhuang.github.io/ji-yu-jenkinsde-pythondai-ma-ji-cheng-zheng-he.html)，曾经提及过Jenkins。在本次实习中，Jenkins是我每天都要使用的工具。在频繁的使用过程当中：通过实际工作感受了「持续集成」的概念（关于持续集成的概念，此处按下不表，待有时间的时候再详细总结。）；逐渐熟悉了Jenkins的使用，并且体会到其带来的方便。因此，希望总结一下Jenkins的使用。

然而Jenkins不通过具体的案例难以体会其方便之处，网上相关使用说明之类的文章又颇多，所以本文仅谈个人使用中的体会，并非学习Jenkins使用的教程。

---
### Jenkins是什么

[Jenkins](http://jenkins-ci.org/)是一个用Java编写的开源的<ruby>持续<rt>Continuous</rt></ruby> <ruby>集成<rt>Integration</rt></ruby>工具。

Jenkins是用Java开发的（界面和Eclipse一样，带着一股浓浓的SWT的味道，好在界面并不太影响使用。），对Java程序开发有天然的良好支持，如JUnit/TestNG测试，Ant等Java开发中常用的工具都包含在Jenkins里。当然，Jenkins也可以通过插件来实现其它语言的开发。

### Jenkins的特性
在使用的过程中，我体会比较深刻的特性有：

* **项目易于配置**

在Jenkins当中，我们可以新建Job。在Job里，可以设置添加<ruby>构建脚本<rt>Build Script</rt></ruby>。构建脚本支持Bash、Ant、Makefile；Job的参数、<ruby>元<rt>Meta</rt></ruby>数据可以作为环境变量在脚本里直接使用，因此设置起来非常方便。

* **种类繁多的插件**（这点也和Eclipse也颇为相似）

Jenkins的开发者社区非常活跃，[第三方插件](https://wiki.jenkins-ci.org/display/JENKINS/Plugins)很多，从而可以帮助我们实现很多常用的功能。
比如，Hipchat插件可以在Job运行结束后把结果发送到Hipchat的聊天室里；Cobertura插件可以显示测试覆盖率的数据。

### Jenkins的使用场景
在我们公司，Jenkins主要被用来用于：

* **<ruby>构建<rt>Build</rt></ruby>、<ruby>测试<rt>Test</rt></ruby>、<ruby>部署<rt>Deploy</rt></ruby>代码**；

我们可以通过一个Job实现以下流程：

1. 使用Git插件，从代码库下载任一版本或分支的源代码；
2. 编译代码；
3. 运行测试。

或者是：

1. 启动若干个EC2实例；
2. 将任一版本的代码部署到新建的实例上。

所有的这些流程在Jenkins里，都只需要设置几个简单的参数（如分支的名称，或者是实例的个数），再点击运行按钮就可以了。

* **自动化一些复杂的流程，如数据库的迁移、备份，系统更新的安装等等**

有一些常用，但是流程很复杂的过程，可以在Jenkins里通过Job来完成。