#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os


def format_string(value):
    ''' Return formatted string without spaces
    '''
    try:
        return value.strip()
    except:
        return ""    

def format_float(value):
    ''' Return a float from string
    '''
    try:
        return float(value.strip().replace(",", "."))
    except:
        return 0.0

def format_int(value):
    ''' Return a integer from string
    '''
    try:
        return int(value.strip())
    except:
        return 0.0

def format_date(value):
    ''' Return a date from string
    '''
    try:
        value = value.strip()
        return "%s-%s-%s" % (value[:4], value[4:6], value[6:8])
    except:
        return False

def format_datetime(value):
    ''' Return a datedime from string
    '''
    try:
        return value
    except:
        return False

