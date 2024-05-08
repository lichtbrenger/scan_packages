#!/usr/bin/env python3
'''
This module scans installed packages
'''

import os
import packages
import re
import requests

'''
Checks vulnerabilities of the given package
using a local version of the national vulnerability database.
We try to find a match with the CPE id by using seperators (:) together with the package
name and version.
e.g. cpe:2.3:a:zlib:zlib:1.1.4:*:*:*:*:*:*:*
Because sqlite does not support booleans we use integers.
2 = not scanned yet
1 = not vulnerable 
0 = vulnerable
'''

def check_vulnerabilities_online(package):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package[1]}"
    response = requests.get(url)
    response_data = response.json()
    string_data = json.dumps(response_data)

    search_strings = [r':'+package[1]+':', r':'+package[2]+':']
    patterns = [re.compile(pattern) for pattern in search_strings]
    if patterns[0].search(response_data):
        if patterns[1].search(response_data):
            package[3] = 0
            return
    package[3] = 1

    return tuple(package)

def display_vulnerable_packages():
    vulnerable_packages = packages.retrieve_vulnerable_packages()
    print(vulnerable_packages)
    
def check_package():
    installed_package = packages.retrieve_package()
    if not installed_package:
        return False
    checked_package = check_vulnerabilities_online(installed_package)
    packages.update_package(checked_package)
    return True

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

#while True:
    #check_package()
check_package()
