/** @odoo-module **/

import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import { registry } from "@web/core/registry";

console.log("TEST___")
export class ReceiptScreenCustom extends ReceiptScreen {
    setup() {
        super.setup();
        // Your additional setup code
    }

    onSendWhatsapp() {
        const order = this.currentOrder;
        const orderName = order.get_name();
        const order_server_id = this.pos.validated_orders_name_server_id_map[orderName];
        return this.orm.call("pos.order", 'action_send_invoice_via_whatsapp', [[order_server_id]]);
    }
}

//registry.category("pos_screens").add('custom_receipt_screen', OriginalReceiptScreen);
//registry.category("pos_screens").add("ReceiptScreen", ReceiptScreen);
