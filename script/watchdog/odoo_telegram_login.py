# Copyright 2019  Micronaet SRL (<https://micronaet.com>).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import telepot
import socket
import time
import pdb
from datetime import datetime, timedelta
try:
    import ConfigParser
except:
    import configparser as ConfigParser

# -----------------------------------------------------------------------------
#                             Read Parameters:
# -----------------------------------------------------------------------------
cfg_file = '../odoo.cfg'  # same directory
config = ConfigParser.ConfigParser()
config.read(cfg_file)

# General parameters:
verbose = False
dry_run = False

log_file = config.get('watchdog', 'log_file')
wait = eval(config.get('watchdog', 'wait'))

telegram_token = config.get('telegram', 'token')
telegram_group = config.get('telegram', 'group')
telegram_alert_loop = eval(config.get('telegram', 'loop'))

dbname = config.get('dbaccess', 'dbname')
user = config.get('dbaccess', 'user')
pwd = config.get('dbaccess', 'pwd')
server = config.get('dbaccess', 'server')
port = int(config.get('dbaccess', 'port'))


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
    bot.sendMessage(telegram_group, 'OpenERP {} watchdog started'.format(
        dbname))
except:
    log_message('OpenERP {} watchdog started!'.format(dbname), mode='error')

bot.sendMessage(telegram_group, 'OpenERP {} start checking...!'.format(dbname))

try:
    while True:
        try:
            # -----------------------------------------------------------------
            # Network check:
            # -----------------------------------------------------------------
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # 3 Second Timeout
            if not sock.connect_ex((server, port)):
                log_message(
                    'OpenERP acceso e funzionante (wait %s sec.)' % wait)

                # Wait seconds:
                time.sleep(wait)
            else:
                # -------------------------------------------------------------
                # Send telegram alert:
                # -------------------------------------------------------------
                while True:
                    try:
                        bot.sendMessage(
                            telegram_group,
                            'OpenERP {} spento! (attesa: {} sec.)'.format(
                                dbname,
                                telegram_alert_loop,
                                ))
                        break  # Sent correctly
                    except:
                        log_message(
                            'OpenERP {} spento! (attesa: {} sec.)'.format(
                                dbname, telegram_alert_loop),
                            mode='error')

                # Wait seconds before next alarm:
                time.sleep(telegram_alert_loop)

        except:
            log_message(
                'OpenERP {} generic error!'.format(dbname),
                mode='error')
            # Break if CTRL + C or CTRL + C
            break
finally:
    log_message('End procedure')
log_message('End script')
