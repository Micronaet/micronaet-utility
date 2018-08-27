# -*- encoding: utf-8 -*-
##########################################################################
#
#    Neobis Execute Scheduled Job Manually.
#    Copyright (C) 2012-2013 Neobis ICT Dienstverlening BV
#    <http://www.neobis.nl>
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License as published by the Free Software Foundation, either
#    version 3 of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public
#    License along with this program.  If not, see
#    <http://www.gnu.org/licenses/>.
#
##########################################################################
{
    'name' : 'Neobis Execute Scheduled Job Manually',
    'version' : '0.1',
    'author': 'Neobis ICT Dienstverlening B.V.',
    'category' : 'other',
    'website': 'http://www.neobis.nl',
    'depends' : [
        "base",
    ],
    'description' : """
Adds a button to a scheduled job, to execute it manually.
""",
    'data': [
        "views/ir_cron.xml",
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}