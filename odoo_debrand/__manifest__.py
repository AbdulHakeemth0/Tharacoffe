# -*- coding: utf-8 -*-

{
    'name': 'Odoo Debrand',
    'category': 'Hidden',
    'description': """ Odoo Debrand """,
    'version': '17.0',
    'depends': [
        'web',
        'mail'
    ],
    'data': [
        'views/res_config_settings.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_debrand/static/src/js/webclient.js',
        ]
    },
    'installable': True,
    'application': True,
}
