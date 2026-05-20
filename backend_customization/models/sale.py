# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sequence = fields.Integer(string="Sequence", default=1)