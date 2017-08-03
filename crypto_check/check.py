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
import ConfigParser
import pickle

# Telegram bot:
import telepot
from datetime import datetime

# -----------------------------------------------------------------------------
#                                Parameters
# -----------------------------------------------------------------------------
# Extract config file name from current name
fullname = './micronaet.cfg' # same folder
file_check = [
    r'c:\\micronaet.doc', 
    r'c:\\windows\micronaet.doc', 
    r'c:\\mexalbp\micronaet.doc', 
    ]

config = ConfigParser.ConfigParser()
config.read([fullname])

# Telegram:
telegram_token = config.get('telegram', 'token')
telegram_group = config.get('telegram', 'group')

def create_file():
    ''' First creation 
    '''
    for f in file_check:
        os.system('touch %s' % f)

def check_file():
    ''' First creation 
    '''
    for f in file_check:
        if not os.path.isfile(f):
            return False
    return True

if len(sys.argv) == 2:
    # read parameter:
    parameter = sys.argv[1]
    if parameter == 'start':
        create_check_file()
        
if check_file():
    error = ''
else:
    error = 'Crypto attack!'

# -----------------------------------------------------------------------------
#                              Comunicate Telegram
# -----------------------------------------------------------------------------
now = datetime.now()

# Notification if info time out or error:
if error > 0:
    bot = telepot.Bot(telegram_token)
    bot.getMe()
    bot.sendMessage(telegram_group, error)
else:
    print '[INFO] No comunication in telegram'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:        
