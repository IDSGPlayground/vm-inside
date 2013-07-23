#!/usr/bin/env python

import getopt
import re
import os
import sys
import logging
from   logging import debug, info, error, warn
import fileinput, os, sys
import vagrant
from fabric.api import env, run, execute
from subprocess import CalledProcessError

import time

class Retry(object):
    defaultexceptions = (Exception,)
    def init(self, tries, exceptions=None, delay=0):
        """
        Decorator for retrying a function if exception occurs

        tries -- num tries
        exceptions -- exceptions to catch
        delay -- wait between retries
        """
        self.tries = tries
        if exceptions is None:
            exceptions = Retry.defaultexceptions
        self.exceptions =  exceptions
        self.delay = delay

    def _call(self, f):
        def fn(args, *kwargs):
            exception = None
            for  in range(self.tries):
                try:
                    return f(args, *kwargs)
                except self.exceptions, e:
                    print "Retry, exception: "+str(e)
                    time.sleep(self.delay)
                    exception = e
            #if no success after tries, raise last exception
            raise exception
        return fn

def initialize(opts, args):
    config = Config(opts, args)
    return config

def run(config):
    v = vagrant.Vagrant()
    info("Initializing Vagrant cell...")
    v.init("raring64")
    info("Booting up cell...")
    v.up(provider)
    info("Finalizing new cell...")
    env.host_string = v.user_hostname()
    env.key_filename = v.keyfile()
    env.disable_known_hosts = True
    shell_command = "vagrant status | grep 'running (' | awk '{ print $2$3 }'"
    event = Popen(shell_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    output = event.communicate()
    if output[0].find("running") != -1:
       prvdr = output[0][8:len(output[0])-2]
       info("Successfully created new " + prvdr + " cell!")
    else: warn("Something went horribly wrong.")
    print()

def cleanup(config):
    pass

class Config():
    def __init__(self, opts, args):
        self.files = args
        self.provier = 'lxc'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        config = initialize(opts, args)
        run(config)
        cleanup(config)
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    main()
