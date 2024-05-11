import subprocess
import re
import os
import logging
import sqlite3
logger = logging.getLogger(__name__)

'''
Determines the operating system and return the local
database that is used for storing data about packages
'''
def determine_os_database():
    os_dict = { 'operating system': '', 'database location': '', 'query': [] }
    if subprocess.call(['which', 'apt-get']) == 0:
        os_dict['operating system'] = 'ubuntu'
        os_dict['database location'] = '/var/lib/apt/lists/sources.sqlite3'
        os_dict['query'] = 'select name,version form rpm'
    if subprocess.call(['which', 'yum']) == 0:
        os_dict['operating system'] = 'fedora'
        os_dict['database location'] = '/var/lib/dnf/history.sqlite'
        os_dict['query'] = ['select name,version form rpm', 'select name from rpm']

    if os_dict['operating system'] and os_dict['database location'] and os_dict['query']:
        logger.info(f'found operating system: {os_dict["operating system"]}')
        return os_dict

    logger.error('Operating system and corresponding database could not be found.')

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

determine_os_database()
