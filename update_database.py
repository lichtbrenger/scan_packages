#!/usr/bin/env python3
'''
This module handles operations on the loca database.
'''

import logging
import database
import os_interface
logger = logging.getLogger(__name__)


'''
Adds newly installed packages to the personal database.
We use Set theory by calculating the difference between the
set of packages from the personal database and the set of packages
from the operating system's database.
'''


def add_newly_installed_packages():
    os_packages = set(os_interface.retrieve_packages())
    database_packages = set(database.retrieve_packages())
    new_packages = database_packages.difference(os_packages)
    if new_packages:
        for package in new_packages:
            database.insert_package(package)


'''
Compares the operating system database
and the personal database.
When packages that are in the personal database are
not found in the operating system's database we remove that package
from the personal database.
'''


def discard_uninstalled_packages():
    os_packages = set(os_interface.retrieve_packages_name())
    database_packages = set(database.retrieve_packages_name())
    uninstalled_packages = database_packages - os_packages
    uninstalled_packages = list(uninstalled_packages)
    for uninstalled_package in uninstalled_packages:
        database.remove_package_from_db(uninstalled_package)


'''
Updates all packages using the update package function.
It retrieves all packages that are listed in the operating system and,
the personal database.
Every package is compared by name.
When a match is found, the version of the package is compared.
When there is a discrepancy we assume the package version is
outdated because the only change in version
could come an update in the operating system's database.
'''


def update_packages():
    os_packages = os_interface.retrieve_packages()
    db_packages = database.retrieve_packages()
    for db_package in db_packages:
        for os_package in os_packages:
            if db_package[1] == os_package[0]:
                if db_package[2] != os_package[1]:
                    database.update_package((db_package[0], os_package[1]))
