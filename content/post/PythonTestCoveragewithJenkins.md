+++
title       = "基于 Jenkins 的 Python 代码集成整合"
categories  = ["DevOps"]
tags        = ["DevOps", "CI", "Jenkins"]
date        = "2015-04-17"
+++

实习中最近做了一个多月的项目是将代码测试覆盖率整合到公司持续整合（Continuous Integration）的流程当中。
<!--more-->

> This project uses Java and XML. How it could be good?
>
>  ——组里的同事如此评价本项目

本文介绍该项目的大致流程，共分为两部分：

1. 介绍 *Automated python unit testing, code coverage and code quality analysis with Jenkins*（[part1](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code.html), [part2](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code_20.html), [part3](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code_27.html)）中使用 Jenkins 实现自动化测试、得到代码覆盖率和代码质量的方法。
2. 简要介绍我们如何在这篇文章的基础上把代码覆盖率整合到公司的 Bitbucket 代码库当中。

### 基于 Jenkins 的 Python 自动化测试工具

使用到的 Python 模块：

* [coverage](http://nedbatchelder.com/code/coverage/)：用来生成代码覆盖率的数据；
* [nose](https://nose.readthedocs.org/en/latest/): 用来运行单元测试；
* [pylint](http://www.pylint.org)：用来得到 Python 代码质量的数据。

使用到的 Jenkins 插件：

* [Cobertura plugin](https://wiki.jenkins-ci.org/display/JENKINS/Cobertura+Plugin)：用来显示代码覆盖率；
* [GIT plugin](https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin)：用来获取最新的代码；
* [Violations plugin](https://wiki.jenkins-ci.org/display/JENKINS/Violations)：用来显示 pylint 的结果。

安装需要的 Jenkins 插件之后，在 Jenkins 当中新建一个作业（Job）接下来进行设置。

#### 从哪里得到代码

如下图所以，在 Jenkins 的 **Source Code Management** 当中可以添加 Git Repository。

![SCM](http://2.bp.blogspot.com/-hDwb_sbJZHk/T5lzDbCT76I/AAAAAAAAADg/adELp3TAeV8/s1600/Source+code.png)

Jenkins 同样支持 subversion 等 CVS 工具。

#### 什么时候运行作业

在 Jenkins 中可以将 **Build Triggers** 设置为 **Poll SCM** 对代码库进行轮询。如下图，**Schedule** 设为 `* * * * *`（含义和 Cron 一样）表示每分钟检查一次代码库，看是否有更新。如果代码库有更新的话则运行 **Build**。

![Poll SCM](http://3.bp.blogspot.com/-DewpmzsyWZo/T5lzXqPVOlI/AAAAAAAAADo/OA2Fxd1YTzY/s1600/Build+triggers.png)

当然，也可以使用 [Git Hook](http://git-scm.com/book/zh/v2/Customizing-Git-Git-Hooks)，从而避免轮询消耗过多的资源。

#### 运行什么

添加一段 **Build Script**:

```shell
PYTHONPATH=''
nosetests --with-xunit --all-modules --traverse-namespace --with-coverage --cover-package=project1 --cover-inclusive
python -m coverage xml --include=project1*
pylint -f parseable -d I0011,R0801 project1 | tee pylint.out
```

这段 Shell 脚本中的三个命令：

1. `nosetests` 命令运行单元测试；
2. 运行 `coverage`，将覆盖率数据输出为 xml 文件；
3. 运行 `pylint` 得到代码的质量数据。

具体参数的含义可以参阅原文的第一、第二部分。

#### 显示结果

上一步的 Build Script 有三个输出文件：

1. `nosetests.xml`
2. `coverage.xml`
3. `pylint.out`

接着，在 Jenkins 当中，在 **Publish JUnit test result report** 添加 `nosetests.xml` 显示单元测试的结果。在 Cobertura 插件 **Publish Cobertura Coverage Report** 里添加 `coverage.xml` 显示测试代码覆盖率。在 **Report Violations** 里添加 `pylint.out` 显示代码质量报告。

最终，运行一次作业之后，Jenkins 将可以得到下图显示的测试报告。

![Jenkins Output](http://4.bp.blogspot.com/-f_YtJcTOQ64/T5qnlOiE35I/AAAAAAAAAF8/l5Nl_YvRSuM/s1600/jenkins+after+logout+added.png)

### 持续整合！

我们持续整合的大致流程是这样的。在代码库中有一个 Master 分支，开发人员添加新功能，修复 Bug 都需要在新建的分支里进行。每新建一个合并到到 Master 的 Pull Request 时，Jenkins 可以自动运行测试。测试通过则在 Bitbucket 的 Pull Request 页面里添加一个的评论表示可以合并，否则会添加一个否决的评论。这个项目的目标就是再添加一个关于测试覆盖率的评论。

我们按照 *Automated python unit testing, code coverage and code quality analysis with Jenkins* 一文的思路实现了测试覆盖率的部分，区别是我们的代码库里包括 Java 和 Python 两种语言的代码，需要同时处理两份数据。经过一段时间的攻关之后，我们终于可以得到代码覆盖的数据。

相较于测试覆盖率的具体数值，我们更关心覆盖率的变化值。我们希望知道合并一个分支之后，测试覆盖率是增加了还是减少了。因此，现在我们需要得到测试覆盖率的变化值（Coverage diff）。

没想到 Python 连这种冷僻的使用场景都有第三方的库支持，还不只一个。我们使用的是 [Pycobertura](https://github.com/SurveyMonkey/pycobertura)。

Pycobertura 可以直接比较两个 Cobertura 格式的 xml 文件，从而得到覆盖率的变化值。

```python
from pycobertura import Cobertura
from pycobertura import TextReporterDelta

coverage1 = Cobertura('coverage1.xml')
coverage2 = Cobertura('coverage2.xml')
delta = TextReporterDelta(coverage1, coverage2)
delta.generate()
```

于是，我创建了一个 Fabric Task，调用 Pycobertura 分析测试生成的 xml 文件和 Master branch 的 xml 文件。在 Jenkins 里添加一段 **Post build script** 来运行 Fabric，这样 Build 完成之后就可以运行 Fabric 程序得到类似下面的输出结果：

```
Coverage Diff for Java code:
No coverage diff can be found.
Coverage Diff for Python code:
Name          Stmts    Miss    Cover
------------  -------  ------  --------
dummy/dummy   -        -2      +50.00%
dummy/dummy2  +2       -       +100.00%
TOTAL         +2       -2      +50.00%
```

最后剩下的就是把之前一步的结果以评论的形式发布到 Bitbucket 里。这里，我们又添加了一个 Fabric 的 Task，通过调用 Bitbucket 的 API 把得到的结果发布到 Pull Request 的页面里。

### 参考文献

1. [Automated python unit testing, code coverage and code quality analysis with Jenkins - part 3](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code_27.html)
