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
try:
    file_name = sys.argv[1]
except:
    print "[ERROR] Use:\ninvoice.py file.csv"
    sys.exit()    
config_file = os.path.expanduser(os.path.join("~", "ETL", "Fiam8", "openerp.cfg"))
csv_file = os.path.expanduser(os.path.join("~", "ETL", "Fiam8", file_name))

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

property_account_receivable = 33 # NOTE manually setup for speed

# Header creation:
print "[INFO] Start importation:"
csv_file = open(csv_file, "r")

i = 0
max_col = False
old_invoice = False
status = False
for all_line in csv_file:
    try:
        status = "parsing line..."
        line = all_line.strip().split(separator)
        if not max_col:
            max_col = len(line)
        if len(line) != max_col:
            print "[ERROR] Col line different, jumped"
            continue
            
        # ------------
        # Read fields:
        # ------------
        # Header:    
        status = "read header fields..."
        partner_code = format_string(line[0])
        doc_nickname = format_string(line[1])
        doc_type = format_string(line[2])
        doc_number = format_int(line[3])
        date = format_date(line[4])
        agent_code = format_string(line[5])

        # Details:
        status = "read line fields..."
        product_code = format_string(line[6])
        product_description = format_string(line[7])
        quantity = format_float(line[8])
        price = format_float(line[9])
        #format_float(line[10])
        total = format_float(line[11])
        sequence = format_string(line[12])

        status = "creating extra fields..."
        name = "%s-%s-%06d" % (doc_nickname, doc_type, doc_number)

        partner_id = get_partner_from_code(sock, dbname, uid, pwd, partner_code, {
            'name': "Partner code %s" % partner_code,
            'ref': partner_code,
            'sql_customer_code': partner_code, 
            })
            
        product_id = get_product_from_code(sock, dbname, uid, pwd, partner_code, {
            'name': product_description,
            'default_code': product_code
            })

        status = "creating header..."
        if old_invoice != name:
            old_invoice = name
            # ---------------
            # Header Invoice:
            # ---------------
            header_data = {
                'name': name,
                'number': name,
                'date_invoice': date,
                'partner_id': partner_id,
                'account_id': property_account_receivable,
                }
                    
            status = "searching header..."
            invoice_id = sock.execute(dbname, uid, pwd, "account.invoice", 'search', [
                ('name', '=', name)])
            if invoice_id:
                status = "updating header..."
                invoice_id = invoice_id[0]        
                print "[INFO] Invoice header updated: %s" % name
            else: 
                status = "creating header..."
                invoice_id = sock.execute(dbname, uid, pwd, "account.invoice", 
                    "create", header_data)
                print "[INFO] Invoice header created: %s" % name
            
        # ----------------
        # Details Invoice:
        # ----------------
        status = "updating detail..."
        detail_data = {
            'name': product_description,
            'product_id': product_id,
            'quantity': quantity,
            'price_unit': price,
            'sequence': sequence, 
            'invoice_id': invoice_id,
            #total
            #'uos_id'
            #'account_id'
            #'name'
            #price_subtotal
            #discount        
            }

        status = "searching detail..."
        line_id = sock.execute(dbname, uid, pwd, "account.invoice.line", 'search', [
            ('invoice_id', '=', invoice_id),
            ('sequence', '=', sequence),
            ])
        if line_id:
            status = "updating detail..."
            print "[INFO] Invoice line updated: %s %s" % (name, sequence)
        else: 
            status = "creating detail..."
            sock.execute(dbname, uid, pwd, "account.invoice.line", 
                "create", detail_data)
            print "[INFO] Invoice line created: %s %s" % (name, sequence)
    except:
        print "Line jumped cause error during", status, "Error:", sys.exc_info()          
        continue      
        
# Workflow:
invoice_ids = sock.execute(dbname, uid, pwd, "account.invoice", 'search', [
    ('state', '=', 'draft')])
for invoice_id in invoice_ids:
    sock.exec_workflow(dbname, uid, pwd, 'account.invoice',
        'invoice_open', invoice_id)
        
# After WF set number:
# update account_invoice set number=name;
print "[INFO] Importation completed!"
