# Copyright (c) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem


@anthem.log
def setup_project(ctx):
    """ Setup project """
    pass


@anthem.log
def main(ctx):
    setup_project(ctx)
