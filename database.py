#!/usr/bin/env python3
'''
This module handles operations on the loca database.
'''

import subprocess
import re
import os
import logging
import sqlite3
logger = logging.getLogger(__name__)

def retrieve_packages():
    operating_system = retrieve_operating_system()
    if operating_system == 'fedora':
        conn = sqlite3.connect('/var/lib/dnf/history.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name,version FROM rpm")
        rows = cursor.fetchall()
        conn.close()
        return rows

def retrieve_db_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id,name,version FROM packages")
    rows = cursor.fetchall()
    conn.close()
    logger.info('successfully retrieved all packages from personal database\n')
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
        logger.info('successfully added new packages to the personal database.')
        return

    logger.info('No new packages were found.')


def remove_package_from_db(package_name):
    try:
        conn = sqlite3.connect('./packages.sqlite')
        cursor = conn.cursor()

        cursor.execute('''
                        DELETE FROM packages
                        WHERE name = ?;
                        ''', (package_name))
        conn.commit()
        conn.close()
        logger.info(f'deleted {package_name} from personal database.')
        
    except sqlite3.Error as e:
        logger.error(f'The following error was encountered:\n{e}.')


def retrieve_db_packages_name():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM packages")
    rows = cursor.fetchall()
    conn.close()
    logger.info('successfully retrieved package names from personal database.')
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


'''
This function retrieves the Operating System that is being used.
'''
def retrieve_operating_system():
    if subprocess.call(['which', 'apt-get']) == 0:
        return 'ubuntu'
    if subprocess.call(['which', 'yum']) == 0:
        return 'fedora'

'''
Updates vulnerable packages using a local sqlite database.
'''
def update_package(package):
    if package:
        logger.info('updating package:' + package[1])
        conn = sqlite3.connect('./packages.sqlite')
        cursor = conn.cursor()
        cursor.execute('''
                UPDATE packages
                SET vulnerable = ?
                WHERE id = ?;
                ''', (package[3], package[0]))
        conn.commit()
        conn.close()
        return

    logger.info(f'package, {package}, could not be updated.')

def retrieve_package():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id,name,version,vulnerable
        FROM packages
        WHERE vulnerable == 2
        LIMIT 1;
    ''')
    package = cursor.fetchone()

    if not package:
        logger.info('All packages scanned')
        return
    
    logger.info('retrieved package: ' + package[1])
    return package

def retrieve_vulnerable_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id,name,version,vulnerable
        FROM packages
        WHERE vulnerable == 0
    ''')
    vulnerable_packages = cursor.fetchall()

    if not vulnerable_packages:
        logger.info('No vulnerable packages found')

    return vulnerable_packages
