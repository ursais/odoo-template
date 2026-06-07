# Copyright (c) 2021 Gray Matter Logic
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import logging
import os

import click
import click_odoo
from songs.common import create_or_update

_logger = logging.getLogger(__name__)


def reset_queue_jobs(env):
    """Reset Queue Jobs"""
    jobs = env["queue.job"].search([("state", "in", ["started", "enqueued"])])
    jobs.write({"state": "pending"})


def setup_admin_user(env):
    """Setup Admin User"""
    admin = env.ref("base.user_admin")
    admin.write(
        {
            "new_password": os.environ.get("ODOO_ADMIN_USER_PASSWORD"),
            "tz": os.environ.get("ODOO_ADMIN_USER_TIMEZONE"),
        }
    )
    admin._set_new_password()


def set_mail_server(env):
    """Set Mail Server"""
    if os.getenv("RUNNING_ENV") != "production":
        mailhog = create_or_update(
            env,
            "ir.mail_server",
            "__setup__.ir_mail_server_mailhog",
            {
                "name": "MailHog",
                "smtp_host": os.environ.get("ODOO_SMTP_SERVER", "mail"),
                "smtp_port": os.environ.get("ODOO_SMTP_PORT", 25),
            },
        )
        try:
            mailhog.test_smtp_connection()
        except Exception as exception:
            _logger.warning("Test SMTP connection to MailHog: %s", exception)


def set_ribbon(env):
    """Set Ribbon"""
    if os.getenv("RUNNING_ENV") != "production":
        background = env["ir.config_parameter"].search(
            [("key", "=", "ribbon.background.color")]
        )
        background.value = "rgba(0,128,0,.6)"
        color = env["ir.config_parameter"].search([("key", "=", "ribbon.color")])
        color.value = "#f0f0f0"
        name = env["ir.config_parameter"].search([("key", "=", "ribbon.name")])
        name.value = os.getenv("RUNNING_ENV").upper() + "<br/>({db_name})"


def set_version(env):
    """Set version in the database"""
    create_or_update(
        env,
        "ir.config_parameter",
        "__setup__.ir_database_version",
        {"key": "database.version", "value": os.getenv("VERSION", "setup")},
    )


@click.command()
@click_odoo.env_options(default_log_level="warn")
def main(env):
    setup_admin_user(env)
    set_mail_server(env)
    set_ribbon(env)
    # reset_queue_jobs(env)
    set_version(env)


if __name__ == "__main__":
    main()
