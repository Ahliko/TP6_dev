import sys
import os
from time import perf_counter

import requests as rq

args = sys.argv[1:]
if len(args) != 1:
    print("Usage: python3 web_sync.py <host>")
    sys.exit(1)

url = args[0]


def get_page(url):
    return rq.get(url).text


def write_content(content, file):
    if os.path.exists(file):
        os.remove(file)
    with open(file, "w") as f:
        f.write(content)


if __name__ == '__main__':
    debut = perf_counter()
    write_content(get_page(url), "/tmp/web_page")
    print(f"Temps d'exécution : {perf_counter() - debut:.2f} secondes.")
