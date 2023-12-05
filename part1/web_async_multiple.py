import sys
from time import perf_counter

import aiohttp
import asyncio
import aiofiles


async def get_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def write_content(content, file):
    async with aiofiles.open(file, mode="w") as f:
        await f.write(content)
        await f.flush()


async def main():
    file = sys.argv[1] if len(sys.argv) > 1 else print("Usage: python3 web_sync_multiple.py <file>") and sys.exit(1)
    with open(file) as f:
        urls = f.readlines()
    for url in urls:
        url = url.split('\n')[0]
        link = url.split('//')[1]
        await write_content(await get_page(url), f"/tmp/web_{link}")


if __name__ == '__main__':
    debut = perf_counter()
    asyncio.run(main())
    print(f"Temps d'exécution : {perf_counter() - debut:.2f} secondes.")
