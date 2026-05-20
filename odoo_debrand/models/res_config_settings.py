# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    odoo_title = fields.Char(
        string='Title', config_parameter='odoo_debrand.odoo_title'
    )
    odoo_favicon = fields.Binary(
        string='Favicon', related='company_id.odoo_favicon', readonly=False
    )

