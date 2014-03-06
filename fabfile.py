from fabric.api import run, sudo, local, cd, env

env.hosts = ['orlando.thraxil.org']
env.user = 'anders'
nginx_hosts = ['lolrus.thraxil.org']

def restart_gunicorn():
    sudo("restart sebastian")

def prepare_deploy():
    local("./manage.py test")

def deploy():
    code_dir = "/var/www/sebastian/sebastian"
    with cd(code_dir):
        run("git pull origin master")
        run("./bootstrap.py")
        run("./manage.py migrate")
        run("./manage.py collectstatic --noinput --settings=sebastian.settings_production")
        for n in nginx_hosts:
            run(("rsync -avp --delete media/ "
                 "%s:/var/www/sebastian/sebastian/media/") % n)
    restart_gunicorn()
