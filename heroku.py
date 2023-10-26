#! /Users/martin/VENVS/py3.8/bin/python3
# -*- coding: utf-8 -*-
"""
list prompt example
"""
# from __future__ import print_function, unicode_literals

import os,sys
import subprocess
import shlex

from pprint import pprint
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

import tempfile
from jinja2 import Template
from subprocess import *
from iterfzf import *
import glob
# https://github.com/martyzz1/heroku3.py
import heroku3
import argparse

from setup_logger import *

tasks = [
    f'{green_book} List of current apps',
    f'{green_book} Get logs for app',
    f'{green_book} GIT remotes for MUSIC_HOMEPAGE Django Project',
    f'',
    Separator(),
    ]
# ===============================================
def get_app(anames):
    app = inquirer.select(
        message="Select App:",
        choices=anames,
        height='100%',
        default=None,
    ).execute()
    return app

# =====================================================================
def main():
    parser = argparse.ArgumentParser(description='This does cool stuff man!')
    parser.add_argument('--debug', action="store_true", help='Run in debug mode')
    args = parser.parse_args()
    if args.debug:
        coloredlogs.set_level('DEBUG1')
    os.system ('clear')
    print ('\n\n')
    # ________________________

    heroku_conn = heroku3.from_key('9e86444a-a389-449c-8b25-7bb1cdb16843')
    happs = heroku_conn.apps()
    happ_info = {}
    for item in happs:
        happ_info[item.name] = item
    happ_names = list(happ_info.keys())
    task = inquirer.select(
        message="Select action:",
        choices=tasks,
        height='100%',
        default=None,
    ).execute()
    if not task:
        return

    if 'List of current apps' in task:
        app_urls= [x.web_url for x in happs]
        logger.info (happ_names)
        logger.info (app_urls)
    elif 'Get logs for app' in task:
        happ_name = get_app(happ_names)
        happ_obj = happ_info[happ_name]
        happ_log = happ_obj.get_log()
        logger.info (happ_log)
    elif 'GIT remotes for MUSIC_HOMEPAGE Django Project' in task:
        os.chdir ('MUSIC_HOMEPAGE')
        gremotes = getoutput('git remote -v')
        logger.info (gremotes)
    else:
        logger.error ('No matching task actions found')

if __name__ == '__main__':
    main()