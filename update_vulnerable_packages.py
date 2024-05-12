import subprocess
import database

vln_packages = database.retrieve_vulnerable_packages()
if not vln_packages:
    print('no vulnerable packages found.')

update_packages = []
for vln_package in vln_packages:
    update_packages.append(vln_package[1])


command = ['sudo', 'dnf', '-y', 'update'] + update_packages
subprocess.run(command)

database.update_packages()
