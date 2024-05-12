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
    os_dict = { 'operating system': '', 'database location': '', 'queries': [] }
    if subprocess.call(['which', 'apt-get']) == 0:
        os_dict['operating system'] = 'ubuntu'
        os_dict['database location'] = '/var/lib/apt/lists/sources.sqlite3'
    if subprocess.call(['which', 'yum']) == 0:
        os_dict['operating system'] = 'fedora'
        os_dict['database location'] = '/var/lib/dnf/history.sqlite'
        os_dict['queries'] = ['select name,version from rpm', 'select name from rpm']

    if os_dict['operating system'] and os_dict['database location'] and os_dict['queries']:
        logger.info(f'found operating system: {os_dict["operating system"]}')
        return os_dict

    logger.error('Operating system and corresponding database could not be found.')


def connect_to_db(database_location):
    if not database_location:
        logger.error('No database location was provided.')
        return

    try:
        conn = sqlite3.connect(database_location)
        logger.info("Connected to the database successfully.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"The error '{e}' occurred.")
        return None

def query_db(conn, query):
    if not query:
        logger.error('No query provided.')
        return None

    if not conn:
        logger.error('no connection provided.')
        return None

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            logger.error(f'could not retrieve any data using the following query: {os_dict["queries"][0]}.')
            return

        conn.close()
        return rows

    except sqlite3.Error as e:
        logger.error(f"An error occurred while querying the database: {e}")
        return None

def retrieve_packages():
    os_dict = determine_os_database()
    connection = connect_to_db(os_dict['database location'])
    packages = query_db(connection, os_dict['queries'][0])
    return packages

    

def retrieve_packages_name():
    os_dict = determine_os_database()
    connection = connect_to_db(os_dict['database location'])
    packages = query_db(connection, os_dict['queries'][1])
    return packages
