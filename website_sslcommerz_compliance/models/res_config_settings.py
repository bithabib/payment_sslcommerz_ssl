# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Company compliance information
    compliance_company_name = fields.Char(
        related='website_id.compliance_company_name',
        readonly=False
    )
    compliance_trade_license = fields.Char(
        related='website_id.compliance_trade_license',
        readonly=False
    )
    compliance_tin_number = fields.Char(
        related='website_id.compliance_tin_number',
        readonly=False
    )
    compliance_registered_address = fields.Text(
        related='website_id.compliance_registered_address',
        readonly=False
    )
    compliance_contact_email = fields.Char(
        related='website_id.compliance_contact_email',
        readonly=False
    )
    compliance_contact_phone = fields.Char(
        related='website_id.compliance_contact_phone',
        readonly=False
    )

    # Delivery information
    compliance_delivery_dhaka = fields.Char(
        related='website_id.compliance_delivery_dhaka',
        readonly=False
    )
    compliance_delivery_outside = fields.Char(
        related='website_id.compliance_delivery_outside',
        readonly=False
    )

    # Refund timeline
    compliance_refund_timeline = fields.Char(
        related='website_id.compliance_refund_timeline',
        readonly=False
    )

    # Enable/disable compliance features
    compliance_show_trade_license = fields.Boolean(
        related='website_id.compliance_show_trade_license',
        readonly=False
    )
    compliance_show_stock_quantity = fields.Boolean(
        related='website_id.compliance_show_stock_quantity',
        readonly=False
    )
    compliance_require_terms_agreement = fields.Boolean(
        related='website_id.compliance_require_terms_agreement',
        readonly=False
    )
    compliance_show_payment_banner = fields.Boolean(
        related='website_id.compliance_show_payment_banner',
        readonly=False
    )
