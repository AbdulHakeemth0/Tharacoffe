/** @odoo-module */
import { ClosePosPopup } from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import { patch } from "@web/core/utils/patch";

import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { _t } from "@web/core/l10n/translation";

patch(ClosePosPopup.prototype, {
    //@override
    async confirm() {
        if (!this.pos.config.cash_control || this.env.utils.floatIsZero(this.getMaxDifference())) {
            await this.closeSession();
            return;
        }
        await this.closeSession();
        return;

    },

    async closeSession() {
        const res = super.closeSession();
        console.log("res___", res)
//        console.log("cash_for_counter__", this.state.payments[this.props.default_cash_details.id].cash_for_counter)
//        console.log("this.pos.config.cash_control", this.pos.config.cash_control)
//        alert(this.pos.config.cash_control);

        if (this.pos.config.cash_control) {
            const response = await this.orm.call(
                "pos.session",
                "update_closing_cash_for_counter",
                [this.pos.pos_session.id],
                {
                    cash_for_counter: parseFloat(
                        this.state.payments[this.props.default_cash_details.id].cash_for_counter
                    ),
                }
            );

            if (!response.successful) {
                return this.handleClosingError(response);
            }
        }
    }

});
