# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    inv_type = fields.Selection([
        ('tax_inv', 'Tax Invoice'), ('bill_supply', 'Bill of Supply')
    ], string='Invoice Type', default='tax_inv')
    state_id = fields.Many2one('res.country.state', string='State')
    transportation_mode = fields.Char(string='Transportation Mode')
    vehicle_no = fields.Char(string='Vehicle No')
    date_supply = fields.Date(string='Date of Supply')
    place_dispatch = fields.Char(string='Place of Dispatch')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    hs_no = fields.Char(string='HS No')

    @api.depends('display_type')
    def _compute_sequence(self):
        seq_map = {
            'tax': 10000,
            'rounding': 11000,
            'payment_term': 12000,
        }
        for line in self:
            line.sequence = seq_map.get(line.display_type, 1)

class AccountTax(models.Model):
    _inherit = 'account.tax'

    split_tax = fields.Boolean(string='Split Tax on Report')