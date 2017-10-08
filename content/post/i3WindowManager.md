+++
title       = "i3 窗口管理器简介"
tags        = ["Linux"]
categories  = ["Linux"]
date        = "2015-03-29"
+++

在[内核恐慌](http://kernelpanic.fm)第九期[「程序员的理想工作环境」](http://ipn.li/kernelpanic/9/)中，主持人 Rio 和吴涛谈及了 Tiling Window Manager，并且介绍了 [Awesome 窗口管理器](http://awesome.naquadah.org/)和 i3 窗口管理器。节目中两位主持人的对描述 Tiling Window Manager 恰好符合我的需求，并且实习所用的笔记本操作系统刚好是 Ubuntu，所以听完节目后，我也试着在办公电脑上安装了 Awesome。然而体验并不愉快，我为此在微博上[吐槽](http://www.weibo.com/2622511625/C1N9FgPr5)。之后在 Rio 的建议下，我安装了 i3，果然非常好用。这里，结合我两个月的使用体验，简单地介绍一下 i3 窗口管理器，并且推荐大家使用。
<!--more-->

## 平铺式窗口管理器

窗口管理器（Window manager）是在图形用户界面的视窗系统中，用来控制窗口位置与外观的系统软件。

窗口管理器主要有两种[^type]：

1. 堆叠式窗口管理器（Stacking Window Manager）；
1. 平铺式窗口管理器（Tiling Window Manager）。

在[堆叠式管理器](http://en.wikipedia.org/wiki/Stacking_window_manager)（也称作悬浮式窗口管理器，Floating Window Manager）中，不同窗口可以像桌子上随意摆放的白纸一样相互重叠。常见的窗口管理器多为堆叠式，如 Windows 的 Explorer，Mac OS X 的 Finder，以及 Ubuntu 的 Unity 等等。

[平铺式](http://en.wikipedia.org/wiki/Tiling_window_manager)（或直译为瓦片式）窗口管理器，其中的窗口不能够重叠，而是像瓦片一样挨个摆放。常用的平铺式管理器有 Awesome 和i3。

根据我个人的使用体验，平铺式窗口管理器（主要指的是 i3 ）有以下几个优点：

1. 简单轻巧；
2. 多依赖键盘操作，较少使用鼠标；
3. 高度可定制化；
4. 稳定。

具体来说。平铺式窗口管理器没有绚丽的界面和复杂的功能，可以让人更加专注于正在做的事情。同时，平铺式管理器非常精简，如 i3 的安装包只有 900 多 KB，相应地，消耗的资源也更少。平铺式管理器多依赖键盘操作，较少使用鼠标，配合应用程序的快捷键，基本上可以避免鼠标操作，从而提升工作效率。平铺式管理器不仅可以实现边框颜色之类的常规设置，还可以根据用户的需求，修改桌面、窗口等。最后，因为平铺式管理器非常精简，较之堆叠式管理器也更加稳定。至少在我使用的两个月里还没有出现过崩溃的情况。

我觉得在工作环境中需要同时打开多个窗口，又拥有多台显示器的时候[^monitor]，就像下图中那样，平铺式窗口管理器最能发挥作用。

![i3 配合多屏幕](http://awesome.naquadah.org/images/6mon.small.png)

比如我工作时有一台 13 寸的笔记本和一台 27 寸的外接显示器。时刻保持打开的窗口包括公司内交流用的即时聊天软件，邮件客户端，编辑器，浏览器和多个终端窗口。使用 i3 之后，我的两个显示器基本是这样分配的：

* 笔记本显示器左右分割为两栏，分别显示聊天软件和邮件客户端；
* 外接显示器分为两栏；
  * 第一栏又分两列，分别给编辑器和调试、运行用的终端；
  * 第二栏也分两列，分别给浏览器和其它用的终端（常用的是远程登录、监控系统）。

虽然需要同时打开了很多软件，但是因为窗口是平铺的，每次要切换软件时，只需要将屏幕的焦点切换到相应的窗口即可，而不需要像堆叠式管理器那样在凌乱的桌面上找到要用的窗口。

## i3 窗口管理器的基本操作
### 按键
i3 窗口管理器操作中非常不同的是需要设置一个 `MOD` 键，用来执行指令。
我用的是一般 PC 键盘上没什么用的 Windows 键 (Mod4)。为此，我特意把[办公室的键盘](http://instagram.com/p/0N9WKCBDZt/)的 Windows 键换成了醒目的红色。

具体按键对应的指令参见下面两幅图：

<img src="http://i3wm.org/docs/keyboard-layer1.png" width="600"/>

按下 `MOD` 键时对应的指令

<img src="http://i3wm.org/docs/keyboard-layer2.png" width="600"/>

按下 `MOD+Shift` 键时对应的指令

### 容器
i3 窗口管理器有一个很重要的概念就是容器（Container）。每个容器内可以存放一个应用程序的窗口。一个桌面（或者说 Workspace）就是一个容器。容器可以嵌套形成树型的结构，所以我们可以将容器水平或者垂直地分割成多个容器，从而充分利用桌面的空间。详细解释请参阅[文档](http://i3wm.org/docs/userguide.html#_tree)。

### 常用的指令
* `MOD + H, J, K, L`：移动屏幕焦点；
* `MOD + Shift + H, J, K, L`：移动容器；
* `MOD + V`：垂直分割容器；
* `MOD + H`：水平分割容器；
* `MOD + D`：打开应用程序启动器Dmenu；
* `MOD + Enter`：打开终端。

## i3窗口管理器的安装和配置
### 安装
以Ubuntu为例。首先添加i3到源列表。

```shell
echo "deb http://debian.sur5r.net/i3/ $(lsb_release -c -s) universe" >> /etc/apt/sources.list
```

然后运行以下指令进行安装。

```shell
apt-get update
apt-get --allow-unauthenticated install sur5r-keyring
apt-get install i3
```

### 配置
我之所以放弃 Awesome 的一个很重要的原因就是它的配置过于复杂。诚然，Awesome 的效果要比 i3 酷炫很多，但是设置需要用到 Lua 脚本。很多功能还需要通过安装插件来完成。相反，i3 只需要两个设置文件，而且用的是非常易读的语法。

配置文件包括两部分，`~/.config/i3/config` 和 `~/.config/i3status/config`，分别用来设置 i3 窗口管理器和状态栏[^config]。

在这里贴一下我自己的[ i3 配置文件](https://github.com/yumminhuang/dotfiles/blob/master/files/i3_config)和[ i3 状态栏的配置文件](https://github.com/yumminhuang/dotfiles/blob/master/files/i3status_config)，基本上每条设置都做了注释，以供读者参考。

想要了解更加具体的配置方法，可以参阅 i3 的[官方文档](http://i3wm.org/docs/)。

[^type]: 事实上，一些窗口管理器，如 Awesome 和 i3，支持堆叠式和平铺式两种窗口管理器的形式。这样的窗口管理器被称作[「动态式窗口管理器」](http://en.wikipedia.org/wiki/Dynamic_window_manager)。因为本文主要介绍 i3 作为平铺的特性，故将其划为平铺式窗口管理器。

[^monitor]: 多台显示器支持可以使用 `xrandr` 指令。

[^config]: 为了方便编辑，我把配置文件放在 `~` 目录下，也可以放在其它目录下面。配置文件路径具体的读取顺序请参阅[关于 i3 设置的文档](http://i3wm.org/docs/userguide.html#configuring)和[关于状态栏设置的文档](http://i3wm.org/i3status/manpage.html#_options)。
