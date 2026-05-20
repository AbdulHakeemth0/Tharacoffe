{
    "name": "POS View Enhanced",
    "version": "17.0.0.1",
    "summary": """ 
            POS View Enhanced
            .""",
    "description": """ 
            POS View Enhanced
            .""",
    "depends": ["point_of_sale", "tus_meta_whatsapp_base"],
    "author": "AR",
    "category": "Point of Sale",
    "installable": True,
    "data": [
        'data/wa_template_pos.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ar_pos_view_enhanced/static/src/**/*',
        ],
    },
}
