# -*- coding: utf-8 -*-
{
    'name': "odoo_report",

    'summary': """
       """,

    'description': """
        
    """,

    'author': "@",
    'website': "http://www.yourcompany.com",

    'category': 'Print Tools',
    'version': '19.6.12',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/ps_print_format.xml',
        'views/menus.xml',
    ],
}
