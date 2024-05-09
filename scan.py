#!/usr/bin/env python3
'''
This module scans installed packages
'''

import os
import database
import re
import requests
import json

'''
Checks vulnerabilities of the given package
using a local version of the national vulnerability database.
We try to find a match with the CPE id by using seperators (:) together with the package
name and version.
e.g. cpe:2.3:a:zlib:zlib:1.1.4:*:*:*:*:*:*:*
Because sqlite does not support booleans we use integers to represent the state of the package
2 = not scanned yet
1 = not vulnerable 
0 = vulnerable
'''
def check_vulnerabilities_online(package):
    package = list(package)
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={package[1]}"
    response = requests.get(url)
    response_data = response.json()
    string_data = json.dumps(response_data)

    search_strings = [r':'+package[1]+':', r':'+package[2]+':']
    patterns = [re.compile(pattern) for pattern in search_strings]
    if patterns[0].search(string_data):
        if patterns[1].search(string_data):
            package[3] = 0
            return
    package[3] = 1

    return tuple(package)

'''
displays the currently vulnerable packages from the personal database
'''
def display_vulnerable_packages():
    vulnerable_packages = database.retrieve_vulnerable_packages()
    print(vulnerable_packages)
   
'''
Retrieves an unchecked package from the personal database.
Then checks that package for vulnerabilities.
It updates the status of the package to either vulnerable or not vulnerable.
'''
def check_package():
    installed_package = database.retrieve_package()
    if not installed_package:
        return False
    checked_package = check_vulnerabilities_online(installed_package)
    database.update_package(checked_package)
    return True

while True:
    check_package()
