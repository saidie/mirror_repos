#!/usr/bin/env python3

import __base__

import os
import configparser

from mirror_repos import host, target

host_mgr = host.HostManager()
host_mgr.load_config(os.path.join(__base__.CONFIG_DIR, 'host.cfg'))

target_config = configparser.ConfigParser()
target_config.read(os.path.join(__base__.CONFIG_DIR, 'target.cfg'))

for section in target_config.sections():
    options = dict(target_config.items(section))
    tgt = target.Target(options)
    tgt.run()
