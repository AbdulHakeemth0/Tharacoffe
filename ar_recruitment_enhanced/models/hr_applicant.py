# -*- coding: utf-8 -*-

import json

from odoo import api, fields, models, tools, _


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    is_agent = fields.Boolean(string='Is Agent', compute='_compute_is_agent', related='source_id.is_agent')
    agent_id = fields.Many2one('res.partner', string='Agent', domain=[('is_agent', '=', True)])
    agent_city = fields.Char(string='Agent City')

    @api.onchange('agent_id')
    def onchange_agent_id(self):
        self.agent_city = self.agent_id.city
