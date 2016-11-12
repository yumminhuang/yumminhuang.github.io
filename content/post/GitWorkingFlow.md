+++
categories = ["DevOps"]
date = "2016-02-13T16:36:21-05:00"
tags = ["git", "CI"]
title = "Git 工作流"
+++

Git 可能是每个开发者最常用的工具之一。Git 让开发团队更加方便地进行版本控制和多人协作。但是如果开发团队没有约定如何使用 Git 工作，很可能会导致工作变得一团糟。其中最大的问题是同时存在太多的开发中的分支，每个分支都包含了部分修改。最终开放团队很难弄清楚哪一个分支应该继续开发，或者把它发布成产品。

正如编程过程中变量命名需要一套标准的命名规则（[Naming convention](https://en.wikipedia.org/wiki/Naming_convention_(programming))）一样，开发团队在使用 Git 的时候，也需要一套标准的工作流，从而确保高效的开发、测试和部署。

关于 Git 的工作流，业界已经有了很多讨论。

<!--more-->

### Git flow
[git-flow](http://nvie.com/posts/a-successful-git-branching-model/) 最早在2010年提出。用下面这幅图可以概括 git-flow 的主要内容。

<img src="http://nvie.com/img/git-model@2x.png" alt="git-flow" style="width: 500px;"/>

git-flow 包含一个 *master* 分支、一个 *develop* 分支，*release* 分支、*hotfix* 分支和若干 *feature* 分支。开发工作在 `develop` 进行，然后提交到 `release` ，最后合并到 `master`。但是 git-flow 太复杂了，需要维护很多分支，开发时还要不停切换分支。所以，到了后来有一些[文章](http://insights.thoughtworkers.org/gitflow-consider-harmful/)就对 git-flow 提出了质疑。

### Github flow
Github 针对 git-flow 的不足，并且充分利用 Pull Request 功能，提出了一套更为简单的工作流 —— [Github flow](http://scottchacon.com/2011/08/31/github-flow.html)。 Github flow 简化了分支：只有一个可部署的 `master` 分支；新添加的代码（不区分 feature、bug-fix）都放在基于 master 创建的新分支里；分支的名称应当能描述出问题（Issue），例如 `new-oauth2-scopes`。Github flow 同时还强调持续交付（[Continuous delivery](http://martinfowler.com/bliki/ContinuousDelivery.html)）和使用当时 Github 新推出的 Pull Request 进行代码审查（[Code review](https://en.wikipedia.org/wiki/Code_review)）。经过几年的发展，Github flow 基本上已经成为业内的标准：几乎所有的代码托管网站、使用 Git 的 SaaS、Git 软件都有基于 branch 的 Pull Request 功能。

### Gitlab flow
但是 Github flow 仍有不足和值得改进的地方，所以 Gitlab 提出了 [Gitlab flow](https://about.gitlab.com/2014/09/29/gitlab-flow/)。Github flow 强调持续交付，合并到 `master` 的代码要立刻部署到线上。Gitlab 指出这种模式并非适用于所有的开放环境。比如有的软件可能隔几个月，甚至几年才会发布新版本。因此（如下图所示），在这些例子里，创建一个 *production* 或 *release* 分支来管理发布的代码是有必要的。

![gitlab-flow](https://about.gitlab.com/images/git_flow/production_branch.png)

另外，Gitlab flow 还强调代码的任何修改都应该开始于一个目标明确的Issue。因此，为一个 Issue 创建新分支时，这个分支的名字应该以 Issue 的编号开始，比如 `15-require-a-password-to-change-it`。Commit 的信息或 Merge Request 的描述里应关联相关的 Issue，如`fixes #14` 或 `closes #67`，这样合并到 `master` 的时候可以自动关闭相应的 Issue。

### Git 工作流的需求
在实际开发的过程中，有各种各样的需要。鉴于诸如 [Scrum](https://en.wikipedia.org/wiki/Scrum_\(software_development\)) 之类的敏捷开发方法已经被业界采用，再结合我以前的经验，我觉得 Git 工作流应当结合以下功能：

1. 缺陷追踪（[Issue tracking](https://en.wikipedia.org/wiki/Issue_tracking_system)）；
2. 代码审查；
3. 持续集成（[Continuous integration](http://martinfowler.com/articles/continuousIntegration.html)）。

首先，缺陷追踪是非常有必要的。Issue 列表不仅可以帮助整个团队及时了解当前存在的问题和未来需要增加的功能，也可以用来帮助在每个 sprint 前制定 [product backlog](https://en.wikipedia.org/wiki/Scrum_\(software_development\)#Product_backlog)。而且现在市面上大部分的缺陷追踪系统，比如 [JIRA](https://www.atlassian.com/software/jira)、[Github Issue](https://guides.github.com/features/issues/)， 都整合了 Git，可以通过 Issue 编号相互链接。

代码审查的重要性不必赘述，在开发过程中，团队成员之间互相检查对于保证代码质量是非常关键的。

持续集成同样有助于提高代码质量。快速持续的合并到 `master` 可以确保团队在最新、最准确的代码上工作，避免了不必要的冲突。通过使用诸如 [Jenkins](https://yumminhuang.github.io/post/Jenkins/)、[Travis CI](https://yumminhuang.github.io/post/TravisCI/) 之类的持续集成工具，可以自动测试每一个 Pull Request，从而保证 `master` 当中代码的正确性。

另外，Git 工作流还需要满足的要求：

1. 代码隔离；
2. 便于版本回溯；
3. 可以在尽可能多的平台上使用。

使用 Git 分支最主要的目的就是实现代码隔离，即：每个人能够各自独立工作，互不干扰；未完成和出错的代码不会混在准备发布的代码里。

使用 Git 还应该能够快速地版本回溯。一旦当前发布的代码出现问题，要能够立刻回溯到上一个可发布版本。

最后，应该能在尽可能多的平台上，无论是 Github、BitBucket 这样的 SaaS，还是自己使用 Gitlab 搭建的服务器，实践这个工作流。最好可以让 GUI 和 CLI 都能够完成整个工作流。

### 改进的 Git 工作流
基于 Github flow，并加入 Gitlab flow 的一些优点，我设计了一个改进的 Git 工作流：

1. `master` 时刻保持「可交付」的状态；
2. 根据 Issue 列表，基于 `master` 创建新分支，并采用描述性的命名方法；
3. 定期 push commits 到服务器；
4. 在需要反馈、帮助，或解决了一个 issue 时，创建 Pull Request，同时添加 Reviewer；
5. 使用持续集成技术运行自动化测试，保证测试通过，并进行代码审查；
6. 合并 Pull Request 到 `master` 分支；
7. 为发布的版本添加 tag。

**`master` 时刻保持「可交付」的状态**

这条应该作为工作流中最基本的准则严格执行。作为 Git 里默认的分支，我们应当保证 `master` 里的代码随时可以发布。这样，一旦代码出现了问题，我们可以回到 `master` 中之前的版本。

软件测试的一个基本原则就是无法保证代码中没有 bug。所以，我们只能确保代码满足需求说明文档，是可以发布、部署的状态。

**根据 Issue 列表，基于 `master` 创建新分支，并采用描述性的命名方法**

如前一条准则所述，`master` 里的代码可以认为是正确的，我们可以基于 `master` 放心地创建新分支。

虽然没有必要单独创建 `hotfix` 之类的分支，我认为还是有必要在命名时，通过添加前缀 `feature/`、`fix/`、`hotfix/`，对每条分支的内容加以区分。比如，增加一个新特性时，可以给分支命名为 `feature/oauth2-login`，修复一个 bug 时，可以给分支命名为`fix/memory-leak`。这样既简化了分支管理，避免一个分支存在太长时间，也方便快速了解一个分支的作用。

**定期 push commits 到服务器**

定期 push commits 一来可以把代码备份到服务器，也可以让整个团队了解项目的进展。Push 的频率取决于具体的情况。开发一个新功能可能需要花费很长的时间，可以相应地降低 push 的频率；而修复一个 bug，则可能较为紧急，应尽可能快地 push 到服务器上。

另外，明确的 Commit message 有助于团队协作、回忆开发过程。关于如何写 Commit message，可以参考这篇 [Commit message 和 Change log 编写指南](http://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html)。

**在需要反馈、帮助，或解决了一个 issue 时，创建 Pull Request，同时添加 Reviewer**

现在几乎所有的代码托管平台都支持 Pull Request 功能，使用 Pull Request 可以方便地进行团队内的代码审查。有的工具，比如 Bitbucket，可以直接添加 Reviewer。其它工具，比如 Github，也可以通过 [@ 功能](https://github.com/blog/1121-introducing-team-mentions)来提醒团队成员进行审查。

并非在完成全部更改时才可以创建 Pull Request，在遇到问题需要团队帮助或反馈时，同样可以创建 Pull Request，并在 Pull Request 的描述里简述当前的进度。通过和 Reviewer 讨论可以更快地解决问题。这样做也方便让团队其他成员了解项目的进展。

在 Pull Request 的描述里，可以链接对应的 Issue，方便索引。Github 等也可以在分支被合并的时候[自动关闭对应的 Issue](https://github.com/blog/1506-closing-issues-via-pull-requests)。

**使用持续集成技术运行自动化测试，保证测试通过，并进行代码审查**

自动化测试在此不再赘述。我们应当保证所有测试用例都被通过，并且得到所有 Reviewer 的许可。

**合并 Pull Request 到 `master`**

在测试通过，并且所有 Reviewer 都同意之后，就可以把分支里的代码合并到 `matser`。

大部分工具都可以在 Pull Request 的图形化页面里直接合并。如果使用命令行，应当使用 `git merge --no-ff feature/xxx` 来进行合并。如下图所示，使用 `--no-ff` 参数后，会执行正常合并，并在 `master` 上生成一个新节点，而非「快进式合并（fast-forward merge）」。

<img src="http://image.beekka.com/blog/201207/bg2012070506.png" alt="--no-ff merge" style="height: 300px;"/>

这样做可以保证版本演进的清晰。

合并到 `master` 之后，创建的分支应当删除。

**为发布的版本添加 tag**

需要发布或者部署时，从 `master` 里选择最新的版本。可以给该版本添加 tag，比如 `v1.0beta`、`2.3.2` 等。

有时候针对不同的演示环境（Staging），可能有必要维护单独的 *production* 分支，可以从 `master` [cherry-pick](https://git-scm.com/docs/git-cherry-pick) 指定的版本到 `production`。

---

这是一个基于 Github flow 和 Gitlab flow 的，又根据我自己的经验改进的 Git 工作流，可能还有一些值得改进的地方。也许未来随着开发经验的增加，我会尝试完善这整个流程。
