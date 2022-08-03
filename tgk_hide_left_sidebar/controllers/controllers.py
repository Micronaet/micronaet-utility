# -*- coding: utf-8 -*-
from odoo import http

# class TgkHideLeftSidebar(http.Controller):
#     @http.route('/tgk_hide_left_sidebar/tgk_hide_left_sidebar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tgk_hide_left_sidebar/tgk_hide_left_sidebar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tgk_hide_left_sidebar.listing', {
#             'root': '/tgk_hide_left_sidebar/tgk_hide_left_sidebar',
#             'objects': http.request.env['tgk_hide_left_sidebar.tgk_hide_left_sidebar'].search([]),
#         })

#     @http.route('/tgk_hide_left_sidebar/tgk_hide_left_sidebar/objects/<model("tgk_hide_left_sidebar.tgk_hide_left_sidebar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tgk_hide_left_sidebar.object', {
#             'object': obj
#         })