+++
date = "2015-12-18T10:27:50-05:00"
title = "如何选择开源项目的证书"
categories  = ["Miscellaneous"]
+++

世界上的开源许可证有很多。除了常见的 [Apache](http://www.apache.org/licenses/LICENSE-2.0)，[BSD](http://en.wikipedia.org/wiki/BSD_licenses)， [MIT](https://en.wikipedia.org/wiki/MIT_License) 等之外，还有一些奇特的证书，比如 [WTFPL (Do What the Fuck You Want to Public License)](http://www.wtfpl.net/)。Github 还专门做了一个[网站](http://choosealicense.com/) 介绍了常见的开源证书。

然而开源证书虽多，却很少有人会仔细研究证书上的法律条文，搞清楚它们的区别。我最近看了 Github 的网站，又看了一些网上的文章，稍稍研究了几个常用证书的区别，以及如何为开源项目选择证书。故撰此文以供参考。

<!--more-->

如果开源的内容不是代码，可以选择[知识共享许可协议](http://creativecommons.org/)。针对是否需要署名使用，是否可以商用等问题，知识共享许可协议有许多不同的版本，可以访问[链接](http://creativecommons.org/choose/)来选择一个合适的知识共享许可协议。

关于开源的代码，可以依次回答以下的问题来确定开源证书。

1. 是否允许他人闭源使用你的代码？
  *	 是：继续回答问题2
  *	 否：[GPL](http://www.gnu.org/licenses/gpl-3.0.en.html) (The GNU General Public License)[^1]
2. 如果他人修改了你的代码，是否需要了解修改？
  * 是：[EPL](https://www.eclipse.org/legal/epl-v10.html) (Eclipse Public License)
  * 否：继续回答问题3
3. 是否打算为代码注册专利？
   * 是：Apache License
   * 否：继续回答问题4
4. 他人发布时是否需要显式地附带你的证书？
   * 是：BSD License
   * 否：MIT License

我没有研究各个开源证书的条文，以上内容也只是我的个人理解，难免有错误之处。所以，为一个正式的项目选择开源证书之前，最好还是仔细确认一遍。

[^1]: GPL [不同的版本之间也有区别](https://opensource.org/licenses/gpl-license)，其中细微的差别对我来说实在难以理解。总之，GPL 是一个 [copyleft](http://www.gnu.org/licenses/copyleft.html) 的协议。