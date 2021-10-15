# Copyright (C) 2021 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Elearning Content",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Training Content and Documentation",
    "author": "Open Source Integrators",
    "maintainer": "Open Source Integrators",
    "website": "https://www.opensourceintegrators.com",
    "depends": ["website_slides"],
    "data": [
        "data/slide.channel.csv",
        # Odoo Interface
        "data/00-interface/slide.slide.csv",
        "data/00-interface/slide.slide.xml",
        # Accounting
        "data/10-account/slide.slide.csv",
        # Inventory
    ],
    "application": True,
    "maintainers": ["ursais"],
}
