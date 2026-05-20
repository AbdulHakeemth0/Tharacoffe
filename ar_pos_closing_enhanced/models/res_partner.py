# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_higher_authority = fields.Boolean(string="Is Higher Authority")
