/* @odoo-module */

import { discussSidebarCategoriesRegistry } from "@mail/discuss/core/web/discuss_sidebar_categories";
import { patch } from "@web/core/utils/patch";
import { DiscussAppCategory } from "@mail/core/common/discuss_app_category_model";
import { compareDatetime } from "@mail/utils/common/misc";

discussSidebarCategoriesRegistry.add(
    "WpChannels",
    {
//        predicate: (store) => store.discuss.WpChannels.threads.some((thread) => thread?.is_pinned),
        value: (store) => store.discuss.WpChannels,
     },
    { sequence: 30 }
);

// CHANGES FOR SORTING
patch(DiscussAppCategory.prototype, {
    /**
     * @param {import("models").Thread} t1
     * @param {import("models").Thread} t2
     */
    sortThreads(t1, t2) {
        if (this.id === "WpChannels") {
            return (
                compareDatetime(t2.lastInterestDateTime, t1.lastInterestDateTime) || t2.id - t1.id
            );
        }
        return super.sortThreads(t1, t2);
    },
});
