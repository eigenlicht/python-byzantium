#!/usr/bin/python

# -*- coding: utf-8 -*-
# vim: set expandtab tabstop=4 shiftwidth=4 :

""" shell.py - a library to support byzantium_configd.py accessing the command line utilities it needs

ChangeLog
- 2013/09/26 - haxwithaxe - separated from byzantium_configd.py
"""
__authors__ = ['haxwithaxe me@haxwithaxe.net',
               'eigenlicht eigenlicht@autistici.org']
__license__ = 'GPLv3'

# Imports
import psutil
from datetime import datetime, timedelta
import os
import byzantium

defaults = byzantium.config.Config()
logger = defaults.utils.get_logger('shell')

DIR_POWER_SUPPLY = '/sys/class/power_supply/'

def _convert_seconds_string(seconds):
    date_time = datetime(1, 1, 1) + timedelta(seconds=seconds)
    string = ''
    if date_time.year > 1:
        string += str(date_time.year-1) + " years, "
    if date_time.month > 1:
        string += str(date_time.month-1) + " months, "
    if date_time.day > 1:
        string += str(date_time.day-1) + " days, "
    if date_time.hour > 0:
        string += str(date_time.hour) + " hours, "
    if date_time.minute > 0:
        string += str(date_time.minute) + " minutes, "
    if date_time.second > 0:
        string += str(date_time.second) + " seconds, "
    return string[:-2]

def uptime():
    with open('/proc/uptime') as f:
        duration = f.read().split(' ', 1)[0]
    return _convert_seconds_string(float(duration))

def memory():
    # Fields: total, available, percent, used, free, active, inactive, buffers, cached
    return psutil.virtual_memory()

def swap():
    # Fields: total, used, free, percent, sin, sout
    return psutil.swap_memory()

def disk_space(path='/'):
    # Fields: total, used, free, percent
    return psutil.disk_usage(path)

def cpu_percent(interval=0.1, percpu=False):
    return psutil.cpu_percent(interval, percpu)

def net_io_counters(pernic=False):
    return psutil.net_io_counters(pernic)

def get_users():
    return psutil.get_users()

def has_battery():
    return any("BAT" in f for f in os.listdir(DIR_POWER_SUPPLY))

def _battery_num():
    if has_battery:
        dirs = (f for f in os.listdir(DIR_POWER_SUPPLY) if "BAT" in f)
        return int(dirs.__next__()[-1])
    else:
        return None # raise exception?

def _battery_capacity():
    with open(DIR_POWER_SUPPLY + 'BAT%i/charge_full' % _battery_num()) as f:
        return int(f.read())

def battery_charge():
    with open(DIR_POWER_SUPPLY + 'BAT%i/charge_now' % _battery_num()) as f:
        return int(f.read())/_battery_capacity() * 100.0