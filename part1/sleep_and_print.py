from time import sleep, perf_counter


def printer(nb=1):
    print(nb)
    sleep(0.5)
    if nb == 10:
        return
    return printer(nb + 1)


if __name__ == '__main__':
    début = perf_counter()
    printer()
    printer()
    print(f"Temps d'exécution : {perf_counter() - début:.2f} secondes.")
