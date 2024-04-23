# scan_packages
scans installed packages and checks if the installed version of a package contains any vulnerabilities.

# Design
- consults a local database, nvd
- keeps a dynamic list of install packages using set theory to get the list up to date as a way to include the safety property of a package
- sqlite3 /var/lib/rpm/rpmdb.sqlite to query the rpmdb database
- SELECT name FROM sqlite_master WHERE type='table';
- uses the 
