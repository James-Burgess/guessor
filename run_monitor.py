import subprocess
import time
import csv
import datetime
import json


def run_and_log(image_dir):
    timestamp = datetime.datetime.now().strftime("%s")
    output_file = f"{image_dir}_{timestamp}.csv"

    # Build the Docker image
    subprocess.run(["docker", "build", "-q", f"./{image_dir}"])

    # Run the container and capture its ID
    build_id = subprocess.check_output(["docker", "build", "-q", f"./{image_dir}"]).decode().strip()
    print(f"Built image {build_id}")
    try:
        container_id = subprocess.run(["docker", "run", "--rm", "-d", "-p", "8080:8080", build_id], capture_output=True).stdout.decode().strip()
        print(f"Server started on port 8080. Container ID: {container_id}")

        log_stats(container_id, output_file)
    finally:
        subprocess.run(["docker", "stop", container_id])
        subprocess.run(["docker", "rm", "-f", container_id])


def log_stats(container_id, output_file):
    # Create the output file with headers
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "CPU_Percent", "Memory_Usage", "Block_IO", "Memory_Percent", "PIDs", "Network_IO"])

    print(f"Starting monitoring loop. writing to {output_file}...")
    while True:
        # Get Docker stats in JSON format
        stats_json = subprocess.check_output(
            ["docker", "stats", "--no-stream", "--format", "{{json .}}", container_id]).decode()
        print(stats_json)
        # {"BlockIO":"0B / 0B","CPUPerc":"7.21%","Container":"","ID":"63778442ae5a","MemPerc":"0.06%","MemUsage":"22.25MiB / 39.02GiB","Name":"happy_kirch","NetIO":"526B / 0B","PIDs":"2"}

        stats_json = json.loads(stats_json)

        # Extract relevant metrics
        timestamp = int(time.time())
        cpu_percent = stats_json["CPUPerc"]
        memory_usage = stats_json["MemUsage"]
        memory_percent = stats_json["MemPerc"]
        network_io_received = stats_json["NetIO"]
        pids = stats_json["PIDs"]
        blkio_stats = stats_json["BlockIO"]

        # Append data to the output file
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, cpu_percent, memory_usage, blkio_stats, memory_percent, pids, network_io_received])

        time.sleep(1)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Please provide the image directory as an argument.")
        sys.exit(1)

    image_dir = sys.argv[1]
    run_and_log(image_dir)
