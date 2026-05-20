# -*- coding: utf-8 -*-

import json
from email.policy import default

from odoo import api, fields, models, tools, _


class WATemplate(models.Model):
    _inherit = "wa.template"

    is_employee_schedule_template = fields.Boolean(string='Is Employee Work Schedule Template')