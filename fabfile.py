from fabric.api import run, sudo, local, cd, env

env.hosts = ['orlando.thraxil.org']
env.user = 'anders'
nginx_hosts = ['lolrus.thraxil.org']

def restart_gunicorn():
    sudo("restart sebastian", shell=False)

def prepare_deploy():
    local("make test")

def deploy():
    code_dir = "/var/www/sebastian/sebastian"
    with cd(code_dir):
        run("git pull origin master")
        run("make migrate")
        run("make collectstatic")
        run("make compress")
        for n in nginx_hosts:
            run(("rsync -avp --delete media/ "
                 "%s:/var/www/sebastian/sebastian/media/") % n)
    restart_gunicorn()
