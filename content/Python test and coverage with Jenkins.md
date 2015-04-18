Title: 基于Jenkins的Python代码集成整合
Date: 2015-04-17 21:40
Modified: 2015-04-17 21:40
Category: DevOps
Tags: DevOps, CI, Jenkins

实习中最近做了一个多月的项目是将代码测试覆盖率整合到公司持续整合（Continuous Integration）的流程当中。

> This project uses Java and XML. How it could be good?
>
>  ——组里的同事如此评价本项目

本文介绍该项目的大致流程，共分为两部分：

1. 介绍*Automated python unit testing, code coverage and code quality analysis with Jenkins*（[part1](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code.html), [part2](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code_20.html), [part3](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code_27.html)）中使用Jenkins实现自动化测试和得到代码覆盖率的方法。
2. 简要介绍我们如何在这篇文章的基础上把代码覆盖率整合到Bitbucket代码库当中。

### 基于Jenkins的Python自动化测试工具

使用到的Python模块：

* coverage：用来生成代码覆盖率的数据；
* nose: 用来运行单元测试；
* pylint：用来得到Python代码质量的数据。

使用到的Jenkins插件：

* [Cobertura plugin](https://wiki.jenkins-ci.org/display/JENKINS/Cobertura+Plugin)：用来显示代码覆盖率；
* [GIT plugin](https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin)：用来获取最新的代码；
* [Violations plugin](https://wiki.jenkins-ci.org/display/JENKINS/Violations)：用来显示pylint的结果。

安装需要的Jenkins插件之后，在Jenkins当中新建一个作业（Job）。

#### 从哪里得到代码

如下图所以，在Jenkins的**Source Code Management**当中可以添加Git Repository。

![SCM](http://2.bp.blogspot.com/-hDwb_sbJZHk/T5lzDbCT76I/AAAAAAAAADg/adELp3TAeV8/s1600/Source+code.png)

Jenkins同样支持subversion等CVS工具。

#### 什么时候运行作业

在Jenkins中可以将**Build Triggers**设置为**Poll SCM**对代码库进行轮询。如下图，**Schedule**设为`* * * * *`（含义和Cron一样）表示每分钟检查一次代码库，看是否有更新。如果代码库有更新的话则运行作业。

![Poll SCM](http://3.bp.blogspot.com/-DewpmzsyWZo/T5lzXqPVOlI/AAAAAAAAADo/OA2Fxd1YTzY/s1600/Build+triggers.png)

当然，也可以使用[Git Hook](http://git-scm.com/book/zh/v2/Customizing-Git-Git-Hooks)，从而避免轮询消耗过多的资源。

#### 运行什么

添加一段**Build Script**:

	:::Bash
	PYTHONPATH=''
	nosetests --with-xunit --all-modules --traverse-namespace --with-coverage --cover-package=project1 --cover-inclusive
	python -m coverage xml --include=project1*
	pylint -f parseable -d I0011,R0801 project1 | tee pylint.out

这段Shell脚本中的三个命令：

1. `nosetests`命令运行单元测试；
2. 运行`coverage`，将覆盖率数据输出为xml文件；
3. 运行`pylint`得到代码的质量数据。

具体参数的含义可以参阅原文的第一、第二部分。

#### 显示结果

上一步的Build Script有三个输出文件：

1. `nosetests.xml`
2. `coverage.xml`
3. `pylint.out`

接着，在Jenkins当中，在**Publish JUnit test result report**添加`nosetests.xml`显示单元测试的结果。在Cobertura插件**Publish Cobertura Coverage Report**里添加`coverage.xml`显示测试代码覆盖率。在**Report Violations**里添加`pylint.out`显示代码质量报告。

最终，运行一次作业之后，Jenkins将可以得到下图显示的测试报告。

![Jenkins Output](http://4.bp.blogspot.com/-f_YtJcTOQ64/T5qnlOiE35I/AAAAAAAAAF8/l5Nl_YvRSuM/s1600/jenkins+after+logout+added.png)

### 持续整合！

我们持续整合的大致流程是这样的。再代码库中有一个Master分支。开发人员添加新功能，修复Bug都需要在新建的分支里进行。每新建一个到Master的Pull Request时，Jenkins可以自动运行测试。测试通过则在Bitbucket的Pull Request页面里添加一个的评论表示可以合并，否则会添加一个否决的评论。这个项目的目标就是再添加一个关于测试覆盖率的评论。

我们按照*Automated python unit testing, code coverage and code quality analysis with Jenkins*一文的思路实现了测试覆盖率的部分，区别是我们的代码库里包括Java和Python两种语言的代码，需要同时处理两份数据。经过一段时间的攻关之后，我们终于可以得到代码覆盖的数据。

相较于测试覆盖率的具体数值，我们更关心覆盖率的变化值。我们希望知道合并一个分支之后，测试覆盖率是增加了还是减少了。因此，现在我们需要得到测试覆盖率的变化值（Coverage diff）。

没想到Python连这种冷僻的使用场景都有第三方的库支持，还不只一个。我们使用的是[Pycobertura](https://github.com/SurveyMonkey/pycobertura)

Pycobertura可以直接比较两个xml文件得到覆盖率的变化值

	:::Python
	from pycobertura import Cobertura
	from pycobertura import TextReporterDelta

	coverage1 = Cobertura('coverage1.xml')
	coverage2 = Cobertura('coverage2.xml')
	delta = TextReporterDelta(coverage1, coverage2)
	delta.generate()

于是，我创建了一个Fabric Task，调用Pycobertura分析测试生成的xml文件和Master branch的xml文件。在Jenkins里添加一段**Post build script**来运行Fabric，于是就可以得到如下的结果：

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

最后剩下的就是把之前一步的结果以评论的形式发布到Bitbucket里。这里，我们又添加了一个Fabric的Task，通过调用Bitbucket的API把得到的结果发布到Pull Request的页面里。

### 参考文献

1. [Automated python unit testing, code coverage and code quality analysis with Jenkins - part 3](http://bhfsteve.blogspot.com/2012/04/automated-python-unit-testing-code_27.html)