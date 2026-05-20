/** @odoo-module */
import { CashOpeningPopup } from "@point_of_sale/app/store/cash_opening_popup/cash_opening_popup";
import { patch } from "@web/core/utils/patch";

import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { _t } from "@web/core/l10n/translation";

patch(CashOpeningPopup.prototype, {
    async report_to_higher_authority() {
        this.orm.call("pos.session", "report_to_higher_authority", [
            this.pos.pos_session.id,
            this.state.opening_cash_comments
        ]);
        alert("Email Sent")
    }
});
