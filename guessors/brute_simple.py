import requests
import itertools
import string
import time

WORD_SIZE = 4


def generate_words():
    return (''.join(word) for word in itertools.product(string.ascii_lowercase, repeat=WORD_SIZE))


def try_word(base_url, word):
    url = f"{base_url}/guess/{word}"
    start_time = time.time()
    response = requests.get(url)
    duration = time.time() - start_time
    return word, response.status_code, duration


def brute_force_api(base_url):
    total_words = 26 ** WORD_SIZE
    start_time = time.time()
    words_tried = 0
    duration = 0

    for word in generate_words():
        word, status_code, req_duration = try_word(base_url, word)
        words_tried += 1

        elapsed_time = time.time() - start_time
        requests_per_second = words_tried / elapsed_time
        duration += req_duration
        avg_duration = duration / words_tried

        print(f"Tried: {word}, RPS: {requests_per_second:.2f}, req_avg: {avg_duration:.2f}")  # Basic output

        if status_code == 200:
            print(f"\nSuccess! The correct word is: {word}")
            print(f"The time took to guess the word was: {elapsed_time:.2f} seconds")
            print(f"The requests per second was: {requests_per_second:.2f}")
            print(f"The average request duration was: {avg_duration:.2f} seconds")
            return word
        elif status_code != 400:
            print(f"\nUnexpected status code: {status_code}")
            return None

    print("\nNo successful guess found")
    return None


if __name__ == "__main__":
    base_url = "https://jbx.co.za"
    result = brute_force_api(base_url)
