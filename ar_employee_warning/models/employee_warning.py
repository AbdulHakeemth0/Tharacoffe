# -*- coding: utf-8 -*-

import json
from email.policy import default

from odoo import api, fields, models, tools, _


class EmployeeWarning(models.Model):
    _name = 'employee.warning'
    _description = 'Employee Warning'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    # warning_type = fields.Selection([
    #     ('waring_1', 'Warning Letter To Employee For Customer Complaint'),
    #     ('waring_2', 'Warning Letter to Employee for Poor Performance'),
    #     ('waring_3', 'Warning Letter to Employee for Absenteeism'),
    #     ('waring_4', 'Warning letter to the Employee for Misconduct or Violating Rules'),
    #     ('waring_5', 'Warning letter for Unprofessional Behaviour'),
    #     ('waring_6', 'Warning Letter for Coming Late'),
    #     ('waring_7', 'Warning Letter For Irregular Attendance'),
    #     ('waring_8', 'Warning Letter to Employee for Misconduct'),
    # ], required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    signed_attachment = fields.Binary(string='Signed Attachment')
    warning_template = fields.Html(string='Warning Template')
    warning_note = fields.Text('Warning Note')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_warning_ids = fields.Many2many('employee.warning', string='Employee Warning',
                                            compute='_compute_employee_warning')
    employee_warning_count = fields.Integer('Repair part count', compute="_compute_employee_warning")

    def _compute_employee_warning(self):
        for rec in self:
            employee_warnings = self.env['employee.warning'].search([('employee_id', '=', rec.id)])
            rec.employee_warning_ids = [(6, 0, employee_warnings.ids)]
            rec.employee_warning_count = len(employee_warnings)

    def action_view_employee_warning(self):
        return {
            'name': _('Employee Warnings'),
            'view_mode': 'tree,form',
            'res_model': 'employee.warning',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('id', 'in', self.employee_warning_ids.ids)],
        }
