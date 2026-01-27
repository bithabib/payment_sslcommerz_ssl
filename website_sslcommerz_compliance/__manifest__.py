# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website SSLCommerz Compliance',
    'version': '1.0',
    'category': 'Website/Website',
    'sequence': 100,
    'summary': 'E-commerce compliance for SSLCommerz payment gateway requirements',
    'description': " ",
    'depends': [
        'website_sale',
        'website_sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/website_pages_data.xml',
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
        'views/website_footer_templates.xml',
        'views/website_product_templates.xml',
        'views/website_checkout_templates.xml',
        'views/snippets/payment_banner_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sslcommerz_compliance/static/src/scss/compliance.scss',
            'website_sslcommerz_compliance/static/src/js/checkout_agreement.js',
        ],
        'web.assets_backend': [
            'website_sslcommerz_compliance/static/src/js/website_builder_redirect_patch.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
