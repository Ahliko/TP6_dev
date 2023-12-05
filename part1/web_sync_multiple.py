import sys
import os
from time import perf_counter
import requests as rq


def get_page(url):
    return rq.get(url).text


def write_content(content, file):
    if os.path.exists(file):
        os.remove(file)
    with open(file, "w") as f:
        f.write(content)


def main():
    file = sys.argv[1] if len(sys.argv) > 1 else print("Usage: python3 web_sync_multiple.py <file>") and sys.exit(1)
    with open(file) as f:
        urls = f.readlines()
    for url in urls:
        url = url.split('\n')[0]
        link = url.split('//')[1]
        write_content(get_page(url), f"/tmp/web_{link}")


if __name__ == '__main__':
    debut = perf_counter()
    main()
    print(f"Temps d'exécution : {perf_counter() - debut:.2f} secondes.")
