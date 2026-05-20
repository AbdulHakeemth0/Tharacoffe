# -*- coding: utf-8 -*-

import json

from odoo import api, fields, models, tools, _


class UtmSource(models.Model):
    _inherit = 'utm.source'

    is_agent = fields.Boolean(string='Is Agent')
