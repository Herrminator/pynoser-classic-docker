# pynoser-classic-docker

Sample docker runtime-configuration for PyNoser classic (pynoser-proto)

Last tested with real-life data on Dec. 28, 2023.

# TL;DR

First run `init.sh`! This will create some required symlinks.
Then either restore existing data (see `tmp/get-remote` and `tmp/restore`)
or run `pynoser-new` after starting the containers.
If you get an error about a readonly database, run data/chmod.sh (maybe with sudo).

# Motivation

PyNoser was **not** written with docker in mind. In fact, it was written more than
17 years ago, when docker wasn't even on the horizon.

So, PyNoser is a kind of complex arrangement of Django apps and scripts, combined
with cron jobs to keep the database up to date.

[`pynoser-proto`](https://github.com/Herrminator/pynoser-proto) is an attempt to
run a legacy Django app in a container. But the configuration is still kind of
complex.

This repository provides sample configurations and admin scripts (cleanup,
error reset, ...) to run a PyNoser container.

# Chores

Daily (not necessarily) checks and cleanups
```
df -BM /
pynoser-errreset ok
pynoser-cleanclip 
pynoser-clean-orphaned 
pynoser-cleanimg 
pynoser-cleanimg_html 
pynoser-sql < scripts/sql/largearticles.sql
${HOME}/bin/logfollow 
journalctl -e -p 4 -x ### daily check
insthist.py -uv | less +G
upddist ### daily check
${HOME}/docker/docker.repocheck 
sudo ipset list|less
sudo iptables -L -vn|less
```
