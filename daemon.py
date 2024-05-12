import os
import sys
import scan
import logging
import multiprocessing
import threading
import time
import resource


'''
Define the work that each worker should be assigned.
In this case each worker will check a package from the personal database
continuously. When the scan did not complete successfully we stop the scanning process of that worker.
'''
def worker_function(task_id):
    while True:
        successful = scan.check_package()
        if not successful:
            logger.error('package could not be successfully checked.')
            break


'''
Main function were we create a number of workers equivalnt to the number of CPU cores.
Afterward we will put the work to work asynchronously.
'''
def start_process():
    # configure logging
    logger = logging.basicConfig(level=logging.INFO, filename='daemon.log', filemode='w', format='%(message)s')

    # Define the number of worker processes
    num_workers = multiprocessing.cpu_count()  # Use the number of CPU cores

    try:
        for i in range(num_workers):
            threading.Thread(target=worker_function, args=(i,)).start()

        # Keep the main process alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info('program stopped')

start_process()
