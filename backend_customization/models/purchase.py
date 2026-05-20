# -*- coding: utf-8 -*-

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends(
        'order_line.move_ids.picking_id',
        'order_line.move_ids.move_dest_ids.picking_id'
    )
    def _compute_picking_ids(self):
        super(PurchaseOrder, self)._compute_picking_ids()
        for order in self:
            if order.order_line.move_ids and order.order_line.move_ids.move_dest_ids:
                order.picking_ids += order.order_line.move_ids.move_dest_ids.mapped(
                    'picking_id'
                )
            picking_ids = self.env['stock.picking'].search(
                [('origin', '=', order.name)])
            if picking_ids:
                order.picking_ids |= picking_ids
            else:
                picking_ids = self.env['procurement.group'].search(
                    [('name', '=', order.name)])
                if picking_ids:
                    order.picking_ids |= picking_ids