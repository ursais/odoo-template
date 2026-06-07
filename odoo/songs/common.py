# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import csv
import io
import logging
import os

from pkg_resources import Requirement, resource_stream

_logger = logging.getLogger(__name__)

req = Requirement.parse("odoo-songs")


def create_or_update(env, model, xmlid, values):
    module, name = xmlid.split(".", 1)
    record = env.ref(xmlid, raise_if_not_found=False)
    if record is None:
        record = env[model].create(values)
        env["ir.model.data"].create(
            {"module": module, "name": name, "model": model, "res_id": record.id}
        )
    else:
        record.write(values)
    return record


def switch_company(env, company):
    return env(context=dict(env.context, allowed_company_ids=[company.id]))


def load_csv_stream(env, model, stream, delimiter=",", header=None, header_exclude=None):
    reader = csv.reader(
        io.TextIOWrapper(stream, encoding="utf-8") if isinstance(stream, io.RawIOBase)
        else io.StringIO(stream.read().decode("utf-8")),
        delimiter=delimiter,
    )
    rows = list(reader)
    if not rows:
        return
    fields = rows[0]
    if header is not None:
        fields = header
    elif header_exclude:
        fields = [f for f in fields if f not in header_exclude]
        rows = [rows[0]] + rows[1:]
    data = rows[1:]
    result = env[model].load(fields, data)
    if result.get("messages"):
        for msg in result["messages"]:
            _logger.warning("load %s: %s", model, msg)
    return result


def load_csv(env, path, delimiter=",", header=None, header_exclude=None):
    content = resource_stream(req, path)
    model = os.path.splitext(os.path.basename(path))[0]
    load_csv_stream(
        env,
        model,
        content,
        delimiter=delimiter,
        header=header,
        header_exclude=header_exclude,
    )


def load_users_csv(env, path, delimiter=","):
    env["res.users"].with_context(no_reset_password=True, tracking_disable=True)
    load_csv(env, path, delimiter)


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

def reset_xml_ids(ctx, model, field, changes=None):
    """
    Reset the XML IDs of existing records to easily reference them.

        Parameters:
            model (string): Name of the model
            field (string): Name of the field to use to generate the new XML ID
            changes (dictionary): {Key: Value} where Key is the old value and
            Value is the new value of the field
    """
    # Force the XML ID to allow easy import and avoid duplicate code error
    with ctx.log("Resetting XML IDs of %s" % model):
        records = ctx.env[model].search([])
        records.export_data(["id"])
        datas = ctx.env["ir.model.data"].search(
            [("model", "=", model), ("module", "=", "__export__")]
        )
        for data in datas:
            val = str(ctx.env[model].browse(data.res_id).read([field])[0][field])
            if changes and val in changes:
                val = changes[val]
            val = (
                val.replace("-", "_")
                .replace(",", "_")
                .replace(".", "_")
                .replace(" ", "_")
            )
            data.write(
                {
                    "name": (model.replace(".", "_") + "_" + val).lower(),
                    "module": "__setup__",
                }
            )
        datas.flush_recordset()
        ctx.log_line("XML IDs of %s reset." % model)
