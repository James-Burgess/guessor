import requests

base_url = "https://jbx.co.za/guess/"

for a in range(ord('a'), ord('z') + 1):
    for b in range(ord('a'), ord('z') + 1):
        for c in range(ord('a'), ord('z') + 1):
            for d in range(ord('a'), ord('z') + 1):
                word = chr(a) + chr(b) + chr(c) + chr(d)
                full_url = base_url + word
                response = requests.get(full_url)

                if response.status_code == 200:
                    print("Success! The word is:", word)
                    break  # Exit the loop once we find the correct word
