+++
categories = ["DevOps"]
date = "2016-03-05T17:29:12-05:00"
tags = ["DevOps", "CI"]
title = "持续集成交付部署"

+++

最近看了一篇文章 [*The Product Managers’ Guide to Continuous Delivery and DevOps*](http://www.mindtheproduct.com/2016/02/what-the-hell-are-ci-cd-and-devops-a-cheatsheet-for-the-rest-of-us/)。
文中对「持续集成（ *Continuous Integration* ）」、「持续交付（ *Continuous Delivery* ）」和「持续部署（ *Continuous Deployment* ）」这三个概念有很详细的解释。这里借用文中的插图，说一下我对这三个概念的理解。

<!--more-->

### 持续集成

<img src="http://cdn02.mindtheproduct.com/wp-content/uploads/2015/12/409-images-for-snap-blog-postedit_image1.png" alt="Continuous Integration" style="width: 500px;"/>

持续集成强调开发人员提交了新代码之后，立刻进行构建、（单元）测试、打包等步骤。根据反馈的测试结果，我们可以知道新代码和原有代码能否正确地集成在一起。

### 持续交付

<img src="http://cdn02.mindtheproduct.com/wp-content/uploads/2015/12/409-images-for-snap-blog-postedit_image4-manual.png" alt="Continuous Delivery" style="width: 500px;"/>

持续交付在持续集成的基础上，将集成后的代码部署到更贴近真实运行环境的「类生产环境（ *production-like environments* ）」中。比如，我们完成单元测试后，可以把代码部署到连接数据库的 Staging 环境中进行更多的测试。如果代码没有问题，接下来就可以继续**手动部署**到生产环境中。

### 持续部署

<img src="http://cdn02.mindtheproduct.com/wp-content/uploads/2015/12/409-images-for-snap-blog-postedit_image3-auto.png" alt="Continuous Deployment" style="width: 500px;"/>

持续部署则是在持续交付的基础上，把部署到生产环境的过程自动化。

我个人觉得持续集成、持续交付、持续部署非常值得推广。开发过程中最怕集成时遇到问题导致返工，而持续集成、持续交付、持续部署恰恰可以做到问题早发现早解决，从而可以避免这样的麻烦。另外，持续集成、持续交付、持续部署的流程高度依赖自动化工具，所以这种开发方法也可以大大提高开发人员的工作效率。