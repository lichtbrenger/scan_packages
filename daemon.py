import os
import sys
import time
import multiprocessing
import scan

'''
Define the work that each worker should be assigned.
In this case each worker will check a package from the personal database
continuously. When the scan did not complete successfully we stop the scanning process of that worker.
'''
def worker_function(task_id):
    while True:
        successful = scan.check_package()
        if not successful:
            break

'''
Limit the CPU usage because it will be a continuous process that is run in the background.
We do this via the nice function and assign a below normal priority.
more information: https://en.wikipedia.org/wiki/Nice_(Unix)
'''
def limit_cpu():
    p = psutil.Process(os.getpid())
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)


'''
Main function were we create a number of workers equivalnt to the number of CPU cores.
Afterward we will put the work to work asynchronously.
'''
def start_process():
    # Create a pool of worker processes
    pool = multiprocessing.Pool(None, limit_cpu)

    # Define the number of worker processes
    num_workers = multiprocessing.cpu_count()  # Use the number of CPU cores

    try:
        # Submit tasks to the pool
        for i in range(num_workers):
            pool.apply_async(worker_function, args=(i,))

        # Keep the main process alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pool.terminate()
        pool.join()

start_process()
