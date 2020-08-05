# Copyright (C) 2020 Open Source Integrators
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
from setuptools import find_packages, setup

setup(
    name="odoo-template",
    version="13.0.0.0.1",
    description="Odoo Template",
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    author="Open Source Integrators",
    author_email="support@opensourceintegrators.com",
    url="www.opensourceintegrators.com",
    packages=["songs"] + ["songs.%s" % p for p in find_packages("./songs")],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
