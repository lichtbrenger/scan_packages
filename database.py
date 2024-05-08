#!/usr/bin/env python3
'''
This module handles operations on the loca database.
'''

import subprocess
import re
import os
import sqlite3

def retrieve_db_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id,name,version FROM packages")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_newly_installed_packages():
    os_packages = set(retrieve_packages())
    database_packages = set(retrieve_db_packages())
    new_packages = database_packages.difference(os_packages)
    if new_packages:
        # insert new packages into local sqlite db
        conn = sqlite3.connect('./packages.sqlite')
        cursor = conn.cursor()

        for package in new_packages:
            cursor.execute("INSERT INTO packages (name, version, vulnerable) VALUES (?, ?, ?)", (package[0], package[1], 2))

        conn.commit()
        conn.close()

def remove_package_from_db(package_name):
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
                    DELETE FROM packages
                    WHERE name = ?;
                    ''', (package_name))
    conn.commit()
    conn.close()

def retrieve_db_packages_name():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM packages")
    rows = cursor.fetchall()
    conn.close()
    return rows

def retrieve_packages_name():
    operating_system = retrieve_operating_system()
    if operating_system == 'fedora':
        conn = sqlite3.connect('/var/lib/dnf/history.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM rpm")
        rows = cursor.fetchall()
        conn.close()
        return rows


def discard_uninstalled_packages():
    os_packages = set(retrieve_packages_name())
    database_packages = set(retrieve_db_packages_name())
    uninstalled_packages = database_packages - os_packages
    uninstalled_packages = list(uninstalled_packages)
    for uninstalled_package in uninstalled_packages:
        remove_package_from_db(uninstalled_package)

def update_package(package):
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE packages
            SET version = ?, vulnerable = ?
            WHERE id = ?;
            ''', (package[0], 2, package[1]))

    conn.commit()
    conn.close()

def update_packages():
    os_packages = retrieve_packages()
    db_packages = retrieve_db_packages()
    for db_package in db_packages:
        for os_package in os_packages:
            if db_package[1] == os_package[0]:
                if db_package[2] != os_package[1]:
                    update_package((db_package[0], os_package[1]))
