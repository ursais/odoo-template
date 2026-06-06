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
    try:
        dir_path = os.environ["DATA_DIR"]
    except KeyError:
        yield resource_stream(req, default_file)
    else:
        for file_name in os.listdir(dir_path):
            yield open(os.path.join(dir_path, file_name))
