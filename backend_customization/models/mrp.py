# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    currency_id = fields.Many2one(
        "res.currency", string="Currency",
        default=lambda self: self.env.company.currency_id
    )
    labour_cost = fields.Boolean(string='Labour Cost')
    labour_cost_price = fields.Monetary(
        string='Labour Cost',
        currency_field="currency_id"
    )

    def _prepare_workorder_vals(self):
        workcenter_id = self.env['mrp.workcenter'].search([], limit=1)
        return {
            'name': 'Roasted',
            'workcenter_id': workcenter_id.id,
            'production_id': self.id,
            'product_uom_id': self.product_uom_id.id,
            'state': 'pending',
        }

    @api.constrains('move_raw_ids', 'labour_cost', 'labour_cost_price')
    def _labour_cost(self):
        for rec in self:
            if rec.labour_cost and rec.labour_cost_price:
                workorder_ids = rec.workorder_ids
                if not workorder_ids:
                    workorder_ids = self.env['mrp.workorder'].create(self._prepare_workorder_vals())
                if workorder_ids:
                    workorder_id = workorder_ids[0]
                    total_qty = sum(rec.move_raw_ids.mapped('product_uom_qty'))
                    total_mint = total_qty * rec.labour_cost_price
                    workorder_id.write({'duration': total_mint})
                    # rec.labour_cost_price = total_mint
            else:
                rec.workorder_ids.unlink()
                # rec.labour_cost_price = 0.0
