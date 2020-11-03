# Copyright (c) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def main(ctx):
    """ Set the VERSION of the database """
    config = ctx.env["ir.config_parameter"]
    version = config.search([("key", "=", "VERSION")])
    if not version:
        config.create({"key": "VERSION", "value": "12.0.0.0.1"})
