import requests
import itertools
import string
import asyncio
import aiohttp
import time
from tqdm import tqdm


# Configurable constants
BATCH_SIZE = 1_000
WORD_SIZE = 4
MAX_WORKERS = 12


def generate_words():
    return (''.join(word) for word in itertools.product(string.ascii_lowercase, repeat=WORD_SIZE))


async def try_word_async(session, base_url, word):
    url = f"{base_url}/guess/{word}"
    start_time = time.time()
    async with session.get(url) as response:
        duration = time.time() - start_time
        return word, response.status, duration


async def brute_force_api_async(base_url):
    total_words = 26 ** WORD_SIZE
    start_time = time.time()
    words_tried = 0
    duration = 0

    max_duration = -100
    min_duration = 100

    max_rps = -100
    min_rps = 100

    async with aiohttp.ClientSession() as session:
        with tqdm(total=total_words, unit="word") as pbar:
            tasks = []
            for batch in batch_words(generate_words(), BATCH_SIZE):
                for word in batch:
                    task = asyncio.create_task(try_word_async(session, base_url, word))
                    tasks.append(task)

                for task in asyncio.as_completed(tasks):
                    word, status_code, req_duration = await task
                    words_tried += 1
                    pbar.update(1)

                    elapsed_time = time.time() - start_time
                    requests_per_second = words_tried / elapsed_time
                    duration += req_duration
                    avg_duration = duration / words_tried

                    max_rps = max(max_rps, requests_per_second)
                    min_rps = min(min_rps, requests_per_second)

                    max_duration = max(max_duration, avg_duration)
                    min_duration = min(min_duration, avg_duration)

                    pbar.set_postfix({
                        "RPS": f"{requests_per_second:.2f}",
                        "Last": word,
                        "req_avg": f"{avg_duration:.2f}"
                    })

                    if status_code == 200:
                        pbar.close()
                        print(f"\nSuccess! The correct word is: {word}")
                        print(f"The time took to guess the word was: {elapsed_time:.2f} seconds")
                        print("-" * 88)
                        print(f"The average request duration was: {avg_duration:.2f} seconds")
                        print(f"The longest request duration was: {max_duration:.2f} seconds")
                        print(f"The shortest request duration was: {min_duration:.2f} seconds")
                        print("-" * 88)
                        print(f"The requests per second was: {requests_per_second:.2f}")
                        print(f"The max requests per second was: {max_rps:.2f}")
                        print(f"The min requests per second was: {min_rps:.2f}")
                        return word
                    elif status_code != 400:
                        pbar.close()
                        print(f"\nUnexpected status code: {status_code}")
                        return None
                tasks = []  # Clear the tasks list for the next batch

    pbar.close()
    print("\nNo successful guess found")
    return None


def batch_words(iterable, n):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == n:
            yield batch
            batch = []
    if batch:
        yield batch


if __name__ == "__main__":
    base_url = "https://jbx.co.za"
    asyncio.run(brute_force_api_async(base_url))
