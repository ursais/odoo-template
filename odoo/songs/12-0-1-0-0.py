# Copyright (c) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def setup_account(ctx):
    """ Setup Accounting """
    pass


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
    version = ctx.env("ir.config.parameter").search([("key", "=", "VERSION")])
    version.write({"value": "12.0.1.0.0"})


@anthem.log
def main(ctx):
    setup_general(ctx)
    setup_account(ctx)
    setup_stock(ctx)
    setup_purchase(ctx)
    setup_sale(ctx)
    setup_project(ctx)
    setup_helpdesk(ctx)
    set_version(ctx)
