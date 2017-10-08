+++
title 		= "Yelp Interview Problem"
tags 		= ["Python", "Interview"]
categories	= ["Miscellaneous"]
date		= "2014-11-18"
+++

Today, I had a skype interview with Yelp.
<!--more-->

### Interview

At first, the interviewer asked me about my experience. Then, he asked me some technical questions, such as
> * What will cause access a website slowly?
> * Difference between thread and process,
> * What is deadlock?
> * What's your favorite programming language? And why?

The last part of the interview is a coding question. The interviewer sent me a link of [CoderPad](http://coderpad.io) and asked me to write code on it.

### Coding Problem Description
The problem is not very difficult. Write a function to **find the longest prefix of a list of string.** For example,

`['abc', 'abcde', 'abxyz'] => 'ab'`

### Solutions

During the interview, I spent some time to finish it due to the pressure from time and the interviewer. He asked me to review the code after I finished by walking through each step in my function. This process did help me complete the task, cause I found some bugs in my code and fixed them in time. He also asked me the time complexity of my solution. Here is my solution.

```python
def longest_prefix(lst):
    tmp = list()
    for i in range(min(map(lambda x: len(x), lst))):
        for idx, s in enumerate(lst):
            if idx == 0:
                tmp.append(s[i])
            if s[i] != tmp[-1]:
                return str(tmp[:-1])
    return str(tmp)
```

Obviously, my solution is not good. My function does not work when input is a empty list. The return of my function is a list instead of a string. It would be better if modify my solution like this way:

```python
def longest_prefix(lst):
    if not lst:
        return ''
    prefix = []
    for i in range(min(map(lambda x: len(x), lst))):
        for idx, item in enumerate(lst):
            if idx == 0:
                prefix.append(item[i])
            if item[i] != prefix[-1]:
                return ''.join((prefix[:-1]))
    return ''.join((prefix))
```

### Better solutions
After the interview, I searched this problem and tried to find some better solutions. I want to code like a [*pythonista*](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html). Here are [some good solutions](http://stackoverflow.com/questions/6718196/python-determine-prefix-from-a-set-of-similar-strings).

```python
def commonprefix(m):
    """
    Return the longest prefix of all list elements.
    """
    if not m: return ''
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1
```

Some guy even found a way to solve this problem using only one line python code.

```python
>>> lst = ['abc', 'abcde', 'abxyz']
>>> from itertools import takewhile, izip
>>> ''.join(c[0] for c in takewhile(lambda x: all(x[0] == y for y in x), izip(*lst)))
'ab'
```
