#!/usr/bin/env python3
'''
This module handles operations on packages.
'''

import subprocess
import re
import os
import sqlite3

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
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
            UPDATE packages
            SET vulnerable = ?
            WHERE id = ?;
            ''', (package[3], package[0]))
    conn.commit()
    conn.close()

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
    return package

'''
Uses a local database to query locally installed packages.
This database is a copy of the dnf sqlite database.
returns a tupple
'''
def retrieve_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT name,version FROM rpm")
    rows = cursor.fetchall()
    conn.close()
    return rows
