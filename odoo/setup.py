# Copyright (C) 2021 Gray Matter Logic
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from setuptools import find_packages, setup

setup(
    name="odoo-songs",
    version="19.0.1.0.0",
    description="Odoo ERP",
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    install_requires=["click-odoo"],
    author="Gray Matter Logic",
    author_email="support@graymatterlogic.com",
    url="https://graymatterlogic.com",
    packages=["songs"] + ["songs.%s" % p for p in find_packages("./songs")],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
