# Copyright (c) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import anthem

from ..common import load_csv, load_users_csv


@anthem.log
def import_account_account(ctx):
    """ Importing accounts """
    load_csv(ctx, "data/full/account.account.csv")


@anthem.log
def import_hr_employee(ctx):
    """ Importing hr employees """
    load_users_csv(ctx, "data/full/hr.employee.csv")


@anthem.log
def import_hr_department(ctx):
    """ Importing hr departments """
    load_users_csv(ctx, "data/full/hr.department.csv")


@anthem.log
def import_res_groups(ctx):
    """ Importing groups """
    load_csv(ctx, "data/full/res.groups.csv")


@anthem.log
def import_res_users(ctx):
    """ Importing users """
    load_users_csv(ctx, "data/full/res.users.csv", ",")


@anthem.log
def import_project_time_type(ctx):
    """ Importing project time types """
    load_csv(ctx, "data/full/project.time.type.csv")


@anthem.log
def main(ctx):
    # import_res_groups(ctx)
    # import_res_users(ctx)
    # import_account_account(ctx)
    # import_hr_department(ctx)
    # import_hr_employee(ctx)
    # import_project_time_type(ctx)
