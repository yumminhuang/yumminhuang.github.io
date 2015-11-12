+++
title       = "在 VPS 搭建 VPN 服务器"
tags        = ["DevOps", "Linux"]
categories  = ["DevOps"]
date        = "2015-03-16"
+++

## 简介
> 从来就没有什么救世主
>
> 也不靠神仙皇帝
>
> 要创造人类的幸福
>
> 全靠我们自己

为了在 [GFW](http://zh.wikipedia.org/wiki/防火长城) 的封锁之下进行正常的上网活动，可以使用 [VPN](http://zh.wikipedia.org/wiki/虛擬私人網路)。为什么有各种各样的 VPN 服务提供商还要自己搭建 VPN 呢？有以下几方面的考虑：

1. 安全性：你很难保证一些 VPN 提供商不会盗取你的敏感信息，自己搭建 VPN 则可以避免这个问题；
2. 稳定：「道高一尺，魔高一丈」，现在很多 VPN 提供商都是打一枪换一个地方，难以保证稳定的连接；
3. 价格：自己搭建 VPN，一个月的费用大概在 $5 左右。

## 具体步骤
#### 注册一个 VPS 账号
注册任意一家 VPS 服务提供商的账号。此步可能需要一张双币信用卡。
至于选择哪家服务商，此处按下不表。下文将以 **DigitalOcean** 为例描述具体步骤。
#### 新建一个 Droplet
我新建的 Droplet 是最低配置，具体配置包括：

* 512MB RAM
* 20GB SSD
* 2TB 流量

地理位置选的是最近的。

操作系统开始选择的是 Ubuntu14.04，后来用的是 Ubuntu12.04（版本应该没有影响）。

没有选择多余的设置。

点击新建按钮会收到一份包含登陆密码的邮件。接着就可以通过ssh进行登录了。

其余添加用户、Linux 基本设置等内容在此不再赘述。
#### 安装PPTP

```
sudo apt-get install pptpd
```
	
#### 配置
* 配置 IP 地址

编辑 `/etc/pptpd.conf`，添加以下内容(基本上默认设置已经完成或者被注释了)：

```
option /etc/ppp/pptpd-options
localip 192.168.0.1
remoteip 192.168.0.100-200
```
这里是 PPTP 服务器的 IP 地址设为 `192.178.0.1` ，把 PPTP 客户端的 IP 地址设置为 `192.168.0.100` 到 `192.168.0.200` 的区间内。当然你也可以自己的需要和喜欢进行相应的设置

* 配置客户端 DNS

编辑 `/etc/ppp/pptpd-options` ，添加 DNS 地址。这里我选择的是[Google Public DNS](https://developers.google.com/speed/public-dns/)。

```
ms-dns 8.8.8.8
ms-dns 8.8.4.4
```

* 添加用户

编辑 `/etc/ppp/chap-secrets`，添加账号和密码。其中第一列为账户名，第二列为密码。

```
# client    server  secret          IP addresses
test		pptpd   1234            *
```

* 设置 IP 转发

打开 IPv4 转发，并重新载入设置。

```
sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/g' /etc/sysctl.conf
sudo sysctl -p
```

为 PPTP 连接设置 NAT，否则不能访问别的网站。

```
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```
	
也可以直接编辑 `/etc/rc.local`，在 `exit 0` 之前添加以上内容。

* 重启 PPTP

```
sudo service pptpd restart
```

这样PPTP服务器就搭建完毕了，可以「科学上网」了！

> 没有什么能够阻挡
>
> 你对自由地向往

---
### Trouble Shooting
* PPTP connection error: GRE: Bad checksum from pppd

第一次设置完毕之后尝试连接 VPN，发现连接失败。重新设置之后依然没有解决，以至于让我怀疑是 Ubuntu14.04 的问题。我新建了一个 Droplet，更换成 Ubuntu12.04 之后还是同样的问题。接着尝试用`netstat`检查，发现连接已经建立，但是因为某种原因被断开了。检查`/var/log/syslog`，发现了以下内容：

```
Mar 21 16:54:23 Server pptpd[1808]: GRE: Bad checksum from pppd.
Mar 21 16:54:53 Server pppd[1809]: LCP: timeout sending Config-Requests
Mar 21 16:54:53 Server pppd[1809]: Connection terminated.
Mar 21 16:54:53 Server pppd[1809]: Modem hangup
Mar 21 16:54:53 Server pppd[1809]: Exit.
Mar 21 16:54:53 Server pptpd[1808]: GRE: read(fd=6,buffer=80504c0,len=8196) from PTY failed: status = -1 error = Input/output error, usually caused by unexpected termination of pppd, check option syntax and pppd logs
Mar 21 16:54:53 Server pptpd[1808]: CTRL: PTY read or GRE write failed (pty,gre)=(6,7)
Mar 21 16:54:53 Server pptpd[1808]: CTRL: Reaping child PPP[1809]
Mar 21 16:54:53 Server pptpd[1808]: CTRL: Client 50.164.202.163 control connection finished
```
上网搜索，在 StackOverflow 上找到了[答案](http://stackoverflow.com/a/21347817)。至此，终于定位到无法连接的根本原因 —— 是路由器不支持 `PPTP Passthrough` 功能。我上路由器厂商的官网一看，果然发现了去年12月发布了一个固件更新用来修复VPN连接的问题。

---

### VPS服务提供商选择
* Amazon Web Service
    * 大公司，服务稳定，无须担心亚马逊被封（因为亚马逊非常熟悉中国的那一套，[有图](http://zhuanlan.zhihu.com/riobard/19910423)为证）；
	* 高度可定制；
	* 丰富的文档、社区支持；
	* 按小时收费，新注册用户可以免费使用一年；
	* 可以将虚拟机部署在东京，理论上访问速度更快。
	* 缺点：**设置复杂**
* DigitalOcean
	* 可选择包月套餐，性价比更高；
	* 控制台界面清爽、简洁。
* Linode 似乎很多人在用，一个老牌的VPS提供商，但是我没有用过。

如果你选择 DigitalOcean，点击[链接](https://www.digitalocean.com/?refcode=ba81ee4b40b2)注册，可以获得10美元的优惠。

---
### 参考文献：
1. [How To Setup Your Own VPN With PPTP -- DigitalOcean.com](https://www.digitalocean.com/community/tutorials/how-to-setup-your-own-vpn-with-pptp)
2. [Configure PPTP VPN on Ubuntu](https://riobard.com/2011/11/12/pptp-vpn-on-ubuntu/)
