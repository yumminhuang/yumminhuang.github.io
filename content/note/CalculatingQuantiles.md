+++
date = "2015-12-03T21:12:18-05:00"
tags 		= ["Python", "Interview"]
categories	= ["Miscellaneous"]
title = "Calculating Quantiles"
+++

This problem is from my recent online coding test. I didn't solve it in the limited time cause I used a wrong way. When I realize that, I don't have enough time to fix it. I feel regretful for failing the test.
<!--more-->

## Problem
Find quantiles for a population of N values. These values are index 1, ..., N from lowest to highest. The K<sup>th</sup> Q-quantile of such population is determined by computing the index l<sub>k</sub> = N * k / Q and taking the value found at index l<sub>k</sub>. If l<sub>k</sub> is not a integer, then it is rounded to the next integer to get the index. For a given value of Q, there will be (Q-1) quantiles.

For example, for Q = 2 the 1<sup>st</sup> (and only) quantile of the population {3, 5, 6} is 5. Explanation: N = 3, Q = 2, k = 1, which means l<sub>1</sub> = ceiling(3 * 1 / 2) = 2. Value at index 2 is 5.

## Input format
The solution should read input from Standard Input in the following format:

```
Q
M
v1 c1
v2 c2
...
vn cn
```

Here Q is the Q-quantile, M is the number of v/c pairs. v<sub>i</sub> is a value in the population, and c<sub>i</sub> is its count. Values of v<sub>i</sub> are guaranteed to be distinct, but may not necessarily appear in order.

For example:

```
3
3
7 2
6 2
5 2
```

The population of number is `{7, 7, 6, 6, 5, 5}` and we need to calculate the two 3-quantiles of this population.

## Output format
Print out the values of all Q-quantiles to the Standard Output in ascending order, separated by newlines.

Sample output for the above example:

```
5
6
```

## Constraints
1. 1 ≤ N ≤ 10<sup>12</sup>
2. 2 ≤ Q. However, Q is not guaranteed to be less than N
3. 1 ≤ M ≤ 100000
4. 1 ≤ c<sub>i</sub>
5. v<sub>i</sub> and c<sub>i</sub> values are integers


## Solutions

At first, I chose a very naïve way to solve this problem. Read v/c pairs and create the whole list, then find all quantiles by their indexes. This is easy to understand and implement, but it will exceed
memory limit when population is large.

Then I realized I should avoid building a list. I should calculate all quantiles' indexes and retrieve values from v/c pairs. I believe the second idea is reasonable, However, in next 30 minutes, I spent too much time on considering data structure for saving pairs, sorting, loop through pairs. I didn't submit correct code in time.

After the online test, I completed it. Here is my final solutions

```
import math
import sys

# Read lines from stdin
lines = sys.stdin.readlines()

# Read Q and M
Q = int(lines[0].rstrip())
M = int(lines[1].rstrip())

# Read population and save numbers and their counts in a list as format
# [[v1, c1], [v2, c2], ...]
input = list()
for line in lines[2:]:
    v, c = line.rstrip().split()
    input.append([int(v), int(c)])

# Sort by number
array = sorted(input, key=lambda pair: pair[0])

# Re-organize array by changing count in each pair to value's last index
total = 0
for pair in array:
    total += pair[1]
    pair[1] = total

# Find Q-quantiles and print it to stdout
k = 1
for v, i in array:
    if math.ceil(total * k / Q) >= total:
        break
    elif i < math.ceil(total * k / Q):
        pass
    else:
        print(v)
        k += 1
```

Frankly speaking, this coding problem is not very difficult. I could have solved it quickly.
