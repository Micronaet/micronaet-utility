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

import os
import pdb
import sys
import logging

from odoo import models, fields, api
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # Generate Payment:
    def generate_payment(self):
        """ Generate payment
        """
        payment_pool = self.env['account.payment']
        invoice = self
        name = invoice.sequence_number_next or invoice.name or '/'
        currency_id = invoice.company_id.currency_id.id or 1  # todo
        journal_id = 5  # bank
        payment_type = 'inbound'
        partner_id = invoice.partner_id.id

        diff_currency = False  # inv.currency_id != company_currency
        payment_method_id = 1  # todo
        ctx = dict(self._context, lang=invoice.partner_id.lang)
        total = total_currency = invoice.manual_total
        iml = []
        if invoice.payment_term_id:
            totlines = invoice.with_context(ctx).payment_term_id.with_context(
                currency_id=currency_id).compute(
                total, invoice.date_invoice)[0]
            res_amount_currency = total_currency
            ctx['date'] = invoice._get_currency_rate_date()
            i = 0
            pdb.set_trace()
            for amount_currency, detail in enumerate(totlines):
                # last line: add the diff
                res_amount_currency -= amount_currency or 0
                if i + 1 == len(totlines):
                    amount_currency += res_amount_currency
                payment_date, amount = detail
                iml.append({
                    'payment_date': payment_date,
                    'type': 'dest',
                    'name': name,
                    'amount': t[1],
                    'partner_id': partner_id,
                    'account_id': invoice.account_id.id,
                    'date_maturity': t[0],
                    'amount_currency': diff_currency and amount_currency,
                    'currency_id': diff_currency and invoice.currency_id.id or currency_id,
                    'invoice_id': invoice.id,
                    'payment_method_id': payment_method_id,
                    'journal_id': journal_id,
                    'payment_type': payment_type,
                })
        else:
            payment_date = invoice.date_invoice
            iml.append({
                'type': 'dest',
                'name': name,
                'payment_date': payment_date,
                'amount': total,
                'partner_id': partner_id,
                'account_id': invoice.account_id.id,
                'date_maturity': invoice.date_due,
                'amount_currency': diff_currency and total_currency,
                'currency_id': diff_currency and invoice.currency_id.id or currency_id,
                'invoice_id': invoice.id,
                'payment_method_id': payment_method_id,
                'journal_id': journal_id,
                'payment_type': payment_type,

            })
        for data in iml:
            payment_pool.create(data)
    manual_total = fields.Float('Totale')

