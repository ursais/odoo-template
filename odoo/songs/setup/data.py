# Copyright (c) 2023 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import os

import anthem

from ..common import load

VERSION = os.path.split(os.path.dirname(__file__))[1]


@anthem.log
def import_account(ctx):
    """Import Accounts"""
    load(ctx, VERSION + "/" + "account.account.csv")


@anthem.log
def import_journal(ctx):
    """Import Journals"""
    load(ctx, VERSION + "/" + "account.journal.csv")


@anthem.log
def main(ctx):
    """Data"""
    # import_account(ctx)
    # import_journal(ctx)
