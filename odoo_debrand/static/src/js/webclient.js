/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    /**
     * @override
     */
    async setup() {
        super.setup();
        const odooTitle = await this.rpc("/get/odoo/title", {});
        if (odooTitle.length != 0) {
            this.title.setParts({zopenerp: odooTitle});
        }
    },
});