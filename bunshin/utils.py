import os
from fabric.api import task, sudo, execute, env
from fabric.contrib.files import upload_template

from .config import SALT_MASTER, SALT_MASTER_USER


@task
def install_minion():
    """ Install saltstack minion into the instance. """

    # install saltstack minion
    sudo('add-apt-repository ppa:saltstack/salt -y')
    sudo('apt-get update')
    sudo('apt-get install salt-minion -y')

    # update minion config
    pkg_path = os.path.abspath(os.path.dirname(__file__))
    templates = os.path.join(pkg_path, 'templates')
    context = {'master': SALT_MASTER}
    upload_template(filename='minion',
                    destination='/etc/salt/minion',
                    context=context,
                    use_jinja=True,
                    template_dir=templates,
                    use_sudo=True)

    # restart minion so it'll connect to master
    sudo('service salt-minion restart')


@task
def accept_minion(minion):
    """ Accept the minion from master. """
    sudo('salt-key -a %s' % minion)


def join_instance(instance):
    """
    Join `instance` to master by installing minion
    on it and accepting its key on master.
    """
    env.host_string = 'ubuntu@%s' % instance.public_dns_name
    execute(install_minion)

    # switch to master and accept minion
    env.host_string = '%s@%s' % (SALT_MASTER_USER, SALT_MASTER)
    execute(accept_minion, minion=instance.private_dns_name)
