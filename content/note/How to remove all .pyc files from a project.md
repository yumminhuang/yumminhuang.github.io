+++
title 		= "How to remove all .pyc files from a project?"
tags 		= ["Linux", "Shell"]
categories	= ["Linux"]
date		= "2014-07-31"
+++

I am a paranoid guy. I like to delete all "useless" files. Today, I want to clean up my project repository. There are lots of `.pyc` files. And I found this command, which is very convenient to batch delete files in a directory.
<!--more-->

```
find . -name "*.pyc" -exec rm -rf {} \;
```
OR

```
find . -name "*.pyc" -delete;
```

I can also delete all `*.class` files for Java project and `.o` files for C project in this way.

```
find . -name "*.class" -exec rm -rf {} \;
find . -name "*.o" -exec rm -rf {} \;
```

Or I can delete all files whose name starts with 'test'.

```
find . -name "test*" -exec rm -rf {} \;
```

**Reference:**

* [How do I remove all .pyc files from a project?](http://stackoverflow.com/questions/785519/how-do-i-remove-all-pyc-files-from-a-project)
