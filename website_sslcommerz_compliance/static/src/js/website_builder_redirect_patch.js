/** @odoo-module **/

import { WebsiteBuilderClientAction } from "@website/client_actions/website_preview/website_builder_action";
import { patch } from "@web/core/utils/patch";
import { redirect } from "@web/core/utils/urls";
import { getActiveHotkey } from "@web/core/hotkeys/hotkey_service";

/**
 * Patch the website builder to use /app instead of /odoo for redirects.
 * The original code uses /odoo/action-... but /app is the standard URL prefix in Odoo 19.
 */
patch(WebsiteBuilderClientAction.prototype, {
    /**
     * @override
     * Override reloadWebClient to use /app instead of /odoo
     */
    reloadWebClient() {
        const currentPath = encodeURIComponent(window.location.pathname);
        const websiteId = this.websiteService.currentWebsite.id;
        redirect(
            `/app/action-website.website_preview?website_id=${encodeURIComponent(
                websiteId
            )}&path=${currentPath}&enable_editor=1`
        );
    },

    /**
     * @override
     * Override onKeydownRefresh to use /app instead of /odoo
     */
    onKeydownRefresh(ev) {
        const hotkey = getActiveHotkey(ev);
        if (hotkey !== "control+r" && hotkey !== "f5") {
            return;
        }
        // The iframe isn't loaded yet: fallback to default refresh.
        if (this.websiteService.contentWindow === undefined) {
            return;
        }
        ev.preventDefault();
        const path = this.websiteService.contentWindow.location;
        const debugMode = this.env.debug ? `&debug=${this.env.debug}` : "";
        redirect(
            `/app/action-website.website_preview?path=${encodeURIComponent(path)}${debugMode}`
        );
    },
});
