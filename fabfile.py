from fabric.api import *

@task(alias='loc')
def localhost():
    env.run = local
    env.project_venv = 'dane-dhp'

@task(alias='rem')
def remote():
    env.hosts = ['danehillard.com']
    env.run = run
    env.user = 'www'
    env.key_filename = '/Users/danehillard/.ssh/dhillard.pem'
    env.project_venv = 'dhp'
    env.project_path = 'dhp'

def manage(args):
    with prefix('workon {venv}'.format(venv=env.project_venv)):
        env.run('./manage.py {args}'.format(args=args))

@task(alias='cs')
def collectstatic():
    manage('collectstatic --noinput -i *.sass')

@task(alias='db')
def update_database():
    manage('syncdb --noinput')
    manage('migrate --noinput')

@task(alias='stage')
def stage_commit_push_changes():
    local('git add -p')
    local('git commit')
    local('git push')

@task
def reload_wsgi():
    run('touch apache/django.wsgi')

@task(alias='dep')
def deploy():
    with cd(env.project_path):
        run('git pull')
        update_database()
        collectstatic()
        reload_wsgi()