#!/usr/bin/env python3
'''
This module handles operations on the loca database.
'''

import subprocess
import re
import os
import logging
import sqlite3
import os_interface
logger = logging.getLogger(__name__)

'''
retrieve all data from the packages in the 
personal database
'''
def retrieve_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT id,name,version FROM packages")
    rows = cursor.fetchall()
    conn.close()
    logger.info('successfully retrieved all packages from personal database\n')
    return rows

def insert_package(package):
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO packages (name, version, vulnerable) VALUES (?, ?, ?)", (package[0], package[1], 2))

    conn.commit()
    conn.close()
    logger.info(f'successfully added package {package} to the personal database.')

    

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

'''
Retrieves the all the names of the packages
from the personal database.
and returns a list of tupples.
'''
def retrieve_packages_name():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM packages")
    rows = cursor.fetchall()
    conn.close()
    logger.info('successfully retrieved package names from personal database.')
    return rows

'''
Updates one package given an ID.
The function takes a package and,
resets the vulnerability status to unchecked.
'''
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
    db_packages = os_interface.retrieve_packages()
    for db_package in db_packages:
        for os_package in os_packages:
            if db_package[1] == os_package[0]:
                if db_package[2] != os_package[1]:
                    update_package((db_package[0], os_package[1]))



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
        ORDER BY RANDOM()
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

def count_vulnerable_packages():
    conn = sqlite3.connect('/home/yide/scan_packages/packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*)
        FROM packages
        WHERE vulnerable == 0
    ''')
    vulnerable_packages = cursor.fetchall()

    if not vulnerable_packages:
        logger.info('No vulnerable packages found')

    return vulnerable_packages[0][0]

