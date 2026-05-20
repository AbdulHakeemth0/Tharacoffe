# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _, Command
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)


class PosSession(models.Model):
    _inherit = 'pos.session'

    cash_for_counter = fields.Monetary(
        string="Cash for Counter",
        readonly=True)

    # higher_authorities = fields.Many2many('res.partner', compute='_compute_higher_authorities')
    higher_authority = fields.Many2one('res.partner', compute='_compute_higher_authorities')

    def _compute_higher_authorities(self):
        for rec in self:
            rec.higher_authority = self.env['res.partner'].search([('is_higher_authority', '=', True)]).id

    def update_closing_cash_for_counter(self, cash_for_counter):
        """
        Calling this method will try store the cash_for_counter during the session closing.

        """
        self.ensure_one()
        self.cash_for_counter = cash_for_counter
        return {'successful': True}

    def action_pos_session_open(self):
        """
        This method will update the opening cash as cash_for_counter during the session opening.
        """
        res = super().action_pos_session_open()
        for session in self.filtered(lambda session: session.state == 'opening_control'):
            if session.config_id.cash_control and not session.rescue:
                last_session = self.search([('config_id', '=', session.config_id.id), ('id', '!=', session.id)],
                                           limit=1)
                session.cash_register_balance_start = last_session.cash_for_counter  # defaults to 0 if lastsession is empty

        return res

    def report_to_higher_authority(self, args):
        """
        This method will report Opening balance issues to higher authorities.
        """
        # mail_template_id = self.env.ref('ar_pos_closing_enhanced.mail_template_pos_closing_bal_mail')
        # mail_template_id.send_mail(self.id, force_send=True)
        mail = self.env['mail.mail'].sudo().create({
            'subject': _('Report: POS Opening Cash - %s' % self.name),
            'email_from': self.env.user.email,
            # 'email_to': self.higher_authority.email,
            'recipient_ids': self.higher_authority.ids,
            'body_html': args,
        })
        mail.send()

        return True
