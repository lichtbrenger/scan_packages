import database


amount = database.count_vulnerable_packages()

if not amount:
    print('no packages found.')

print(amount)
