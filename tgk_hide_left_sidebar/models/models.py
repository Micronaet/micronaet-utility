# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class tgk_hide_left_sidebar(models.Model):
#     _name = 'tgk_hide_left_sidebar.tgk_hide_left_sidebar'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100