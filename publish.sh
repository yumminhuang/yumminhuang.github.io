#!/bin/bash

# pelican-bootstrap3 doesn't support instagram logo.
# This is a kludge to fix it

ruby -i -pe "gsub \"'weibo'\", \"'weibo', 'instagram'\"" \
pelican-bootstrap3/templates/includes/sidebar.html

# In WebSite directory
# Move .git to avoid flushing git config
mv ../yumminhuang.github.io/.git ../git

# Publish site
make publish

ruby -i -pe "gsub \", 'instagram'\", ''" \
pelican-bootstrap3/templates/includes/sidebar.html

# Change to web page directory
cd ../yumminhuang.github.io

# Move .git back
mv ../git ./.git

echo 'Commit and Push'
git add .
git commit -m 'Update blog'
git push
