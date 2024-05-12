import subprocess
import database
'''
short script that updates the vulnerable packages
that are installed in the operating system.
'''

# get vulnerable packages
vln_packages = database.retrieve_vulnerable_packages()
if not vln_packages:
    print('no vulnerable packages found.')

# We only need the name of the package, not other metadata.
update_packages = []
for vln_package in vln_packages:
    update_packages.append(vln_package[1])

# decide on the package manager
package_manager = ''
if subprocess.call(['which', 'apt-get']) == 0:
    package_manager = 'apt-get'
if subprocess.call(['which', 'dnf']) == 0:
    package_manager = 'dnf'

# update the packages using the OS package manager
command = ['sudo', package_manager, '-y', 'update'] + update_packages
subprocess.run(command)

# update the status of the updated packages in personal database
database.update_packages()
