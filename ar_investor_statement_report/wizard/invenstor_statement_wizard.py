# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class InvestorStatementWizard(models.TransientModel):
    _name = 'investor.statement.wizard'
    _description = 'Investor Statement Wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def generate_investor_statement_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'investor.statement.wizard',
            'form': data
        }
        return self.env.ref('ar_investor_statement_report.action_investor_statement_report').report_action(self.id, datas)
