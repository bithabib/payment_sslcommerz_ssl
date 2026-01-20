/** @odoo-module **/

/**
 * SSLCommerz Compliance - Checkout Terms Agreement
 *
 * This module ensures that the terms agreement checkbox is validated
 * before the customer can proceed with payment.
 */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ComplianceTermsAgreement = publicWidget.Widget.extend({
    selector: '.compliance-terms-agreement',
    events: {
        'change #compliance_terms_checkbox': '_onCheckboxChange',
    },

    /**
     * @override
     */
    start() {
        this._super(...arguments);
        this._updatePaymentButton();
        return Promise.resolve();
    },

    /**
     * Handle checkbox change event
     * @private
     */
    _onCheckboxChange() {
        this._updatePaymentButton();
    },

    /**
     * Enable/disable payment button based on checkbox state
     * @private
     */
    _updatePaymentButton() {
        const checkbox = this.el.querySelector('#compliance_terms_checkbox');
        const paymentForm = document.querySelector('#o_payment_form');

        if (checkbox && paymentForm) {
            const submitButtons = paymentForm.querySelectorAll('button[type="submit"], .o_payment_submit');
            submitButtons.forEach(button => {
                if (checkbox.checked) {
                    button.classList.remove('disabled');
                    button.removeAttribute('disabled');
                } else {
                    button.classList.add('disabled');
                    button.setAttribute('disabled', 'disabled');
                }
            });
        }
    },
});

export default publicWidget.registry.ComplianceTermsAgreement;
