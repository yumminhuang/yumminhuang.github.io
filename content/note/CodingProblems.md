+++
date = "2015-12-18T16:53:33-05:00"
title = "Two Coding Problems"
tags        = ["Python", "Interview"]
categories  = ["Miscellaneous"]
+++

Two coding problems I encountered in a recent interview.

### Problem 1

> Problem: Print a binary tree row-by-row, from top to bottom.

> Example:

```
Input: Binary tree
  3
 / \
1   4
 \   \
  2   5
  
Output: 3, 1, 4, 2, 5
```

**Solution**

```python
class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def traverse(rootnode):
    # The list to save all visited nodes
    visited = list()

    # BFS
    thislevel = [rootnode]
    while thislevel:
        nextlevel = list()
        for n in thislevel:
            visited.append(n.value)
            if n.left:
                nextlevel.append(n.left)
            if n.right:
                nextlevel.append(n.right)

        thislevel = nextlevel
    # Print
    print(', '.join(map(str, visited)))
```

Output for the given example

```python
t = Node(3, Node(1, right=Node(2)), Node(4, right=Node(5)))
traverse(t)
```


### Problem 2

> Problem: Write a function to add two numbers represented as arrays of digits.

> Example: [1, 2, 3] + [3, 2, 1] = [4, 4, 4] => 123 + 321 = 444

The given example is confusing. There are two difficulties:

1. carry digit when adding two digits, e.g. `[1, 2, 3] + [9, 8, 7]`;
2. input two arrays of different size, e.g. `[1, 2, 3] + [4, 3, 2, 1]`

Although and the interviewer didn't mention those points, I thought I should consider them. Otherwise, the problem can be easily solved by a loop or one line code of python
`[x + y for x, y in zip(lst1, lst2)]`.

Similar problem solved by C++: [Add two numbers represented by linked lists](http://www.geeksforgeeks.org/sum-of-two-linked-lists/).

**Solution**

```python
def add(lst1, lst2):
    ret = list()
    # minimum size
    length = min(len(lst1), len(lst2))

    carry = 0
    # From left to right
    for i in range(-1, -(length + 1), -1):
        ret.append((carry + lst1[i] + lst2[i]) % 10)
        carry = (carry + lst1[i] + lst2[i]) / 10

    # Adding extra digits
    if len(lst1) > length:
        for n in lst1[len(lst1) - length - 1::-1]:
            ret.append((carry + n) % 10)
            carry = (carry + n) / 10

    if len(lst2) > length:
        for n in lst2[len(lst2) - length - 1::-1]:
            ret.append((carry + n) % 10)
            carry = (carry + n) / 10

    if carry > 0:
        ret.append(carry)

    # Reverse result list
    return ret[::-1]
```

**Follow Up Problem**

> How to modify your code if input is a list of arrays instead of two arrays?

```python
def add_lists(*lists):
    return reduce(lambda x, y: add(x, y), lists)
```

