# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('VERSION') as fd:
    version = fd.read().strip()

setup(
    name="odoo-customer",
    version=version,
    description="Odoo Implementation Project for Customer",
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    author="Open Source Integrators",
    author_email="contact@opensourceintegrators.com",
    url="https://www.opensourceintegrators.com",
    packages=['songs'] + ['songs.%s' % p for p in find_packages('./songs')],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
