# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import os

from anthem.lyrics.loaders import load_csv, load_csv_stream
from anthem.lyrics.records import switch_company
from pkg_resources import Requirement, resource_stream

req = Requirement.parse("odoo-songs")


def load_safe(ctx, model, path):
    try:
        load_csv(ctx, model, path)
    except Exception:
        ctx.log_line("Exception while importing {}".format(path))


def load(ctx, path):
    model = os.path.splitext(os.path.basename(path))[0]
    load_safe(ctx, model, path)


def load_users(ctx, path):
    # make sure we don't send any email
    model = ctx.env["res.users"].with_context(
        **{"no_reset_password": True, "tracking_disable": True}
    )
    load_safe(ctx, model, path)


def load_warehouses(ctx, company, path):
    # in multicompany mode we must force the company
    # otherwise the sequences that stock module generates automatically
    # will have the wrong company assigned.
    ctx.env.uid = 2
    with switch_company(ctx, company) as ctx:
        if company == ctx.env.user.company_id:
            ctx.log_line("Switched to {}".format(company.name))
            load_csv(ctx, "stock.warehouse", path)
            # NOTE: dirty hack here.
            # We are forced to load the CSV twice because
            # if you are modifying the existing base warehouse (stock.warehouse0)
            # and you've changed the `code` (short name)
            # the changes are not reflected on existing sequences
            # until you load warehouse data again.
            # We usually don't have that many WHs so... it's fine :)
            load_csv(ctx, "stock.warehouse", path)
    ctx.env.uid = 1


def get_files(default_file):
    """Check if there is a DATA_DIR in environment else open default_file.

    DATA_DIR is passed by importer.sh when importing splitted file in parallel

    Returns a generator of file to import as DATA_DIR can contain a split of
    csv file
    """
    try:
        dir_path = os.environ["DATA_DIR"]
    except KeyError:
        yield resource_stream(req, default_file)
    else:
        file_list = os.listdir(dir_path)
        for file_name in file_list:
            file_path = os.path.join(dir_path, file_name)
            yield open(file_path)


def load_csv_parallel(ctx, path, defer_parent_computation=True, delimiter=","):
    """Use me to load an heavy file ~2k of lines or more.

    Then calling this method as a parameter of importer.sh

    importer.sh will split the file in chunks per number of processor
    and per 500.
    This method will be called once per chunk in order to do the csv loading
    on multiple processes.

    Usage::

        @anthem.log
        def setup_locations(ctx):
            load_csv_parallel(
                ctx,
                'data/install/stock.location.csv',
                defer_parent_computation=True)

    Then in `migration.yml`::

        - importer.sh songs.install.inventory::setup_locations /opt/odoo/data/install/stock.location.csv
        # if defer_parent_computation=True
        - anthem songs.install.inventory::location_compute_parents

    """  # noqa
    load_ctx = ctx.env.context.copy()
    model = os.path.splitext(os.path.basename(path))[0]
    if defer_parent_computation:
        load_ctx.update({"defer_parent_store_computation": "manually"})
    if isinstance(model, str):
        model = ctx.env[model]
    model = model.with_context(**load_ctx)
    for content in get_files(path):
        load_csv_stream(ctx, model, content, delimiter=delimiter)


def deferred_compute_parents(ctx, model):
    """Use me for heavy files after calling `deferred_import`.

    Usage::

        @anthem.log
        def location_compute_parents(ctx):
            deferred_compute_parents(ctx, 'stock.location')

    """
    ctx.env[model]._parent_store_compute()
