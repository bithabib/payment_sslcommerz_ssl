# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pprint

from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.http import request

from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_sslcommerz_ssl import const
from odoo.addons.payment_sslcommerz_ssl.commerz.payment import Validation


_logger = get_payment_logger(__name__, const.SENSITIVE_KEYS)


class SSLCommerzController(http.Controller):
    _return_url = "/payment/sslcommerz/return"
    _webhook_url = "/payment/sslcommerz/webhook"

    @http.route(
        _return_url,
        type="http",
        auth="public",
        methods=['GET', 'POST'],
        csrf=False,
        save_session=False,
    )
    def sslcommerz_return(self, **data):
        """ Handle the return from SSLCommerz after payment.

        The customer is redirected here after completing, failing, or cancelling payment.

        The route is configured with save_session=False to prevent Odoo from creating a new session
        when the user is redirected here via a POST request. Indeed, as the session cookie is
        created without a `SameSite` attribute, some browsers that don't implement the recommended
        default `SameSite=Lax` behavior will not include the cookie in the redirection request from
        the payment provider to Odoo. However, the redirection to the /payment/status page will
        satisfy any specification of the `SameSite` attribute, the session of the user will be
        retrieved and with it the transaction which will be immediately post-processed.

        :param dict data: The payment data sent by SSLCommerz.
        :return: A redirection to the payment status page.
        """
        _logger.info("Received SSLCommerz return data:\n%s", pprint.pformat(data))

        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference(
            'sslcommerz', data
        )
        if tx_sudo:
            tx_sudo._process('sslcommerz', data)

        return request.redirect('/payment/status')

    @http.route(_webhook_url, type="http", auth="public", methods=['POST'], csrf=False)
    def sslcommerz_webhook(self, **data):
        """ Handle SSLCommerz IPN (Instant Payment Notification) webhook.

        SSLCommerz sends IPN notifications to this endpoint to inform about payment status.

        :param dict data: The IPN data sent by SSLCommerz.
        :return: 'VALID' or 'FAIL' to acknowledge the IPN.
        :rtype: str
        """
        _logger.info("Received SSLCommerz webhook data:\n%s", pprint.pformat(data))

        # Find the transaction
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference(
            'sslcommerz', data
        )
        if not tx_sudo:
            _logger.warning(
                "Transaction not found for IPN data with tran_id: %s",
                data.get("tran_id", "Unknown")
            )
            return "FAIL"

        # Verify the notification origin
        self._verify_notification_origin(data, tx_sudo)

        # Process the payment data
        tx_sudo._process('sslcommerz', data)

        return "VALID"

    def _verify_notification_origin(self, data, tx_sudo):
        """ Verify that the IPN notification was sent by SSLCommerz.

        :param dict data: The IPN data received from SSLCommerz.
        :param payment.transaction tx_sudo: The sudoed transaction.
        :return: None
        :raise Forbidden: If the notification origin cannot be verified.
        """
        provider = tx_sudo.provider_id

        validation = Validation(
            sslc_is_sandbox=provider.state != 'enabled',
            sslc_store_id=provider.sslc_store_id,
            sslc_store_pass=provider.sslc_store_pass,
        )

        if not validation.validate_ipn_hash(data):
            _logger.warning(
                "Invalid IPN hash received for transaction: %s",
                data.get("tran_id", "Unknown")
            )
            raise Forbidden()
