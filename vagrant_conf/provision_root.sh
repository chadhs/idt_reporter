#!/bin/bash

set -e

main() {
    install_apt_packages
	update_python_tools
    config_postgres
    config_npm
    config_shell
    config_ssh
}

install_apt_packages() {
    apt-get update

    # this is to be able to manipulate apt repositories
    apt-get install -y software-properties-common python-software-properties

    # to get a recent nodejs, which bundles npm and nosejs-dev also
    add-apt-repository -y ppa:chris-lea/node.js
	# ruby-rvm isn't available for 14.04, so let's grab it
    add-apt-repository -y ppa:rael-gc/rvm

    apt-get update --fix-missing

    # let's make sure ruby1.9 is loaded first and takes precedence
    apt-get install -y ruby1.9.1 ruby1.9.1-dev rvm

    # bash syntax for arrays is a big strange, but that's all that's going on with the declare -a and ${packages[*]}
    declare -a packages=(
        # keep related things close to each other
        emacs23-nox vim-nox git zsh tree htop sqlite3 screen tmux lynx
        cachefilesd # for fast nfs
        apache2 libapache2-mod-wsgi
        postgresql-9.3 libpq-dev

        python-dev python-psycopg2 python-imaging python-setuptools
        virtualenvwrapper
        libreadline6 libreadline6-dev ncurses-dev apt-file # without installing apt-file python's readline is unable to compile ???

        g++ make nodejs libfontconfig # the nodejs package includes npm and nodejs-dev, libfontconfig is a dependency of phantomjs
        ruby-compass
        rabbitmq-server libxml2-dev libxslt-dev
        ruby-json # for heroku toolbelt to not throw warnings about a more efficient json library
    )

    apt-get install -y ${packages[*]}

    # clean up junk we no longer need
    apt-get autoremove -y

    #make sure cachefilesd is running on boot (for speedy nfs)
    echo "RUN=yes" > /etc/default/cachefilesd
}

update_python_tools() {
    # going from pip 1.x to 6.x with a `pip install --upgrade pip` causes path problems,
    # therefore, use easy_install load load pip avoiding the issue.
    easy_install -U setuptools
    easy_install -U pip
    pip install --upgrade virtualenv virtualenvwrapper readline
}

config_postgres() {
    # fix the default encoding, otherwise creating a db requires that we pass
    # template, locale, and encoding by hand and this can't be done easily for
    # tests.
    pg_dropcluster --stop 9.3 main
    pg_createcluster --start --encoding=UTF8 --locale=en_US.utf8 9.3 main
    sudo -u postgres createuser -drsw vagrant
    sudo -u vagrant createdb idt_reporter-dev
}

config_npm() { npm config set registry http://registry.npmjs.org/ --global; }

config_shell() { chsh -s `which zsh` vagrant; }

config_ssh() {
    # host_id_rsa.pub is put in place by a file provisioner in Vagrantfile
    cat /home/vagrant/.ssh/host_id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
}

main
