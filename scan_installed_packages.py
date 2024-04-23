#!/usr/bin/env python3
import subprocess
import re
import requests
import os


'''
Checks vulnerabilities of the given package
using a local version of the national vulnerability database.
We try to find a match with the CPE id by using seperators (:) together with the package
name and version.
e.g. cpe:2.3:a:zlib:zlib:1.1.4:*:*:*:*:*:*:*
'''
def check_vulnerabilities(package):
    directory = './nvd'
    search_strings = [r':'+package["name"]+':', r':'+package["version"]+':']
    patterns = [re.compile(pattern) for pattern in search_strings]
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            for line_number, line in enumerate(file, 1):
                if patterns[0].search(line):
                    if patterns[1].search(line):
                        package["vulnerable"] = 'yes'
                        return

    package["vulnerable"] = 'no'

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

    elif subprocess.call(['which', 'yum']) == 0:
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
            pattern = r'^([a-zA-Z0-9-]+)-[0-9]+(\.[0-9]+)*(-[a-zA-Z0-9]+)*(-[a-zA-Z0-9_.]+)*(-[a-zA-Z0-9]+)*$'
            match = re.match(pattern, package)
            if match:
                package_name = match.group(1)
            package_info = { 'name': package_name, 'version': version, 'vulnerable': undecided }
            package_dictionary.append(package_info)


        return package_dictionary

    else:
        return "Unsupported package manager."

def check_all_packages():
    installed_packages = get_installed_packages()
    amount_of_vulnerabilities = 0
    for package in installed_packages:
        contains_vulnerability = check_vulnerabilities(package)
        if contains_vulnerability:
            amount_of_vulnerabilities += 1

    if amount_of_vulnerabilities > 0:
        return True

    return False
