import logging
import database
logger = logging.getLogger(__name__)

'''
displays the currently vulnerable packages from the personal database
'''
def display_vulnerable_packages():
    vulnerable_packages = database.retrieve_vulnerable_packages()

    if not vulnerable_packages:
        logger.info('no vulnerable packages found.')

    return list(vulnerable_packages)
 
def return_amount_of_vulnerable_packages():
    amount = database.count_vulnerable_packages()
    
    if not amount:
        logger.info('no vulnerbale packages found.')

    return amount

amount = return_amount_of_vulnerable_packages()
print(amount)
