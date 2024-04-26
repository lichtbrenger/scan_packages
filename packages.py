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
Fetch rows from database
'''
def retrieve_rows():
    operating_system = retrieve_operating_system()
    if operating_system == 'fedora':
        conn = sqlite3.connect('/var/lib/dnf/history.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT name,version FROM rpm")
        rows = cursor.fetchall()
        conn.close()
        return rows

'''
Create a local copy of the existing database
'''
def create_personal_database():
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

    operating_system = retrieve_operating_system()
    if operating_system == 'fedora':
        conn_dest = sqlite3.connect('./packages.sqlite')
        cursor_dest = conn_dest.cursor()
        cursor_dest.execute('''CREATE TABLE IF NOT EXISTS packages
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, version TEXT, vulnerable INTEGER)''')
        for row in rows:
            cursor_dest.execute("INSERT INTO packages (name, version) VALUES (?, ?)", (row[1], row[2]))


'''
Updates vulnerable packages using a local sqlite database.
'''
def update_vulnerable_packages():
    conn = sqlite3.connect('./packages.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
            ALTER TABLE products
            ADD COLUMN vulnerable BOOLEAN DEFAULT FALSE;
            ''')
    conn.commit()


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


'''
The function retrieves installed packages using regular expressions.
Taking into account the operating system that is being used.
We return a dictionary with the package name and package version.
This could also be done using dnf list installed | awk '{print $1}'
'''
def get_installed_packages():
    package_dictionary = []
    if subprocess.call(['which', 'apt-get']) == 0:
        process = subprocess.Popen(['dpkg', '-l'], stdout=subprocess.PIPE)
        output, _ = process.communicate()

        return 'not implemented yet'

    if subprocess.call(['which', 'yum']) == 0:
        process = subprocess.Popen(['rpm', '-qa'], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        list_packages = output.decode('utf-8').split('\n')
        pattern = r'\d+(\.\d+)+'
        for package in list_packages:
            # Get the version of the package
            pattern = r'(\d+(\.\d+)*(-\d+)*)'
            match = re.search(pattern, package)
            if match:
                version = match.group()
            # Get the name of the package
            pattern = r'^([a-zA-Z0-9-]+)-[0-9]+(\.[0-9]+)*' \
                     '(-[a-zA-Z0-9]+)*(-[a-zA-Z0-9_.]+)*(-[a-zA-Z0-9]+)*$'
            match = re.match(pattern, package)
            if match:
                package_name = match.group(1)
            package_info = { 'name': package_name, 'version': version, 'vulnerable': 'undecided' }
            package_dictionary.append(package_info)


        return package_dictionary

    else:
        return "Unsupported package manager."

retrieve_rows()
