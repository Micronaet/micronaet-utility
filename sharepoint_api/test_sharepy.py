#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
#
# ODOO (ex OpenERP)
# Open Source Management Solution
# Copyright (C) 2001-2015 Micronaet S.r.l. (<https://micronaet.com>)
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
import sharepy
import logging
import pdb

from sharepy import connect
from sharepy import SharePointSession


pdb.set_trace()
client_id = 'e31f9c0f-5a52-4ae3-85bc-c175045396bc'  # App ID
client_secret = 'L+3eec8y95HDt1MIO+/9Oo7d/QmLiFvaGkqoHepXeM4='
tenant = 'panchemicalsitaly'
# site = 'IT'
# tenant_id = 'd6a7ff30-4398-46ab-9a8c-821db007295f'

sharepoint = 'https://{}.sharepoint.com'.format(tenant)
url = 'https://{}.sharepoint.com/:x:/r/personal/601600/_layouts/15/'.format(
    tenant,
    )

s = sharepy.connect(sharepoint, client_id, client_secret)
# Create header for the http request
my_headers = {
    'accept': 'application/json;odata=verbose',
    'content-type': 'application/json;odata=verbose',
    'odata': 'verbose',
    'X-RequestForceAuthentication': 'true'
    }
if not hasattr(s, 'cookie'):
    print('authentication failed!')
    quit()
else:
    # This will return a Requests response object.
    # See the requests documentation for details.
    # s.get() returns Requests response object
    reply = s.getfile(url, filename='DASHBOARD.xlsx')
    print(reply.status_code)
    print(reply.raw)
