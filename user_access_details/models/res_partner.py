# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        user_id = self.env.user.id
        if not self.env.user.has_group('base.group_system'):
            domain = expression.AND([['|', ('create_uid', '=', user_id), ('user_id', '=', user_id)], domain])
        return super().search_fetch(domain, field_names, offset, limit, order)
