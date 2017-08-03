# -*- coding: utf-8 -*-
###############################################################################
#
# ODOO (ex OpenERP) 
# Open Source Management Solution
# Copyright (C) 2001-2015 Micronaet S.r.l. (<http://www.micronaet.it>)
# Developer: Nicola Riolini @thebrush (<https://it.linkedin.com/in/thebrush>)
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import sys
import erppeek
import xlsxwriter
import ConfigParser


# -----------------------------------------------------------------------------
# Read configuration parameter:
# -----------------------------------------------------------------------------
# From config file:
cfg_file = os.path.expanduser('../openerp.cfg')

config = ConfigParser.ConfigParser()
config.read([cfg_file])
dbname = config.get('dbaccess', 'dbname')
user = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = config.get('dbaccess', 'port')   # verify if it's necessary: getint

# Excel:
row_start = 1
file_out = '~/all_product.xlsx'
file_out = os.path.expanduser(file_out)

# -----------------------------------------------------------------------------
# Utility:
# -----------------------------------------------------------------------------
def xls_write_row(WS, row, row_data, format_cell=None):
    ''' Print line in XLS file            
    '''
    ''' Write line in excel file
    '''
    col = 0
    for item in row_data:
        try:
            if format_cell:
                WS.write(row, col, item, format_cell)
            else:            
                WS.write(row, col, item)
        except:
            WS.write(row, col, '#ERR')
        col += 1
    return True

# -----------------------------------------------------------------------------
# Connect to ODOO:
# -----------------------------------------------------------------------------
odoo = erppeek.Client(
    'http://%s:%s' % (
        server, port), 
    db=dbname,
    user=user,
    password=pwd,
    )
product_pool = odoo.model('product.product')
template_pool = odoo.model('product.template')

# -----------------------------------------------------------------------------
# Read database used:
# -----------------------------------------------------------------------------
WB = xlsxwriter.Workbook(file_out)
WS = WB.add_worksheet('Prodotti')

columns = product_pool.fields().keys()
template_columns = template_pool.fields().keys()
xls_write_row(WS, 0, columns)

description = [
    product_pool.fields()[item]['string'] for item in product_pool.fields()]
    
# Description
xls_write_row(WS, 1, description)

# Translate
translate_fields = [
    name for name in product_pool.fields() if \
        product_pool.fields()[name].get('translate', False)]

translate = [
    ('X' for name in translate_fields else '') \
        for name in product_pool.fields()]
xls_write_row(WS, 2, translate)
            

# Read newsletter category and put in database:
product_ids = product_pool.search([
    ('default_code', '!=', False),
    ('statistic_category', 'in', 
        ('C01', 'I01', 'I02', 'I03', 'I04', 'I05', 'I06')),
    ])

i = 1
for product in product_pool.browse(product_ids):
    i += 1
    if i == 4:
        break
    print 'Write line: %s' % i
    res = []
    for col in columns:
        if col in template_columns:
            try:
                res.append(eval('product.product_tmpl_id.%s' % col))
            except:
                res.append('#ERR')
        else:        
            try:
                value = eval('product.%s' % col)
            except:
                res.append('#ERR')
                            
    xls_write_row(WS, i, res)
WB.close()
