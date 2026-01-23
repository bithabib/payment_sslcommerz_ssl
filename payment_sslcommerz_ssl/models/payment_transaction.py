# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_sslcommerz_ssl import const
from odoo.addons.payment_sslcommerz_ssl.commerz.payment import SSLCSession, Validation


_logger = get_payment_logger(__name__, const.SENSITIVE_KEYS)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _compute_reference(self, provider_code, prefix=None, separator='-', **kwargs):
        """ Override of `payment` to ensure that SSLCommerz' requirements for references are satisfied.

        SSLCommerz' requirements for transaction are as follows:
        - References can only be made of alphanumeric characters and/or '-' and '_'.
          The prefix is generated with 'tx' as default. This prevents the prefix from being
          generated based on document names that may contain non-allowed characters
          (eg: INV/2020/...).

        :param str provider_code: The code of the provider handling the transaction.
        :param str prefix: The custom prefix used to compute the full reference.
        :param str separator: The custom separator used to separate the prefix from the suffix.
        :return: The unique reference for the transaction.
        :rtype: str
        """
        if provider_code == 'sslcommerz':
            prefix = payment_utils.singularize_reference_prefix()

        return super()._compute_reference(provider_code, prefix=prefix, separator=separator, **kwargs)

    def _get_specific_rendering_values(self, processing_values):
        """ Override of `payment` to return SSLCommerz-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the
                                       transaction.
        :return: The dict of provider-specific processing values.
        :rtype: dict
        """
        if self.provider_code != 'sslcommerz':
            return super()._get_specific_rendering_values(processing_values)

        provider = self.provider_id

        mypayment = SSLCSession(
            sslc_is_sandbox=provider.state != 'enabled',
            sslc_store_id=provider.sslc_store_id,
            sslc_store_pass=provider.sslc_store_pass,
        )

        urls = provider._sslcommerz_get_urls()
        mypayment.set_urls(
            success_url=urls["success_url"],
            fail_url=urls["fail_url"],
            cancel_url=urls["cancel_url"],
            ipn_url=urls["ipn_url"]
        )

        mypayment.set_product_integration(
            tran_id=self.reference,
            total_amount=self.amount,
            currency=self.currency_id.name,
            product_category="E-commerce",
            product_name=self.payment_method_id.name or "Payment",
            num_of_item=1,
            shipping_method="NO"
        )

        mypayment.set_customer_info(
            name=self.partner_id.name or "",
            email=self.partner_id.email or "",
            address1=self.partner_id.contact_address or "",
            city=self.partner_id.city or "",
            postcode=self.partner_id.zip or "",
            country=self.partner_id.country_id.name or "",
            phone=self.partner_id.phone or "",
        )

        response = mypayment.init_payment()
        _logger.info("SSLCommerz init_payment response: %s", response)

        if response.get("status") == "SUCCESS":
            return {
                'api_url': response["GatewayPageURL"],
            }
        else:
            self._set_error(_(
                "Payment initialization failed: %(reason)s",
                reason=response.get("failedreason", "Unknown error")
            ))
            return {}

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """ Override of `payment` to extract the reference from the payment data.

        :param str provider_code: The code of the provider handling the transaction.
        :param dict payment_data: The payment data sent by the provider.
        :return: The transaction reference.
        :rtype: str
        """
        if provider_code != 'sslcommerz':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('tran_id')

    def _extract_amount_data(self, payment_data):
        """Override of `payment` to extract the amount and currency from the payment data."""
        if self.provider_code != 'sslcommerz':
            return super()._extract_amount_data(payment_data)

        amount = payment_data.get('amount')
        currency_code = payment_data.get('currency')

        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }

    def _apply_updates(self, payment_data):
        """ Override of `payment` to update the transaction based on the payment data.

        :param dict payment_data: The payment data sent by the provider.
        :return: None
        """
        if self.provider_code != 'sslcommerz':
            return super()._apply_updates(payment_data)

        if not payment_data:
            self._set_canceled(state_message=_("The customer left the payment page."))
            return

        # Get the status from payment data
        status = payment_data.get('status', '').upper()
        tran_id = payment_data.get('tran_id')
        val_id = payment_data.get('val_id')

        _logger.info(
            "Processing SSLCommerz payment data for transaction %s with status %s",
            tran_id, status
        )

        # Update the provider reference
        if tran_id:
            self.provider_reference = tran_id

        # If we have a validation ID, validate with SSLCommerz API
        if val_id:
            provider = self.provider_id
            validation = Validation(
                sslc_is_sandbox=provider.state != 'enabled',
                sslc_store_id=provider.sslc_store_id,
                sslc_store_pass=provider.sslc_store_pass,
            )
            result = validation.validate_transaction(val_id)
            _logger.info("SSLCommerz validation result: %s", result)
            status = result.get("status", "").upper()

        # Update the payment state based on status
        if status in const.PAYMENT_STATUS_MAPPING['done']:
            self._set_done()
        elif status in const.PAYMENT_STATUS_MAPPING['error']:
            error_msg = payment_data.get('failedreason') or payment_data.get('error', 'Payment failed')
            self._set_error(_(error_msg))
        elif status == 'CANCELLED':
            self._set_canceled()
        else:
            _logger.warning(
                "Received data with unexpected payment status (%s) for transaction %s.",
                status, self.reference
            )
            self._set_error(_("Received data with unexpected payment status: %s", status))
