# Copyright (c) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem

from ..common import load_csv, load_users_csv


@anthem.log
def import_account_account(ctx):
    """ Importing accounts from csv """
    load_csv(ctx, "data/demo/account.account.csv")


@anthem.log
def import_res_groups(ctx):
    """ Importing groups from csv """
    load_csv(ctx, "data/demo/res.groups.csv")


@anthem.log
def import_res_users(ctx):
    """ Importing users """
    load_users_csv(ctx, "data/demo/res.users.csv", ",")


@anthem.log
def main(ctx):
    # import_res_groups(ctx)
    # import_res_users(ctx)
    # import_account_account(ctx)
    pass
