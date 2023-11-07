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
import time

from setup_logger import *

tasks = [
    f'{green_book} List of current Apps',
    f'{green_book} Open App in Browser',
    f'{green_book} Get config for App',
    f'{green_book} Get App releases',
    f'{green_book} Get Domains for App',
    f'{green_book} Get logs for App',
    f'{green_book} GIT remotes for MUSIC_HOMEPAGE Django Project',
    f'{tick} Enable Collect Static on deploy',
    f'{cross_mark} Disable Collect Static on deploy',
    Separator(),
    f'{cactus} Django: Start local server and browse to Aisling Home Page',
    f'{cactus} Django: Compare two versions of Project',
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

    if 'List of current Apps' in task:
        app_urls= [x.web_url for x in happs]
        logger.info (happ_names)
        logger.info (app_urls)
    elif 'Open App in Browser' in task:
        happ_name = get_app(happ_names)
        happ_obj = happ_info[happ_name]
        os.system (f'open {happ_obj.web_url}')
    elif 'Get config for App' in task:
        happ_name = get_app(happ_names)
        happ_obj = happ_info[happ_name]
        happ_config = happ_obj.config()
        logger.info(happ_config)
    elif 'Get App releases' in task:
        happ_name = get_app(happ_names)
        happ_obj = happ_info[happ_name]
        rlist = happ_obj.releases(order_by='version', limit=10, sort='desc')
        for ritem in rlist:
            logger.info (f'{ritem.version} {ritem.description}')
    elif 'Get logs for App' in task:
        happ_name = get_app(happ_names)
        happ_obj = happ_info[happ_name]
        happ_log = happ_obj.get_log()
        logger.info (happ_log)
    elif 'Get Domains for App' in task:
        happ_name = get_app(happ_names)
        happ_obj = happ_info[happ_name]
        happ_domains = happ_obj.domains(order_by='id')
        logger.info(happ_domains)
    elif 'GIT remotes for MUSIC_HOMEPAGE Django Project' in task:
        os.chdir ('MUSIC_HOMEPAGE')
        gremotes = getoutput('git remote -v')
        logger.info (gremotes)
    elif 'Django: Start local server and browse to Aisling Home Page' in task:
        pid = os.fork()
        if pid == 0:
            time.sleep(5)
            os.system('open http://127.0.0.1:9000')
        else:
            os.chdir('MUSIC_HOMEPAGE')
            os.system ('heroku local -p 9000')
    elif 'Disable Collect Static on Deploy' in task:
        os.system ('heroku config:set DISABLE_COLLECTSTATIC=1')
    elif 'Enable Collect Static on Deploy' in task:
        os.system ('heroku config:unset DISABLE_COLLECTSTATIC')
    elif 'Django: Compare two versions of Project' in task:
        os.chdir ('Existing_Heroku_App_Versions')
        os.system ('opendiff aisling-music/ staging-aisling-music/')
    else:
        logger.error ('No matching task actions found')

if __name__ == '__main__':
    main()