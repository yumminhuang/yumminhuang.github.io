from fabric.api import *
import os
import shutil

# Run on local machine
env.hosts = ['localhost']
# Local path configuration (can be absolute or relative to fabfile)
PD = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEPLOY_PATH = PD + '/yumminhuang.github.io'

# pelican-bootstrap3 doesn't support instagram logo.
# Use a kludge to fix it
CSS_FILENAME = 'pelican-bootstrap3/templates/includes/sidebar.html'


def commit_and_push():
    local('git add -A')
    local('git commit -m "Update blog"')
    local('git push')


def replace(string, replacement, filename):
    local("""ruby -i -pe "gsub \\"%s\\", \\"%s\\"" %s""" %
          (string, replacement, filename))


@task
def clean():
    """Remove generated files"""
    if os.path.isdir(DEPLOY_PATH):
        shutil.rmtree(DEPLOY_PATH)
        os.makedirs(DEPLOY_PATH)


@task
def build():
    """Build local version of site"""
    local('pelican -o %s -s pelicanconf.py' % DEPLOY_PATH)


@task
def regenerate():
    """Automatically regenerate site upon file modification"""
    local('pelican -o %s -r -s pelicanconf.py' % DEPLOY_PATH)


@task
def publish():
    """generate using production settings"""
    local('pelican -o %s -s publishconf.py' % DEPLOY_PATH)


@task
def deploy():

    replace("'weibo'", "'weibo', 'instagram'", CSS_FILENAME)

    # Move .git to avoid flushing git config
    local('mv %s/.git %s/git' % (DEPLOY_PATH, PD))

    print('Publish sites')
    publish()

    replace("'weibo', 'instagram'", "'weibo'", CSS_FILENAME)

    # Commit changes
    with lcd(DEPLOY_PATH):
        local('mv ../git .git')
        print('Commit and Push')
        commit_and_push()
