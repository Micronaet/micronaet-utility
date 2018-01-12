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
import xlsxwriter
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)


_logger = logging.getLogger(__name__)

class ExcelWriter(orm.Model):
    """ Model name: ExcelWriter
    """    
    _name = 'excel.writer'
    _description = 'Excel writer'
    
    # -------------------------------------------------------------------------
    # UTILITY:
    # -------------------------------------------------------------------------
    def _create_workbook(self):
        ''' Create workbook in a temp file
        '''
        now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        now = now.replace(':', '_').replace('-', '_').replace(' ', '_')
        filename = '/tmp/wb_%s.xlsx' % now
             
        _logger.info('Start create file %s' % filename)
        self._WB = xlsxwriter.Workbook(filename)
        self._WS = {}
        self._filename = filename

    def _close_workbook(self, ):
        ''' Close workbook
        '''
        self._WS = {}
        try:
            self._WB.close()            
        except:            
            _logger.error('Error closign WB')    
        self._WB = False # remove object in instance

    def create_worksheet(self, name=False):
        ''' Create database for WS in this module
        '''
        try:
            if not self._WB:
                self._create_workbook()                 
            _logger.info('Using WB: %s' % self._WB)
        except:
            self._create_workbook()                
            
        self._WS[name] = self._WB.add_worksheet(name)
        
    def return_attachment(self, cr, uid, name, name_of_file, context=None):
        ''' Return attachment passed
            name: Name for the attachment
            name_of_file: file name downloaded
            context: context passed
        '''
        if context is None: 
            context = {
                'lang': 'it_IT',
                }

        # Pool used:                
        attachment_pool = self.pool.get('ir.attachment')
        self._close_workbook() # if not closed maually
        b64 = open(self._filename, 'rb').read().encode('base64')
        attachment_id = attachment_pool.create(cr, uid, {
            'name': name,
            'datas_fname': name_of_file,
            'type': 'binary',
            'datas': b64,
            'partner_id': 1,
            'res_model': 'res.partner',
            'res_id': 1,
            }, context=context)

        _logger.info('Return XLSX file: %s' % self._filename)
        return {
            'type' : 'ir.actions.act_url',
            'url': '/web/binary/saveas?model=ir.attachment&field=datas&'
                'filename_field=datas_fname&id=%s' % attachment_id,
            'target': 'self',
            }
        
    def merge_cell(self, WS_name, rectangle, default_format=''):
        ''' Merge cell procedure:
            WS: Worksheet where work
            rectangle: list for 2 corners xy data: [0, 0, 10, 5]
            default_format: setup format for cells
        '''
        if default_format:
            rectangle.append(default_format)
            
        self._WS[WS_name].merge_range(*rectangle)
        return 
             
    def write_xls_line(self, WS_name, row, line, default_format=False):
        ''' Write line in excel file:
            WS: Worksheet where find
            row: position where write
            line: Row passed is a list of element or tuple (element, format)
            default_format: if present replace when format is not present
            
            @return: nothing
        '''
        col = 0
        for record in line:
            if type(record) == bool:
                record = ''
            if type(record) not in (list, tuple):
                self._WS[WS_name].write(row, col, record)                
            elif len(record) == 2: # Normal text, format
                self._WS[WS_name].write(row, col, *record)
            else: # Rich format
                self._WS[WS_name].write_rich_string(row, col, *record)
            col += 1
        return True
        
    def column_width(self, WS_name, columns_w):
        ''' WS: Worksheet passed
            columns_w: list of dimension for the columns
        '''
        col = 0
        for w in columns_w:
            self._WS[WS_name].set_column(col, col, w)
            col += 1
        return True
        
    def get_format(self, key):  
        ''' Database for format cells
            key: mode of format
        '''
        WB = self._WB # Create with start method
        
        # Save database in self:
        if not self._wb_format:
            self._wb_format = {
                # -------------------------------------------------------------
                # Used when key not present:
                # -------------------------------------------------------------
                'default' : WB.add_format({
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    }),

                # -------------------------------------------------------------
                # Format text:
                # -------------------------------------------------------------
                'title' : WB.add_format({
                    'bold': True, 
                    'font_name': 'Courier 10 pitch',
                    'font_size': 11,
                    'align': 'left',
                    }),
                'header': WB.add_format({
                    'bold': True, 
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'center',
                    'valign': 'vcenter',
                    'bg_color': '#cfcfcf', # grey
                    'border': 1,
                    #'text_wrap': True,
                    }),
                'text': WB.add_format({
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    }),
                'text_center': WB.add_format({
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'center',
                    'border': 1,
                    }),
                    
                # -------------------------------------------------------------
                # With text color:
                # -------------------------------------------------------------
                'bg_red': WB.add_format({
                    'bold': True, 
                    'font_color': 'black',
                    'bg_color': '#ff420e',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    }),
                'bg_green': WB.add_format({
                    'bold': True, 
                    'font_color': 'black',
                    'bg_color': '#99cc66',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    }),
                'bg_order': WB.add_format({
                    'bold': True, 
                    'font_color': 'black',
                    'bg_color': '#cc9900',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'right',
                    'border': 1,
                    'num_format': num_format,
                    }),

                # -------------------------------------------------------------
                # With text color:
                # -------------------------------------------------------------
                'text_black': WB.add_format({
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    'text_wrap': True
                    }),
                'text_blue': WB.add_format({
                    'font_color': 'blue',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    'text_wrap': True
                    }),
                'text_red': WB.add_format({
                    'font_color': '#ff420e',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    'text_wrap': True
                    }),
                'text_green': WB.add_format({
                    'font_color': '#328238', ##99cc66
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    'text_wrap': True
                    }),
                'text_grey': WB.add_format({
                    'font_color': '#eeeeee',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    }),                
                'text_wrap': WB.add_format({
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    'text_wrap': True,
                    }),
                'text_bg_yellow': WB.add_format({
                    'bold': True, 
                    'font_color': 'black',
                    'bg_color': '#ffff99',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'border': 1,
                    }),                
                'number': WB.add_format({
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'right',
                    'border': 1,
                    'num_format': num_format,
                    }),
                'number_blue': WB.add_format({
                    'font_color': 'blue',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'right',
                    'border': 1,
                    'num_format': num_format,
                    }),
                'text_total': WB.add_format({
                    'bold': True, 
                    'font_color': 'black',
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'left',
                    'bg_color': '#DDDDDD',
                    'border': 1,
                    #'text_wrap': True,
                    }),
                'number_total': WB.add_format({
                    'bold': True, 
                    'font_name': 'Courier 10 pitch',
                    'font_size': 9,
                    'align': 'right',
                    'bg_color': '#DDDDDD',
                    'border': 1,
                    'num_format': num_format,
                    }),
                }
        
        # Return format or default one's
        return self._wb_format.get(
            key, 
            self._wb_format.get('default'),
            )
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
