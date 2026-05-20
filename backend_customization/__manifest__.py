# -*- coding: utf-8 -*-

{
    'name': 'Backend Customization',
    'category': 'Hidden',
    'description': """ Backend Customization """,
    'version': '17.0',
    'depends': [
        'sale',
        'account',
        'mrp',
        'purchase',
        'l10n_in'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/invoice_report.xml',
        'report/expense_report_template.xml',
        # 'report/paperformat.xml',
        'report/report_expense.xml',
        'report/external_layout.xml',
        'views/mrp.xml',
        'views/base.xml',
        # 'views/sale.xml',
        'views/accounting.xml',
        'views/contract.xml',
    ],
    'installable': True,
    'application': True,
}
