import os
import sys
import time
import multiprocessing
import logging
import scan

def worker_function(task_id):
    """Function executed by each worker process."""
    while True:
        scan.check_package()
        print('this works')
        logging.info(f"Worker {task_id} is working...")
        time.sleep(2)  # Simulate some work

def limit_cpu():
    "is called at every process start"
    p = psutil.Process(os.getpid())
    # set to lowest priority, this is windows only, on Unix use ps.nice(19)
    p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)

def main():
    # Set up logging
    logging.basicConfig(filename='./my_daemon.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Redirect standard output and error to both the log file and /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    log_file = open('./my_daemon.log', 'a')
    with open("/dev/null", "r") as dev_null:
        os.dup2(dev_null.fileno(), sys.stdin.fileno())
        os.dup2(log_file.fileno(), sys.stdout.fileno())
        os.dup2(log_file.fileno(), sys.stderr.fileno())

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
        logging.info("Interrupted, terminating processes...")
        pool.terminate()
        pool.join()
        logging.info("Processes terminated.")
    finally:
        log_file.close()

if __name__ == "__main__":
    # Daemonize the script
    main()
