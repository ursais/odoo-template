# Copyright (c) 2021 Gray Matter Logic
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import logging
import os
from base64 import b64encode

import anthem
from pkg_resources import resource_string
from ..common import req



@anthem.log
def setup_admin_user(env):
    """Setup admin user"""
    admin = env.ref("base.user_admin")
    admin.write(
        {
            "new_password": os.environ.get("ODOO_ADMIN_USER_PASSWORD"),
            "tz": os.environ.get("ODOO_ADMIN_USER_TIMEZONE"),
        }
    )
    admin._set_new_password()

@anthem.log
def setup_company(env):
    """Setup company"""
    logo_content = resource_string(req, "songs/data/images/logo.png")
    b64_logo = b64encode(logo_content)

    values = {
        "name": "Gray Matter Logic",
        "street": "PO Box 940",
        "zip": "85236",
        "state_id": env.ref("base.state_us_3").id,
        "city": "Higley",
        "country_id": env.ref("base.us").id,
        "phone": "+1 (855) 811-2377",
        "email": "contact@graymatterlogic.com",
        "website": "https://www.graymatterlogic.com",
        "vat": "",
        "logo": b64_logo,
        "currency_id": env.ref("base.USD").id,
    }
    env.ref("base.main_company").write(values)


@anthem.log
def main(ctx):
    setup_company(ctx)
    setup_admin_user(ctx)
