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

from openerp.osv import osv, orm, fields
import logging

_logger = logging.getLogger(__name__)


class ir_cron(osv.Model):
    _inherit = 'ir.cron'

    def exec_manually(self, cr, uid, ids, context):
        for job in self.browse(cr, uid, ids, context):
            _logger.info('User id: %s, manually started job: %s.%s "%s"' % (
                uid, job.model, job.function, job.args)
            )
            self._callback(
                cr, job.user_id.id, job.model, job.function, job.args, job.id)
            return True
