#!/usr/bin/env python3
'''
This module scans installed packages
'''

import os
import packages
import re

'''
Checks vulnerabilities of the given package
using a local version of the national vulnerability database.
We try to find a match with the CPE id by using seperators (:) together with the package
name and version.
e.g. cpe:2.3:a:zlib:zlib:1.1.4:*:*:*:*:*:*:*
'''
def check_vulnerabilities(package):
    package = list(package)
    directory = './nvd'
    search_strings = [r':'+package[1]+':', r':'+package[2]+':']
    patterns = [re.compile(pattern) for pattern in search_strings]
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                if patterns[0].search(line):
                    if patterns[1].search(line):
                        package[3] = 0
                        return
    package[3] = 1

    return tuple(package)

    
def check_package():
    installed_package = packages.retrieve_package()
    checked_package = check_vulnerabilities(installed_package)
    packages.update_package(checked_package)

def check_all_packages():
    installed_packages = packages.get_installed_packages()
    amount_of_vulnerabilities = 0
    for package in installed_packages:
        contains_vulnerability = check_vulnerabilities(package)
        if contains_vulnerability:
            amount_of_vulnerabilities += 1

    if amount_of_vulnerabilities > 0:
        return True

    return False

check_package()
