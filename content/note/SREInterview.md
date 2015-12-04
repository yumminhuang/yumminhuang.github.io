+++
date = "2015-12-03T23:35:42-05:00"
title = "Site Reliability Engineer Interview"
tags        = ["Python", "Interview"]
categories  = ["Miscellaneous"]
+++
Recently, I had a phone interview for a position of Site Reliability Engineer. They asked me four questions in 60 minutes. I was asked to writing code on [collabedit](http://collabedit.com/)
Because Site Reliability Team of that company uses Python and I also prefer to Python, so all solutions are written in Python.

<!--more-->

#### Question 1

It is a kind of [FizzBuzz](https://en.wikipedia.org/wiki/Fizz_buzz) problem.

This is a quite easy coding task that can be completed in 5 minutes. There are some [solutions](http://codereview.stackexchange.com/questions/9751/ultra-beginner-python-fizzbuzz-am-i-missing-something) online.

#### Question 2

Parse `/var/log/syslog` and extract values.

```
Dec  3 00:02:54 Mac Google Chrome Helper[69194]: Couldn't set selectedTextBackgroundColor from default ()
Dec  3 00:03:05 Mac Safari[68992]: KeychainGetICDPStatus: keychain: -25300
Dec  3 00:03:05 Mac Safari[68992]: KeychainGetICDPStatus: status: off
Dec  3 00:03:06 Mac com.apple.xpc.launchd[1] (com.apple.WebKit.Networking.AC8ED90D-0AC0-4666-B213-8BE93DE51E8C[68993]): Service exited with abnormal code: 1
Dec  3 00:03:08 Mac WindowServer[68664]: CGXGetConnectionProperty: Invalid connection 20367
Dec  3 00:03:08 Mac garcon[68729]: host connection <NSXPCConnection: 0x7fc9d8f1eda0> connection from pid 68708 invalidated
Dec  3 00:03:08 Mac WindowServer[68664]: CGXGetConnectionProperty: Invalid connection 20367
```

Write a script which parses /var/log/messages and generates a CSV with two columns: minute, number_of_messages in sorted time order.

```
minute,number_of_messages
Dec  3 00:02,1
Dec  3 00:03,6
```

Extract the program name from the field between the hostname and the log message and output those values in columns.

```
minute,number_of_messages,Google Chrome Helper,Safari,com.apple.xpc.launchd,WindowServer,garcon
Dec  3 00:02,1,0,0,0,0
Dec  3 00:03,0,2,1,2,1
```

I think the key part of this problem is *regular expression*. For the first task, I used the following regular expression:

```
^(.*? \d+ \d+\:\d+).*
```

* Then use [`re.match(regexp, line).groups()`](https://docs.python.org/2/library/re.html#re.MatchObject.groups) to extract `minute`.
* [collections.Counter](https://docs.python.org/2/library/collections.html#collections.Counter) can count objects.

For the second task, the regular expression is:

```
^(.*? \d+ \d+\:\d+)\:\d+ .*? (.*?)\: .*
```

The second task also has to find all programs in the log file.

#### Question 3

Assume there is a REST API available at `http://www.employee.com/api` for accessing employee information The employee information endpoint is `/employee/<id>` Each employee record you retrieve will be a JSON object with the following keys:

* `name`  refers to a String that contains the employee's first and last name
* `title` refers to a String that contains the employee's job title
* `reports` refers to an Array of Strings containing the IDs of the employee's direct reports

Write a function that will take an employee ID and print out the entire hierarchy of employees under that employee. For example, suppose that Flynn Mackie's employee id is 'A123456789' and his only direct reports are Wesley Thomas and Nina Chiswick. If you provide 'A123456789' as input to your function, you will see the sample output below.

```
Flynn Mackie - Senior VP of Engineering
  Wesley Thomas - VP of Design
    Randall Cosmo - Director of Design
      Brenda Plager - Senior Designer
  Nina Chiswick - VP of Engineering
    Tommy Quinn - Director of Engineering
      Jake Farmer - Frontend Manager
        Liam Freeman - Junior Code Monkey
      Sheila Dunbar - Backend Manager
        Peter Young - Senior Code Cowboy
```

Main ideas for my solution:

* [requests](http://docs.python-requests.org/en/latest/) is a useful module for calling RESTful APIs.
* [`json.loads()`](https://docs.python.org/2/library/json.html#json.loads) is required to parse JSON.
* Recursion is the easiest way to handle such DFS algorithm.
* Be careful about indentation of each line. Adding a `depth` parameter in function. Here is the basic idea:

```
def foo(id, depth=0):
    ...
    if depth == 0:
        # print without indentation
    else:
        # print with a prefix ' ' * 2 * depth
    ...
    foo(employee, depth + 1)
```
