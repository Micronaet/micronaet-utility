#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# This module create or updare standard anagraphic list

# Modules required:
import sys
import os
import xmlrpclib
import ConfigParser
from format import *
from openerp import *


# Set up parameters (for connection to Open ERP Database) ********************************************
config = ConfigParser.ConfigParser()

config_file = os.path.expanduser(os.path.join("~", "ETL", "Fiam8", "openerp.cfg"))

config.read([config_file])
dbname = config.get('dbaccess', 'dbname')
uid = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = config.get('dbaccess', 'port')   # verify if it's necessary: getint
separator = config.get('dbaccess', 'separator') # test


# XMLRPC connection for autentication (UID) and proxy 
sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/common' % (server, port), allow_none=True)
uid = sock.login(dbname ,uid ,pwd)
sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/object' % (server, port), allow_none=True)

# Workflow:
print "[INFO] Start importation!"
invoice_ids = sock.execute(dbname, uid, pwd, "account.invoice", 'search', [
    ('state', '=', 'draft')])
for invoice_id in invoice_ids:
    sock.exec_workflow(dbname, uid, pwd, 'account.invoice',
        'invoice_open', invoice_id)
    print "Validated ID:", invoice_id    

print "[INFO] Importation completed!"
