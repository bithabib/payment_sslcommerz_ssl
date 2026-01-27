/** @odoo-module **/

/**
 * SSLCommerz Compliance - Checkout Terms Agreement
 *
 * Ensures the terms agreement checkbox is checked before the customer
 * can proceed with payment. The checkbox is blank by default and
 * the customer must check it to proceed.
 */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ComplianceTermsAgreement = publicWidget.Widget.extend({
    selector: '.compliance-terms-agreement',
    events: {
        'change #compliance_terms_checkbox': '_onCheckboxChange',
    },

    start() {
        this._super(...arguments);
        this._updatePaymentButton();
        // Watch for dynamically loaded payment buttons
        this._observer = new MutationObserver(() => this._updatePaymentButton());
        const paymentArea = document.querySelector('#payment_method') || document.body;
        this._observer.observe(paymentArea, { childList: true, subtree: true });
        return Promise.resolve();
    },

    destroy() {
        if (this._observer) {
            this._observer.disconnect();
        }
        const buttons = document.querySelectorAll('button[name="o_payment_submit_button"]');
        buttons.forEach(btn => {
            btn.classList.remove('disabled');
            btn.removeAttribute('disabled');
        });
        this._super(...arguments);
    },

    _onCheckboxChange() {
        this._updatePaymentButton();
    },

    _updatePaymentButton() {
        const checkbox = this.el.querySelector('#compliance_terms_checkbox');
        if (!checkbox) return;

        const buttons = document.querySelectorAll('button[name="o_payment_submit_button"]');
        buttons.forEach(btn => {
            if (checkbox.checked) {
                btn.classList.remove('disabled');
                btn.removeAttribute('disabled');
            } else {
                btn.classList.add('disabled');
                btn.setAttribute('disabled', 'disabled');
            }
        });
    },
});

export default publicWidget.registry.ComplianceTermsAgreement;
