+++
categories = ["Miscellaneous"]
date = "2015-11-13T09:38:53-05:00"
tags = ["Hugo", "Go"]
title = "将博客由 Pelican 迁移到 Hugo"
+++

前两天花了一些时间研究了一下 [Hugo 的文档](https://gohugo.io/overview/introduction/)，并且把博客从 [Pelican](http://blog.getpelican.com/) 迁移到 Hugo。
<!--more-->

Pelican 是一个优秀的静态博客生成器。当初选用 Pelican 的主要是因为它是用 Python 开发的，而我又对 Python 比较熟悉。而且 Pelican 有很多由第三方开发者制作的插件提供了更多的功能。但是长期使用的过程中还是有一些小小的麻烦。当初，我想给博客里的中文文章添加[「汉字标准格式」](https://css.hanzi.co/) 这个框架，需要向模版里添加一段引入 CSS 和 JS 代码。但是 Pelican 的模版不易更改，我需要为了修改一两行 HTML 文件 Fork 之前的模版，方法既不优雅，维护成本又很高。另外，Pelican 的模版似乎是全局性的，所有的页面都使用相同的模版。

后来，无意之间发现 Hugo 在配置和文件结构上和 Pelican 有很大的不同，大大地提高了可配置性，可以解决上述的两个问题。此外，第一次看到  [Hugo 官网](https://gohugo.io/)的首页的时候，看上去非常漂亮，令人印象深刻。

使用 `hugo new site SITE_DIR` 新建一个 Hugo 之后，生成以下路径：

```
.
├── archetypes/
├── config.toml
├── content/
├── data/
├── layouts/
└── static/
```

`config.toml` 用来存放设置。`content/` 里存放的是文章，`data/` 用来存放一些数据。 `static/` 里是需要引入的 CSS 或图片之类的文件。如果需要添加现场的主题模版，可以添加到 `themes/` 里并在`config.toml` 里设置。这些内容和 Pelican、Jekyll 一样，有的也可以望文生义，猜到大致的作用。

加下来着重介绍的是 `layouts/`，这里定义了博客的模版，是自定义 Hugo 最重要的部分。和 Pelican 有很大不同的地方是，Hugo 可以自定义文章的类型（ Type ）。不同的类型可以使用不同的模版。比如，除了第三方主题提供的文章类型，我还想为中文文章新建一个类型 `zhpost`。只需要在 `layouts/` 下新建一个 `zhpost/`。接着，我可以设置中文文章的样式，只需新建一个 `single.html` 就可以了。我也因此可以在`layouts/zhpost/single.html` 里引入「汉字标准格式」的 CSS 和 JS。另外，对于第三方主题的模版不满意的话还可以按照相同的路径重写一个。Hugo 会优先读取根目录下 `layouts/` 里的设置。具体来说，`layouts/post/single.html` 可以覆盖 `themes/THEME/layouts/post/single.html`。这样我就可以很容易的替换不满意的模版了。

Hugo 的可定制性非常高，从 404 页面，到文章列表的页面都可以修改，而且可以做到不同类型的文章使用不一样的样式。具体的配置需要参考[第三方的主题](http://themes.gohugo.io/)的设置和 Hugo 的文档。

值得一提的是，Go 的模版语言可读性很高，几乎不需要花额外的时间学习。我对照着别人开发的主题照葫芦画瓢就完成了模版的定义和修改。

`archetypes/`，用来存放定义的「原型」。原型的作用是自动添加文字的元数据。比如，我想每次创建 `post` 类文章的时候都自动添加元数据，只需要在 `archetypes/` 里添加一个 `post.md`，并加入以下内容：

```
+++
title = "my new post"
date = "2015-01-12T19:20:04-07:00"
tags = ["x", "y"]
categories = ["x", "y"]
+++
```
这样每次运行 `hugo new post/ARTICLE.md` 的时候都可以自动添加上面的元数据。

Hugo 另外的一个优点是生成博客的速度非常快，生成一个网页的速度可以达到毫秒级别。如果博客的内容很多，Hugo 要比 Pelican、Jekyll 等由动态语言写成的博客生成器有很大的优势。

当然，Hugo 也有不足。比如，Hugo 默认是不支持代码高亮的，需要额外设置。此外，在 Pelican 里，可以通过 [cjk-auto-spacing](https://github.com/yuex/cjk-auto-spacing) 插件来自动在英文单词和汉字之间插入空格，这对于有大量中英文混排的技术笔记来说非常方便。但是，目前我还没有找到 Hugo 有类似的解决方法，暂时只能在写文章的时候手工加入空格。

刚开始使用 Hugo，有一些诸如 Taxonomies，Section 之类的功能还没有仔细研究。这篇文章也是草草完成，不慎严谨，俟后完善。