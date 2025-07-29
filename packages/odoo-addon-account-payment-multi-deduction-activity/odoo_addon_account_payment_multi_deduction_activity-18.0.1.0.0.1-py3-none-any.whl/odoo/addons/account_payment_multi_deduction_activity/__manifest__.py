# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Payment Register Diff - Activity",
    "version": "18.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/ecosoft-odoo/budgeting",
    "category": "Accounting",
    "depends": [
        "account_payment_multi_deduction",
        "budget_activity",
    ],
    "data": [
        "wizard/account_payment_register_views.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["ps-tubtim", "Saran440"],
}
