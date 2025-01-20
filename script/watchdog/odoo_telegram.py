# Copyright 2019  Micronaet SRL (<https://micronaet.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import os
import pdb
import psutil
import telepot
import time
import sys
from datetime import datetime, timedelta
try:
    import ConfigParser
except:
    import configparser as ConfigParser

# -----------------------------------------------------------------------------
#                             Read Parameters:
# -----------------------------------------------------------------------------
cfg_file = '../odoo.cfg' # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)

# General parameters:
verbose = False
dry_run = False

command = config.get('watchdog', 'command')
start = config.get('watchdog', 'start')
setup = config.get('watchdog', 'setup')
database = config.get('watchdog', 'database')
log_file = config.get('watchdog', 'log_file')
wait = eval(config.get('watchdog', 'wait'))

telegram_token = config.get('telegram', 'token')
telegram_group = config.get('telegram', 'group')
telegram_alert_loop = eval(config.get('telegram', 'loop'))


def log_message(message, mode='info', verbose=True):
    """ Write log message
    """
    log_text = '{}. [{}] {}'.format(
        str(datetime.now())[:19],
        mode.upper(),
        message,
    )

    # Verbose:
    if verbose:
        print(log_text)
    return True


# -----------------------------------------------------------------------------
# Check process:
# -----------------------------------------------------------------------------
log_message('Start procedure')
bot = telepot.Bot(telegram_token)

try:
    bot.sendMessage(telegram_group, 'ODOO Punto curvatura watchdog started')
except:
    log_message('ODOO Punto curvatura watchdog started!', mode='error')

bot.sendMessage(telegram_group, 'ODOO Punto curvatura start checking...!')

while True:
    pid = False
    for process in psutil.process_iter():
        args = process.cmdline()
        if verbose:
            print('Process read: {}'.format(args))
        if (command in args and start in args and setup in args and
                database in args):
            if verbose:
                print('Found process #{} command: {}'.format(
                    process.pid, args))
            pid = process.pid
            break

    # Start service if not present:
    if pid:
        log_message(
            'ODOO acceso e funzionante, ID: {} [Attesa: {}]'.format(
                pid, wait))
    else:
        # Send telegram alert:
        while True:
            try:
                bot.sendMessage(telegram_group, 'ODOO Punto curvatura spento!')
            except:
                log_message('ODOO Spento!', mode='error')
            # Wait seconds before new alarm:
            time.sleep(telegram_alert_loop)
    # Wait seconds:
    time.sleep(wait)

log_message('End procedure')
