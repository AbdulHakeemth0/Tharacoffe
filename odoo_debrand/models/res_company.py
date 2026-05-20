# -*- coding: utf-8 -*-

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    odoo_favicon = fields.Binary(string='Favicon')
