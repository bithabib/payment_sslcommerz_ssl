# Payment Provider: SSLCommerz for Odoo 19

## Description

This module integrates SSLCommerz Payment Gateway with Odoo 19. SSLCommerz is the largest payment gateway aggregator in Bangladesh, supporting multiple payment methods including credit/debit cards, mobile banking, and internet banking.

## Supported Features

- Payment with redirection flow
- Instant Payment Notification (IPN) / Webhook support
- Sandbox (Test) and Production modes
- Multiple payment methods (Cards, Mobile Banking, Internet Banking)

## Prerequisites

- Odoo 19.0
- SSLCommerz Account:
  - **For Testing**: [Create a Sandbox Account](https://developer.sslcommerz.com/registration/)
  - **For Production**: [Create a Live Merchant Account](https://join.sslcommerz.com/)

---

## Installation Guide (Step-by-Step for Beginners)

### Step 1: Download the Module

Download or clone this module to your computer.

### Step 2: Place the Module in Odoo

1. Locate your Odoo custom addons directory (usually `/odoo/custom/addons/` or similar)
2. Copy the `payment_sslcommerz_ssl` folder into that directory

### Step 3: Activate Developer Mode in Odoo

1. Log in to your Odoo instance as an administrator
2. Go to **Settings** (click the gear icon in the top menu)
3. Scroll down to the bottom of the Settings page
4. Click on **Activate the developer mode** link

![Activate Developer Mode](static/description/images/activate_developer_mode.png)

### Step 4: Update the Apps List

1. Go to **Apps** menu (the grid icon in the top menu)
2. Click on **Update Apps List** in the top menu
3. Click **Update** in the popup dialog

### Step 5: Install the Module

1. In the Apps menu, remove the "Apps" filter from the search bar
2. Search for **"SSLCommerz"** or **"payment_sslcommerz_ssl"**
3. Click **Install** on the "Payment Provider: SSLCommerz" module

---

## Configuration Guide (Step-by-Step)

### Step 1: Access Payment Providers

1. Go to **Website** > **Configuration** > **Payment Providers**

   OR

   Go to **Invoicing/Accounting** > **Configuration** > **Payment Providers**

2. Find and click on **SSLCommerz** in the list

### Step 2: Configure Credentials

#### For Testing (Sandbox Mode):

1. Get your sandbox credentials from [SSLCommerz Developer Panel](https://developer.sslcommerz.com/)
2. In the SSLCommerz payment provider form:
   - **SSLCommerz Store ID**: Enter your sandbox store ID (e.g., `testbox`)
   - **SSLCommerz Store Password**: Enter your sandbox store password (e.g., `qwerty@12345`)
   - **State**: Select **Test Mode**
3. Click **Save**

#### For Production (Live Mode):

1. Get your live credentials from your SSLCommerz Merchant Panel
2. In the SSLCommerz payment provider form:
   - **SSLCommerz Store ID**: Enter your live store ID
   - **SSLCommerz Store Password**: Enter your live store password
   - **State**: Select **Enabled**
3. Click **Save**

### Step 3: Configure Payment Methods (Optional)

1. In the payment provider form, go to the **Configuration** tab
2. Under **Payment Methods**, you can enable/disable specific payment methods
3. Under **Countries**, you can restrict which countries can use this payment method (default: Bangladesh)

### Step 4: Test the Integration

1. Go to your website's shop
2. Add a product to cart and proceed to checkout
3. At the payment step, select **SSLCommerz**
4. Complete the payment on the SSLCommerz gateway
5. You should be redirected back to your Odoo website with payment confirmation

---

## Test Credentials

Use these test credentials when in **Test Mode**:

### Test Credit Cards

**VISA**
```
Card Number: 4111111111111111
Expiry: 12/25
CVV: 111
```

**Mastercard**
```
Card Number: 5111111111111111
Expiry: 12/25
CVV: 111
```

**American Express**
```
Card Number: 371111111111111
Expiry: 12/25
CVV: 111
```

### Mobile OTP
```
OTP: 111111 or 123456
```

### Mobile Banking
Select any mobile banking option - all will work in sandbox mode.

---

## Troubleshooting

### Payment not showing at checkout?

1. Make sure the payment provider state is set to **Test Mode** or **Enabled**
2. Check that Bangladesh (BD) is in the allowed countries
3. Make sure BDT currency is configured in your Odoo

### Payment fails with error?

1. Verify your Store ID and Store Password are correct
2. Check if you're using sandbox credentials with Test Mode (or live credentials with Enabled)
3. Check Odoo logs for detailed error messages

### IPN/Webhook not working?

1. Your Odoo instance must be publicly accessible (not localhost)
2. The webhook URL is: `https://your-domain.com/payment/sslcommerz/webhook`
3. Configure this URL in your SSLCommerz merchant panel

---

## URLs Reference

| Purpose | URL |
|---------|-----|
| Return URL | `/payment/sslcommerz/return` |
| Webhook/IPN URL | `/payment/sslcommerz/webhook` |

---

## Support

- **SSLCommerz Integration Support**: integration@sslcommerz.com
- **SSLCommerz Documentation**: https://developer.sslcommerz.com/doc/v4/

---

## License

LGPL-3

---

## Credits

- **Author**: SSLCommerz
- **Maintainer**: SSLCommerz
- **Website**: https://sslcommerz.com

© 2024-2025 SSLCOMMERZ ALL RIGHTS RESERVED
