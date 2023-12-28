#!/bin/bash
[ ! -e ./.env ] && cp -p env.sample .env && echo "Created .env from env.sample! Please check"

. .env


pynoser_repo="git@github.com:Herrminator/pynoser-proto.git"
ssh git@github.com 2>&1 | grep success > /dev/null ||\
  pynoser_repo="https://github.com/Herrminator/pynoser-proto.git"

# create empty files if necessary to make docker file volumes work
touch ./data/logs/uwsgi.log
touch ./data/logs/cron.log

# the weirdest symlink of all (creates /home/johler/develop/python/django/pynoser/data in container)
ln -sf /data ./data
# more no-existent symlinks ;)
# /opt/pynoser/pynoser/util/pywrap

# Retrieve required scripts from pynoser-proto
scripts="pynoser-admin pynoser-sh pynoser-cron-sh pynoser-errreset pynoser-randupd docker.compose.up docker.compose.down"

mkdir -p ./tmp

if [ "$1" == "-r" ]; then
    rm $scripts
    exit
fi

if [[ ! -L "pynoser-admin" || "$1" == "-f" ]]; then
    pushd pynoser-scripts
    # not supported by github :(
    # git archive --remote="$pynoser_repo" HEAD $scripts | tar x0

    git clone $pynoser_repo pynoser.tmp
    pushd pynoser.tmp || exit
    cp -p $scripts ..
    cp -p doc/restore ../../tmp
    popd
    rm -rf pynoser.tmp
    ln -srf $scripts ..
    popd
else
    echo "Script links seem to exist. Use '-f' to overwrite"
fi
