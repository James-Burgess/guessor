import subprocess
import psutil
import argparse
import time
import csv
import os
import threading

from loguru import logger


def run_script_and_log_stats(script, timeout=None):
    logger.info(f"Starting script: '{script}' with timeout: {timeout} seconds")

    csv_filename = f"run_results/resource_usage_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    os.makedirs(os.path.dirname(csv_filename), exist_ok=True)  # Create directory if it doesn't exist
    process = subprocess.Popen(script.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pid = process.pid

    # Start threads for monitoring and resource logging
    monitor_thread = threading.Thread(target=monitor_script, args=(process, timeout))
    resource_thread = threading.Thread(target=log_resource_usage, args=(pid, csv_filename))

    monitor_thread.start()
    resource_thread.start()

    # Wait for threads to complete
    monitor_thread.join()
    resource_thread.join()

    logger.info(f"Script finished with PID: {pid}")


def monitor_script(process, timeout=None):
    """
    Monitors the script's output and termination.
    """
    start_time = time.time()
    while True:
        output_line = process.stdout.readline()
        if output_line:
            print(output_line.strip())  # Immediate feedback
            logger.info(f"[Script Output] {output_line.strip()}")

        if process.poll() is not None:  # Process has terminated
            break

        if timeout and time.time() - start_time > timeout:
            logger.warning(f"Timeout reached after {timeout} seconds. Terminating script.")
            process.terminate()
            break

    error_output = process.stderr.read()
    if error_output:
        logger.error(f"[Script Error] {error_output}")


def log_resource_usage(pid, csv_filename):
    fieldnames = ['Timestamp', 'PID', 'CPU_Percent', 'Memory_MB']

    if not os.path.exists(csv_filename):
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['Timestamp', 'PID', 'CPU_Percent', 'Memory_MB']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    while True:
        try:
            proc = psutil.Process(pid)
        except psutil.NoSuchProcess:
            break  # Process has finished

        cpu_percent = proc.cpu_percent()
        memory_info = proc.memory_info()

        log_message = f"[Resource Usage] CPU: {cpu_percent}%, Memory: {memory_info.rss / 1024 ** 2:.2f} MB"
        logger.info(log_message)

        with open(csv_filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'PID': pid,
                'CPU_Percent': cpu_percent,
                'Memory_MB': memory_info.rss / 1024 ** 2
            })

        time.sleep(5)  # Log every 5 seconds


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a Python script, stream output, and log resource usage.')
    parser.add_argument('script_path', help='Path to the Python script to run.')
    parser.add_argument('-t', '--timeout', type=int, default=None, help='Optional timeout in seconds.')
    args = parser.parse_args()

    run_script_and_log_stats(args.script_path, timeout=args.timeout)
