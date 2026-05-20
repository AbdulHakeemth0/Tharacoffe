# -*- coding: utf-8 -*-

import json

from odoo import api, fields, models, tools, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_agent = fields.Boolean(string='Is Agent')

    def open_agent_applicants(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Applicants'),
            'res_model': 'hr.applicant',
            'domain': [('agent_id', '=', self.id)],
            'context': {
                'create': False,
                'edit': False,
            },
            'views': [[False, 'tree'], [False, 'kanban'], [False, 'form']],
        }

    def open_agent_employees(self):
        agent_employees = self.env['hr.applicant'].search([('agent_id', '=', self.id)]).emp_id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Employees'),
            'res_model': 'hr.employee',
            'domain': [('id', 'in', agent_employees.ids)],
            'context': {
                'create': False,
                'edit': False,
            },
            'views': [[False, 'tree'], [False, 'kanban'], [False, 'form']],
        }