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
import logging
import openerp
import base64
import contextlib
import cStringIO
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools.misc import get_iso_codes
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)
_logger = logging.getLogger(__name__)


class base_language_export(osv.osv_memory):
    _inherit = 'base.language.export'

    # Utility:
    def clean_folder_name(value):
        value = '%s' % (value, )
        for c in ['[', ','. '.', ']', '(', ')', '-']:
            value = value.replace(c, '')
        return value
    def act_save_all_file(self, cr, uid, ids, context=None):
        ''' Get po file and save in folder for installed module
        '''
        # Pool used:
        module_pool = self.pool.get('ir.module.module')
        
        path = '~/etl/translate'
        path = os.path.expanduser(path)
        os.system('mkdir -p \'%s\'' % path)
        
        lang = 'it_IT' 
        module_ids = module_pool.search(cr, uid, [
            ('state', '=', 'installed'),
            ], context=context)

        for module in module_pool.browse(cr, uid, module_ids, context=context):
            name = module.name
            author = clean_folder_name(module.author)
            mods = [name]
            
            with contextlib.closing(cStringIO.StringIO()) as buf:
                tools.trans_export(lang, mods, buf, 'po', cr)
                out_buf = buf.getvalue()

            if author:
                path_in = os.path.join(path, author)
                os.system('mkdir -p \'%s\'' % path_in)
            else:
                path_in = path
                    
            filename = '%s.it.po' % name
            filename = os.path.join(path_in, filename)

            _logger.info('Generate: %s' % filename)
            f = open(filename, 'w')
            f.write(out_buf)
            f.close()
        _logger.info('End export po files!')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
