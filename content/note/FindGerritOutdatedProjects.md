+++
title = "Find Gerrit Outdated Projects"
date = "2016-12-03T14:09:23+08:00"
tags        = ["Gerrit"]
categories  = ["Gerrit"]

+++

Recently, I had a job to clean up our Gerrit server.
First of all, I have to find projects which we can deprecate and remove them.

Here is the solution how I found outdated Gerrit Projects.

Gerrit Administrator can use [gerrit gsql command](https://gerrit-review.googlesource.com/Documentation/cmd-gsql.html)
 to access Gerrit backend database and query outdated projects. 
The below SQL can find **projects whose lastest changes were updated 180 days ago**.

<script src="https://gist.github.com/yumminhuang/b30e3650d26f0958384b68ab405f6932.js"></script>

The results could be the candidates of deprecating projects.