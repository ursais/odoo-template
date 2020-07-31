# Copyright (c) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
from base64 import b64encode

import anthem
from pkg_resources import resource_string

from .common import req


@anthem.log
def setup_account(ctx):
    """ Setup Accounting """
    pass


@anthem.log
def setup_company(ctx):
    """ Setup company """
    # load logo on company
    logo_content = resource_string(req, "data/images/logo-osi.png")
    b64_logo = b64encode(logo_content)

    values = {
        "name": "Open Source Integrators",
        "street": "PO Box 940",
        "zip": "85236",
        "state_id": ctx.env.ref("base.state_us_3").id,
        "city": "Higley",
        "country_id": ctx.env.ref("base.us").id,
        "phone": "+1 (855) 877-2377",
        "email": "contact@opensourceintegrators.com",
        "website": "https://www.opensourceintegrators.com",
        "vat": "",
        "logo": b64_logo,
        "currency_id": ctx.env.ref("base.USD").id,
    }
    ctx.env.ref("base.main_company").write(values)
    ctx.env.ref("base.main_company").partner_id.customer = True


@anthem.log
def setup_general(ctx):
    """ Setup General Settings """
    pass


@anthem.log
def setup_helpdesk(ctx):
    """ Setup Helpdesk """
    pass


@anthem.log
def setup_project(ctx):
    """ Setup Project """
    pass


@anthem.log
def setup_purchase(ctx):
    """ Setup Purchase """
    pass


@anthem.log
def setup_sale(ctx):
    """ Setup Sale """
    pass


@anthem.log
def setup_stock(ctx):
    """ Setup Stock """
    pass


@anthem.log
def set_version(ctx):
    """ Set the VERSION of the database """
    config = ctx.env["ir.config_parameter"]
    version = config.search([("key", "=", "VERSION")])
    if not version:
        config.create({"key": "VERSION", "value": "13.0.0.0.1"})


@anthem.log
def main(ctx):
    setup_company(ctx)
    setup_general(ctx)
    setup_account(ctx)
    setup_stock(ctx)
    setup_purchase(ctx)
    setup_sale(ctx)
    setup_project(ctx)
    setup_helpdesk(ctx)
    set_version(ctx)
