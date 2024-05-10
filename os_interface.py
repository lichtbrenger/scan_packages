import subprocess
import re
import os
import logging
import sqlite3
logger = logging.getLogger(__name__)

'''
This function retrieves the Operating System that is being used.
'''
def determine_os_database():
    if subprocess.call(['which', 'apt-get']) == 0:
        return '/var/lib/apt/lists/sources.sqlite3'
    if subprocess.call(['which', 'yum']) == 0:
        return '/var/lib/dnf/history.sqlite'


def retrieve_packages():
    database_location = determine_os_database()
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()
    cursor.execute("SELECT name,version FROM rpm")
    rows = cursor.fetchall()
    conn.close()
    return rows


def retrieve_packages_name():
    database_location = determine_os_database()
    conn = sqlite3.connect(database_location)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM rpm")
    rows = cursor.fetchall()
    conn.close()
    return rows


