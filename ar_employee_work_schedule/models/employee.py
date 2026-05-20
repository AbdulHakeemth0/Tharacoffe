# -*- coding: utf-8 -*-

import json
from email.policy import default

from odoo import api, fields, models, tools, _
import base64
from markupsafe import Markup


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def send_message_by_whatsapp(self):
        # partner_id = self.env.context.get('partner', False)
        partner_id = self.user_partner_id

        # working_schedule_report = self.env.ref('ar_employee_work_schedule.action_report_employee_work_schedule')._render_qweb_pdf(self.id)[0]
        working_schedule_report = self.env['ir.actions.report'].with_context(force_report_rendering=True)._render_qweb_pdf('ar_employee_work_schedule.action_report_employee_work_schedule', res_ids=self.id)
        pdf_data = working_schedule_report[0]
        encoded_report = base64.b64encode(pdf_data).decode('utf-8')
        attachment = self.env['ir.attachment'].create({
            'name': f"{self.name} - Working Schedule.pdf",
            'type': 'binary',
            'datas': encoded_report,  # Make sure to encode the PDF as base64
            'res_model': 'hr.employee',
            'res_id': self.id,
        })

        if partner_id:
            provider_id = self.env['provider'].search([('graph_api_authenticated', '=', True)], limit=1)
            # template_id = self.env['wa.template'].search([('name', '=', 'partner_welcome_template'), ('state', '=', 'added')], limit=1)
            template_id = self.env['wa.template'].search([('is_employee_schedule_template', '=', True), ('state', '=', 'added')], limit=1)
            wizard_rec = self.env['wa.compose.message'].with_context(active_model='res.partner',
                                                                     active_id=partner_id.id,
                                                                     default_body=Markup("<p>Here is your updated working schedule.</p>"),
                                                                     ).create(
                {'partner_id': partner_id.id, 'provider_id': provider_id.id,
                 # 'template_id': template_id.id,
                 # 'body': Markup("<p>Here is your updated working schedule.</p>"),
                 'attachment_ids': [(6, 0, attachment.ids)], #have to work on this - need to generate employee work schedule report and attach it here.
                 })
            wizard_rec.onchange_template_id_wrapper()
            return wizard_rec.send_whatsapp_message()
