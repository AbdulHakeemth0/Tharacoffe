# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request


class TermsController(http.Controller):

    @http.route('/get/odoo/title', type='json', auth="user")
    def config_parameter(self, **kwargs):
         return request.env['ir.config_parameter'].sudo().get_param('odoo_debrand.odoo_title')
