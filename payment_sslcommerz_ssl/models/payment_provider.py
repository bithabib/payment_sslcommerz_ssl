# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_sslcommerz_ssl import const


_logger = get_payment_logger(__name__, const.SENSITIVE_KEYS)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('sslcommerz', "SSLCommerz")],
        ondelete={'sslcommerz': 'set default'}
    )
    sslc_store_id = fields.Char(
        string="SSLCommerz Store ID",
        required_if_provider='sslcommerz',
        copy=False,
    )
    sslc_store_pass = fields.Char(
        string="SSLCommerz Store Password",
        required_if_provider='sslcommerz',
        copy=False,
        groups='base.group_system',
    )

    # === CRUD METHODS === #

    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        self.ensure_one()
        if self.code != 'sslcommerz':
            return super()._get_default_payment_method_codes()
        return const.DEFAULT_PAYMENT_METHOD_CODES

    # === BUSINESS METHODS === #

    def _sslcommerz_get_urls(self):
        """ Return the SSLCommerz callback URLs.

        Note: self.ensure_one()

        :return: A dictionary with the callback URLs.
        :rtype: dict
        """
        self.ensure_one()
        base_url = self.get_base_url()
        _logger.info("SSLCommerz callback URLs: %s", base_url)

        # remove '/' from last if exists
        if '/' == base_url[-1]:
            base_url = base_url[:-1]

        return {
            "success_url": f"{base_url}/payment/sslcommerz/return",
            "fail_url": f"{base_url}/payment/sslcommerz/return",
            "cancel_url": f"{base_url}/payment/sslcommerz/return",
            "ipn_url": f"{base_url}/payment/sslcommerz/webhook",
        }

    def _sslcommerz_get_api_url(self):
        """ Return the API URL according to the provider state.

        Note: self.ensure_one()

        :return: The API URL.
        :rtype: str
        """
        self.ensure_one()
        if self.state == 'enabled':
            return 'https://securepay.sslcommerz.com'
        else:
            return 'https://sandbox.sslcommerz.com'
