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
import random
import ConfigParser
from datetime import datetime, timedelta

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

file_in = './clienti.csv'

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

# Pool used:
partner_pool = odoo.model('res.partner')
invoice_pool = odoo.model('account.invoice')

import pdb; pdb.set_trace()
partner_db = {}
counter = 0
for row in open(file_in, 'r'):
    counter += 1
    name = row.strip()
    partner_ids = partner_pool.search([
        ('name', '=', name),
    ])
    if partner_ids:
        partner_db[name] = partner_ids[0]
        print('[INFO] %s. Partner %s updated' % (counter, name))
    else:
        partner_db[name] = partner_pool.create({
            'name': name,
        })
        print('[INFO] %s. Partner %s created' % (counter, name))

import pdb; pdb.set_trace()
total = len(partner_db) - 1
now = datetime.now()
for loop in range(1000):
    amount = random.randrange(10) * 1000
    day_date = random.randrange(365)
    date = (now - timedelta(days=day_date)).strftime('%Y-%m-%d')
    partner_pos = random.randrange(total)

    invoice_pool.create({
        'partner_id': partner_db[partner_pos],
        'date_invoice': date,
        'payment_term_id': False,
        # 'sequence_number_next':
        'manual_total': amount,
    })

