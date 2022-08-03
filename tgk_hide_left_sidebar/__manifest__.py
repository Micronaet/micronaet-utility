# -*- coding: utf-8 -*-
{
    'name': "Hide Left Sidebar",

    'summary': """
        Hide left sidebar""",

    'description': """
        Hide left sidebar
    """,

    'author': "Tepat Guna Karya",
    'website': "http://www.tepatguna.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Misc',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/tgk_hide_left_sidebar_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'price': 3,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'license': 'OPL-1',
}
