# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    # Company compliance information
    compliance_company_name = fields.Char(
        string="Company Name",
        help="Company name to display in compliance pages"
    )
    compliance_trade_license = fields.Char(
        string="Trade License Number",
        help="Trade license number to display in footer/about us"
    )
    compliance_tin_number = fields.Char(
        string="TIN Certificate Number",
        help="TIN certificate number to display in footer/about us"
    )
    compliance_registered_address = fields.Text(
        string="Registered Address",
        help="Registered address as per trade license"
    )
    compliance_contact_email = fields.Char(
        string="Contact Email"
    )
    compliance_contact_phone = fields.Char(
        string="Contact Phone"
    )

    # Delivery information
    compliance_delivery_dhaka = fields.Char(
        string="Delivery Time (Inside Dhaka)",
        default="3-5 working days"
    )
    compliance_delivery_outside = fields.Char(
        string="Delivery Time (Outside Dhaka)",
        default="7-10 working days"
    )

    # Refund timeline
    compliance_refund_timeline = fields.Char(
        string="Refund Timeline",
        default="7-10 working days",
        help="Standard refund processing timeline"
    )

    # Enable/disable compliance features
    compliance_show_trade_license = fields.Boolean(
        string="Show Trade License in Footer",
        default=True
    )
    compliance_show_stock_quantity = fields.Boolean(
        string="Show Stock Quantity on Products",
        default=True
    )
    compliance_require_terms_agreement = fields.Boolean(
        string="Require Terms Agreement at Checkout",
        default=True
    )
    compliance_show_payment_banner = fields.Boolean(
        string="Show Payment Banner in Footer",
        default=True
    )
