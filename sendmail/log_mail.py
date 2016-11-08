# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import sys
import ConfigParser
from smtplib import SMTP
from datetime import datetime

#folder = sys.argv[1]

cfg_file = os.path.expanduser('~/etl/openerp.cfg')

config = ConfigParser.ConfigParser()
config.read([cfg_file])
smtp_host = config.get('smtp', 'host')
smtp_port = eval(config.get('smtp', 'port'))
smtp_user = config.get('smtp', 'user')
smtp_password = config.get('smtp', 'password')
smtp_from = config.get('smtp', 'form')
smtp_to = config.get('smtp', 'to')
subject = config.get('smtp', 'subject')

# Parameter:
body = 'body'

# Send mail:
smtp = SMTP()
smtp.set_debuglevel(0)
smtp.connect(smtp_host, smtp_port)
smtp.login(smtp_user, smtp_password)

date = datetime.now().strftime('%Y-%m-%s %H:%M')
smtp.sendmail(
    from_addr, to_addr,
    'From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s' % (
        from_addr,
        to_addr,
        subject,
        date,
        body,
        ))
smtp.quit()
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: