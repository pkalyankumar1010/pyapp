import os
import time

def ping_url(url):
    while True:
        response = os.system(f"ping -n 1 {url}")
        if response == 0:
            print(f"{url} is reachable")
        else:
            print(f"{url} is not reachable")
        time.sleep(10)

if __name__ == "__main__":
    url = input("Enter URL to ping: ")
    ping_url(url)
