+++
categories = ["Programming"]
date = "2015-06-27"
tags = ["ruby"]
title = "Ruby 中的猴子补丁"
+++

之前一段时间，在实习工作当中，使用到了一种有些独特的编程技巧；而且该技巧又有一个奇特的名称：「猴子补丁」。
<!--more-->

## 猴子补丁

猴子补丁（[Monkey Patch](https://en.wikipedia.org/wiki/Monkey_patch)）是一种特殊的编程技巧。Monkey patch 可以用来在运行时动态地修改（扩展）类或模块。我们可以通过添加 Monkey Patch 来修改不满足自己需求的第三方库，也可以添加 Monkey Patch 零时修改代码中的错误。

### 词源
Monkey patch 最早被称作 Guerrilla patch，形容这种补丁像游击队员一样狡猾。后来因为发音相似，被称为 Gorilla patch。因为大猩猩不够可爱，后改称为 Monkey patch。

### 使用场景
以我的理解，Monkey patch 有两种使用场景：

1. 紧急的安全性补丁，即 Hotfix；
2. 修改或扩展库中的属性和方法。

## 在 Ruby 中使用 Monkey Patch
我当时遇到的场景是这样的：

我司使用第三方库 [fog](http://fog.io/) 进行 EC2 的操作。创建实例等很多命令都需要设置实例类型这个参数。在 fog 里，EC2 的所有类型都定义在 `fog/aws/models/compute/flavors.rb` 的 `FLAVORS` 数组里。如果设置的类型不在 `FLAVORS` 数组里，fog 都会视作是无效的参数而报错。

后来，亚马逊发布了新的实例类型 `D2`。虽然 Ruby 的第三方社区非常活跃，但是 fog 的开发社区还是没有及时添加 D2 到 `flavors.rb` 里；而我司的工作又迫切需要使用 D2 类型的实例。

背景交待完毕，接下来看看有什么样的解决方法。

**方法一**：我们可以向 fog 提交一个 Pull Request 来添加新类型。

但是这个方法行不通。我们使用的 [knife-ec2](https://github.com/chef/knife-ec2) 对 fog 的版本依赖必须是 `1.25.*`，但是 fog 已经更新到了 `1.31.0`，而且 fog 从 `1.27.0` 开始结构上有很大的变化。显然，我们不可能再等 knife-ec2 升级支持新版本的 fog，所以我们提交 Pull Request 更新 fog 不能解决问题。

**方法二**：手动更新旧版 fog
既然不能使用最新版的 fog，我们可以手动编辑 `1.25` 版的 fog，再打包成 Gem 使用。这个方法比前一个方法更容易操作，但是带来的问题时不易于维护。为了一个极小的改动，把自己的代码加入到第三方库中总是让人觉得不够「干净」。

最后，在同事的指点下，我采用了第三种方法，即 **Monkey Patch**。我在我司的 Ruby 项目里添加了一个文件 `lib/PROJECT_NAME/monkey_patches/flavors.rb`，接着在文件中添加以下代码来修改 `fog/aws/models/compute/flavors`：

```
require 'fog/aws/models/compute/flavors'

class Object

  def redef_without_warning(const, value)
    mod = self.is_a?(Module) ? self : self.class
    mod.send(:remove_const, const) if mod.const_defined?(const)
    mod.const_set(const, value)
  end
end

module Fog
  module Compute
    class AWS
      NEW_FLAVORS = FLAVORS + [
        {
          :id => "d2.xlarge",
          ...
        },
        {
          :id => "d2.2xlarge",
          ...
        },
        {
          :id => "d2.4xlarge",
          ...
        },
        {
          :id => "d2.8xlarge",
          ...
        }
      ]

      redef_without_warning :FLAVORS, NEW_FLAVORS

    end
  end
end
```

## 总结
通过在自己的代码中添加一个 Monkey patch，我们成功地实现了向 fog 中动态添加新实例类型。我司终于可以使用 fog 创建 D2 类型的机器了；而且这个方法改动的代码量最小，也更加容易维护。

Monkey Patch 并非是完美的解决方法，它会引入一些[陷阱](https://en.wikipedia.org/wiki/Monkey_patch#Pitfalls)。所以这个技巧在软件工程领域还有一些争议。不过，我还是觉得 Monkey Patch 是一个不错的零时性解决方法。

---
### 参考文章

* [3 Ways to Monkey-patch Without Making a Mess](http://www.justinweiss.com/blog/2015/01/20/3-ways-to-monkey-patch-without-making-a-mess/)
* [Monkeypatching is Destroying Ruby](http://devblog.avdi.org/2008/02/23/why-monkeypatching-is-destroying-ruby/)
