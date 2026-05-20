# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def search_fetch(self, domain, field_names, offset=0, limit=None, order=None):
        user_id = self.env.user.id
        if not self.env.user.has_group('base.group_system'):
            domain = expression.AND([[('create_uid', '=', user_id)], domain])
        return super().search_fetch(domain, field_names, offset, limit, order)

    @api.constrains('groups_id')
    def _check_one_user_type(self):
        access_grp = self.env.ref('base.group_erp_manager').id
        setting_grp = self.env.ref('base.group_system').id
        if not self.env.user.has_group('base.group_system') and (access_grp in self.groups_id.ids or setting_grp in self.groups_id.ids):
            raise ValidationError(_("You don't have access to apply this group please contact with your admin."))
        return super()._check_one_user_type()
