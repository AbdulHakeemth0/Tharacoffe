{
    "name": "POS Closing Popup Enhanced",
    "version": "17.0.0.1",
    "summary": """ 
            POS Closing Popup Enhanced
            .""",
    "description": """ 
            POS Closing Popup Enhanced
            .""",
    "depends": ["point_of_sale"],
    "author": "AR",
    "category": "Point of Sale",
    "installable": True,
    "data": [
        "data/pos_mail_template.xml",
        "views/pos_session.xml",
        "views/res_partner.xml",
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ar_pos_closing_enhanced/static/src/**/*',
        ],
    },
}
