# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StatementInvestorReport(models.AbstractModel):
    _name = 'report.ar_investor_statement_report.investor_statement_report'
    _description = 'Statement Investor Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form'].get('date_from')
        date_to = data['form'].get('date_to')
        # journal_items = self.env['account.move.line'].search([])
        journal_items = self.env['account.move.line'].search(
            [('date', '>=', date_from),
             ('date', '<=', date_to),
             ('account_id.account_type', 'in', ['equity', 'expense', 'asset_fixed', 'asset_receivable', 'income'])
             ])
        print("journal_items___", journal_items)
        return {
            'doc_model': self.env['res.company'],
            'date_from': date_from,
            'date_to': date_to,
            'docs': journal_items,
            'company': self.env.company
        }
