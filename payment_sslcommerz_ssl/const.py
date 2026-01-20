# Part of Odoo. See LICENSE file for full copyright and licensing details.

# The codes of the payment methods to activate when SSLCommerz is activated.
DEFAULT_PAYMENT_METHOD_CODES = {
    'sslcommerz',
}

# Mapping of transaction states to SSLCommerz payment statuses.
PAYMENT_STATUS_MAPPING = {
    'done': ('VALIDATED', 'VALID', 'validated', 'valid'),
    'error': ('FAILED', 'DECLINED', 'INVALID', 'CANCELLED'),
}

# Keys to be masked in logs for security reasons.
SENSITIVE_KEYS = (
    'store_passwd',
    'sslc_store_pass',
    'verify_sign',
)
