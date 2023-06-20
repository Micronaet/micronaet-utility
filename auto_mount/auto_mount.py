import os
import ConfigParser
import time
from datetime import datetime


# -----------------------------------------------------------------------------
# Parameters:
# -----------------------------------------------------------------------------
cfg_file = os.path.expanduser('./setup.cfg')

config = ConfigParser.ConfigParser()
config.read([cfg_file])
server = config.get('setup', 'server')
mount_file = config.get('setup', 'mount_file')
mount_command = config.get('setup', 'mount_command')
max_try = eval(config.get('setup', 'max_try'))
sleep = eval(config.get('setup', 'sleep'))


# -----------------------------------------------------------------------------
#                                  UTILITY
# -----------------------------------------------------------------------------
def host_is_on(hostname, hop=5):
    """ Check if host is on
    """
    response = os.system('ping -c %s %s' % (
        hop, hostname,
        ))

    if response == 0:
        return True
    else:
        return False

def log_message(log_f, message, mode='info', verbose=True):
    """ Log on file
    """
    now = str(datetime.now())[:19]
    message = '%s. [%s] %s\n' % (
        now,
        mode.upper(),
        message,
        )

    log_f.write(message)
    if verbose:
        print(message.strip())


# -----------------------------------------------------------------------------
#                                  PROCEDURE:
# -----------------------------------------------------------------------------
log_file = './activity.log'
log_f = open(log_file, 'a')

if host_is_on:
    if not os.path.isfile(mount_file):
        # Check mount file
        while max_try > 0:
            message = 'Host is on and not mounted, try to mount #%s...' % \
                max_try
            log_message(log_f, message, mode='warning')

            os.system(mount_command)
            max_try -= 1
            if os.path.isfile(mount_file):
                message = 'Host mounted!'
                log_message(log_f, message, mode='info')
                break
            time.sleep(sleep)
    else:
        message = 'Host is yet mounted'
        log_message(log_f, message, mode='info')

else:
    message = 'Host is off'
    log_message(log_f, message, mode='error')
