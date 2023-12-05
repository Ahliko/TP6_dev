from time import perf_counter
import asyncio


async def printer(nb=1):
    print(nb)
    await asyncio.sleep(0.5)
    if nb == 10 or nb >= 20:
        return
    return await printer(nb + 1)


async def main():
    debut = perf_counter()
    tasks = [printer(), printer(11)]
    await asyncio.gather(*tasks)
    print(f"Temps d'exécution : {perf_counter() - debut:.2f} secondes.")


if __name__ == '__main__':
    asyncio.run(main())
