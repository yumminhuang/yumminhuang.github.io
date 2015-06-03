Title: One Trick for Debugging Python
Date: 2015-05-11 20:18
Category: Miscellaneous
Tags: Python

I just learned one trick for debugging Python script from my colleague. It's not such magical  maybe most of Pythonistee have already used it everyday), but I think it is very useful to debug Python script.

I only need to add single line at the position I want to break.

    :::Python
    import code; code.interact(local=locals())

After that, run Python script as usual. Python Interpreter will stop at your break point and launch a REPL (*Read–eval–print loop*) console. You can print out variables to debug.

---
In Ruby, we can use [Pry](https://github.com/pry/pry) as the same way to debug Ruby script.
