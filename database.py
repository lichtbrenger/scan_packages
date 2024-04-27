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
