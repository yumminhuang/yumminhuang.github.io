Title: Travis CI
Date: 2015-06-20 21:10
Category: DevOps
Tags: DevOps, CI

本文将主要介绍如何使用[Travis CI](https://travis-ci.org)托管Github上的开源项目，从而实现自动化测试、部署。同时，还将介绍使用[Coveralls](https://coveralls.io/)来监测测试覆盖率。

## Travis CI

Travis CI是一款Web端的<ruby>持续<rt>Continuous</rt></ruby> <ruby>集成<rt>Integration</rt></ruby>工具。

Travis CI采用[「Freemium」](https://en.wikipedia.org/wiki/Freemium)的模式：对Github上的开源项目免费，付费的话则可以托管私有项目。Github上很多知名的开源项目都适用Travis CI来进行自动化测试。

和Jenkins相比，Travis CI要轻量很多。但是已经足以完成简单的自动化测试、部署。

## Coveralls

Coveralls用来显示代码覆盖率，从而可以让程序员及时了解代码质量。

Coveralls和Travis CI一样，仅对Github上的开源项目免费。Coveralls支持包括Travis CI、Jenkins在内的绝大多数持续集成工具。

## 样例

接下来以Python项目为例，说明如何使用Travis CI和Coveralls[^src]。

### 依赖管理和虚拟环境

我喜欢为每个项目新建一个<ruby>virtualenv<rt>虚拟环境</rt></ruby>，这样可以确保每个项目的开发环境相互独立，避免发生冲突。[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)是一个让人方便使用virtualenv的小工具。它把如新建virtualenv、切换virtualenv等常用的操作都封装成了简单的指令。

我一般会在项目中添加一个`requirements.txt`，里面列出项目所依赖的Pip库。这样在virtualenv中，直接运行

	:::bash
	pip install -r requirements.txt
	
就可以安装所有的库。

### 单元测试和测试覆盖

对于Python项目，我喜欢使用[nose](https://nose.readthedocs.org/en/latest/)来进行单元测试。此外，我还会使用[coverage.py](http://nedbatchelder.com/code/coverage/)来测量代码的测试覆盖率。

nose对coverage.py的支持非常好，可以在`nosetests`命令后添加一系列选项来生成覆盖率。

	:::bash
	nosetests --with-coverage

就可以直接得到测试覆盖率的数据。

详细的使用方法可以参见[nose的官方文档](https://nose.readthedocs.org/en/latest/)和[coverage.py的官方文档](http://nedbatchelder.com/code/coverage/cmd.html)。

### 持续集成
在Github上新建项目之后，在Travis CI的页面上开启该项目。（新建的项目可能不会及时出现在Travis CI页面上，需要手动同步一下Github的项目。）接着，在Github项目里添加Travis CI的配置文件`.travis.yml`。Travis CI的配置使用的是非常易读的YAML文件。

	:::yaml
	language: python
	python:
	    - 2.6
	    - 2.7
	# command to install dependencies
	install:
	    - pip install -r requirements.txt
	    - pip install coveralls
	# command to run tests
	script:
	    nosetests --cover-package=project --with-coverage
	# coveralls
	after_success:
	    coveralls

同样地，也需要在Coveralls上开启相应的项目。

这样，Github的代码库在每次收到`Push`和`Pull Request`的时候，Travis CI都会按照配置文件上的步骤自动运行测试（或者部署，本样例只有测试。），并且把测试覆盖率的数据发布到Coveralls。

详细的配置说明可以参见[Travis CI的官方文档](http://docs.travis-ci.com/)和[Coveralls的官方文档](https://coveralls.zendesk.com/hc/en-us)。

### 其它
Travis CI和Coveralls都可以生成<ruby>图章<rt>Badge</rt></ruby>，用来显示<ruby>构建<rt>Build</rt></ruby>的结果，或者测试覆盖率。

[![Build Status](https://travis-ci.org/yumminhuang/turbo-octo-meme.svg?branch=master)](https://travis-ci.org/yumminhuang/turbo-octo-meme)

可以将这些图章（如果已经发布到PyPi，还可以加上版本号、下载量的图章。）放在项目的*README*文件里。

[^src]: 详细代码可参见[turbo-octo-meme](https://github.com/yumminhuang/turbo-octo-meme)。