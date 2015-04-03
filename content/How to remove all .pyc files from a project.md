Title: How to remove all .pyc files from a project?
Date: 2014-07-31 19:39
Modified: 2014-07-31 19:39
Category: Linux
Tags: Linux, Shell

I am a paranoid guy. I like to delete all "useless" files. I want to clean up my project repository today. There are lots of `.pyc` files. And I found this command, which is very convenient to batch delete files in a directory.

	:::bash
	find . -name "*.pyc" -exec rm -rf {} \;

I can also delete all `*.class` files for Java project and `.o` files for C project in this way.

	:::bash
	find . -name "*.class" -exec rm -rf {} \;
	find . -name "*.o" -exec rm -rf {} \;

Or I can delete all files whose name starts with 'test'.

	:::bash
	find . -name "test*" -exec rm -rf {} \;
	
**Reference:**

* [How do I remove all .pyc files from a project?](http://stackoverflow.com/questions/785519/how-do-i-remove-all-pyc-files-from-a-project)