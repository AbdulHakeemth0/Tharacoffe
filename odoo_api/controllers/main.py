# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request


class OdooApi(http.Controller):

    @http.route('/get/sales/person', type='json', methods=['GET'], auth='public')
    def get_sales_person(self, **kw):
        vals = []
        ResUsers = request.env['res.users'].sudo()
        sales_person = ResUsers.search([])
        for rec in sales_person:
            vals.append({
                'id': rec.id,
                'name': rec.name
            })
        return vals

    @http.route('/create/crm/lead', type='json', methods=['POST'], auth='public')
    def create_crm_lead(self, **kw):
        if not (kw.get('name') and kw.get('salesperson_id')):
            return {
                'success': False,
                'error': _('Could not create a crm lead.'),
                'msg': _("Required fields are missing.")
            }
        CrmLead = request.env['crm.lead'].sudo()
        lead_id = CrmLead.create({
            'type': 'lead',
            'name': kw.get('name'),
            'user_id': kw.get('salesperson_id'),
            'email_from': kw.get('email'),
            'phone': kw.get('phone')
        })
        if lead_id:
            return {
                'success': True,
                'msg': _("Successfully created a crm lead.")
            }
        else:
            return {
                'success': False,
                'error': _('Could not create a crm lead.'),
                'msg': _("Something went wrong!")
            }
