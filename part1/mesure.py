import asyncio
from time import perf_counter
import web_sync_multiple
import web_async_multiple


if __name__ == '__main__':
    debut = perf_counter()
    web_sync_multiple.main()
    print(f"Temps d'exécution : {perf_counter() - debut:.2f} secondes.")
    debut = perf_counter()
    asyncio.run(web_async_multiple.main())
    print(f"Temps d'exécution : {perf_counter() - debut:.2f} secondes.")