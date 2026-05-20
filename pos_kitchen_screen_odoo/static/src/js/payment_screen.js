/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        const res = await super.validateOrder(...arguments);
        var line = []
        var self = this;
        var order_name = this.pos.selectedOrder.uid
        await this.orm.call("pos.order", "check_order_status", ["", order_name]).then(function(result) {
            if (result == false) {
                self.kitchen_order_status = false
                self.popup.add(ErrorPopup, {
                    title: _t("Order is Completed"),
                    body: _t("There Order is Completed please create a new Order"),
                });
            } else {
                self.kitchen_order_status = true
            }
        });
        if (self.kitchen_order_status) {
            await this.pos.sendOrderInPreparationUpdateLastChange(this.currentOrder);
            for (const orders of this.pos.selectedOrder.orderlines) {
                line.push([0, 0, {
                    'qty': orders.quantity,
                    'price_unit': orders.price,
                    'price_subtotal': orders.quantity * orders.price,
                    'price_subtotal_incl': orders.quantity * orders.price,
                    'discount': orders.discount,
                    'product_id': orders.product.id,
                    'tax_ids': [
                        [6, false, []]
                    ],
                    'id': 29,
                    'pack_lot_ids': [],
                    'full_product_name': orders.product.display_name,
                    'price_extra': orders.price_extra,
                    'name': 'newsx/0031',
                    'is_cooking': true,
                    'customer_note': orders.customerNote
                }])
            }
            var orders = [{
                'pos_reference': this.pos.get_order().uid,
                'session_id': 1,
                'amount_total': 0,
                'amount_paid': 0,
                'amount_return': '0',
                'amount_tax': 2.18,
                'lines': line,
                'is_cooking': true,
                'order_status': 'draft',
                'company_id': this.pos.company.id,
                'session_id': this.currentOrder.pos_session_id,
                'hour': self.currentOrder.date_order.c.hour,
                'minutes': self.currentOrder.date_order.c.minute,
                'config_id': this.pos.get_order().pos.config.id
            }]
            await self.orm.call("pos.order", "get_details", ["", self.pos.config.id, orders])
        }
        return res;
    }
});