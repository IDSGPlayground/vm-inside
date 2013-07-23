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

def initialize(opts, args):
    config = Config(opts, args)
    return config

def run(config):
    debug('something')

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
