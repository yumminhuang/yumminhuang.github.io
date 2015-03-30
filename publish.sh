#!/bin/bash

# In WebSite directory
# Move .git to avoid flushing git config
mv ../yumminhuang.github.io/.git ../git

# Publish site
make publish

# Change to web page directory
cd ../yumminhuang.github.io

# Move .git back
mv ../git ./.git

echo 'Commit and Push'
git commit -a -m 'Update blog'
git push
