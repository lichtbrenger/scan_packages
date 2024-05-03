#!/usr/bin/env python3
'''
This module handles operations on the loca database.
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
Fetch rows from database
'''
def retrieve_packages():
    operating_system = retrieve_operating_system()
    if operating_system == 'fedora':
        conn = sqlite3.connect('/var/lib/dnf/history.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name,version FROM rpm")
        rows = cursor.fetchall()
        conn.close()
        return rows

def create_file():
    filename = './packages.sqlite'
    # Check if the file exists
    if not os.path.exists('./packages.sqlite'):
         # Command to create a file
        command = f"touch {filename}"
        # Execute the command using subprocess.Popen
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(f"File '{filename}' created successfully.")
    else:
        print(f"File '{filename}' already exists.")

'''
creates a table in the local database and inserts 
the installed packages
'''
def insert_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS packages
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, version TEXT, vulnerable INTEGER)''')

    packages = retrieve_packages()
    for package in packages:
        cursor.execute("INSERT INTO packages (name, version, vulnerable) VALUES (?, ?, ?)", (package[0], package[1], 2))

    conn.commit()
    conn.close()

'''
main process, creates a local copy of the existing database
'''
def create_local_database():
    create_file()
    insert_packages()

# create_local_database()

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

discard_uninstalled_packages()
