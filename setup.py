#!/usr/bin/env python3
'''
This module facalitates the creating of an
environment necessary for the app to function.
It needs to be run first in order for the app to work
'''


import subprocess
import os
import sqlite3


def create_log():
    filename = './daemon.log'
    # Check if the file exists
    if not os.path.exists('./daemon.log'):
        # Command to create a file
        command = f"touch {filename}"
        # Execute the command using subprocess.Popen
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(f"File '{filename}' created successfully.")
    else:
        print(f"File '{filename}' already exists.")


'''
This function retrieves the Operating System that is being used.
'''


def retrieve_operating_system():
    if subprocess.call(['which', 'apt-get']) == 0:
        return 'ubuntu'
    if subprocess.call(['which', 'yum']) == 0:
        return 'fedora'


'''
This function retrieves the rows of the operating system's database.
This is used to create our own database where we can add properties to
packages without altering the base system.
This also ensures easy removal
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


'''
Create the personal database where operations will be run on.
The personal database is a copy of the OS database for packages including
certain properties related to vulnerabilities.
'''


def create_database():
    filename = './packages.sqlite'
    # Check if the file exists
    if not os.path.exists('./packages.sqlite'):
        # Command to create a file
        command = f"touch {filename}"
        # Execute the command using subprocess.Popen
        process = subprocess.Popen(command,
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(f"File '{filename}' created successfully.")
    else:
        print(f"File '{filename}' already exists.")


'''
creates a table in the personal database and inserts
the installed packages that are found in the OS's
database including the vulnerability status.
'''


def insert_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS packages
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT, version TEXT, vulnerable INTEGER)
                   ''')

    packages = retrieve_packages()
    for package in packages:
        cursor.execute('''
                       INSERT INTO packages
                       (name, version, vulnerable) VALUES (?, ?, ?)
                       ''', (package[0], package[1], 2))

    conn.commit()
    conn.close()


'''
starts the setup
'''


def create_local_database():
    create_log()
    create_database()
    insert_packages()


create_local_database()
