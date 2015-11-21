+++
title 		= "Execute a Command in the Background on Remote Server using SSH"
tags 		= ["Shell"]
categories	= ["Linux"]
date		= "2014-05-04"
+++

In a project, I have to deploy a simple server program on several remote servers. So I wrote a shell script to deploy and run the program using `scp` and `ssh`.

Since there are several remote servers, I have to run the server program in the background on all remote machines.

At first, I simply add the ampersand (&) at the end of the command like this:

```
ssh user@host "cd /some/directory; ./program &"
```

But my script just hangs after it runs first remote server. After googling this problem, I found this command to solve it.

```
ssh -n -f user@host "sh -c 'cd /some/directory; nohup ./program > /dev/null 2>&1 &'"
```

This command is quiet complicated. It need to use [`nohup`](http://en.wikipedia.org/wiki/Nohup) as well as output redirection. But it works and solved my problem.

### Reference

1. [Stackoverflow](http://stackoverflow.com/questions/29142/getting-ssh-to-execute-a-command-in-the-background-on-target-machine)