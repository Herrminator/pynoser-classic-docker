# pynoser-classic-docker
Sample docker runtime-configuration for PyNoser classic (pynoser-proto)

# TL;DR
First run init.sh! This will create some required symlinks.
Then either restore existing data (see `tmp/restore`) or run `pynoser-new`
after starting the containers.

# Motivation
PyNoser was *not* written with docker in mind. In fact, it was written more than
17 years ago, when docker wasn't even on the horizon.

So, PyNoser is a kind of complex arrangement of Django apps and scripts, combined
with cron jobs to keep the database up to date.

[`pynoser-proto`](https://github.com/Herrminator/pynoser-proto) is an attempt to
run a legacy Django app in a container. But the configuration is still kind of
complex.

This repository provides sample configurations and admin scripts (cleanup,
error reset, ...) to run a PyNoser container.
