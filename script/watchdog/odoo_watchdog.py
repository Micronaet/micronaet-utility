# Copyright 2019  Micronaet SRL (<https://micronaet.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import os
import pdb
import psutil
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

# -----------------------------------------------------------------------------
# ODOO Command:
# -----------------------------------------------------------------------------
start_command = f'{command} {start} -c {setup} -d {database}'

# -----------------------------------------------------------------------------
# Log file:
# -----------------------------------------------------------------------------
log_f = open(log_file, 'w')


def log_message(log_f, message, mode='info', verbose=True):
    """ Write log message
    """
    log_text = '{}. [{}] {}'.format(
        str(datetime.now())[:19],
        mode.upper(),
        message,
    )

    # Log only error:
    if mode != 'info':
        log_f.write(log_text)

    # Verbose:
    if verbose:
        print(log_text)
    return True


# -----------------------------------------------------------------------------
# Check process:
# -----------------------------------------------------------------------------
log_message(log_f, 'Start procedure')
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
            log_f, 'ODOO acceso e funzionante, ID: {} [Attesa: {}]'.format(
                pid, wait))
    else:
        log_message(log_f, 'Avvio ODOO non trovato acceso', mode='error')
        try:
            log_message(log_f, f'Avvio ODOO {start_command}', mode='error')
            if not dry_run:
                os.system(start_command)
                # Program freeze here
        except:
            log_message(log_f, 'Errore avviando ODOO', mode='error')

    # Wait seconds:
    time.sleep(wait)

log_message(log_f, 'End procedure')
