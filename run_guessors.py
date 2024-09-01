import subprocess
from multiprocessing import Pool

NUM_GUESSORS = 5  # Adjust as needed


def run_guessor(i):
    """Function to execute the guessor script in a separate process."""
    process = subprocess.Popen(["go", "run", "."], cwd="guessors/go_guessor")
    process.wait()  # Wait for the process to complete


if __name__ == "__main__":
    with Pool(processes=NUM_GUESSORS) as pool:
        pool.map(run_guessor, range(NUM_GUESSORS))
