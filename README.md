# TP6 : Chat room

## Sommaire

- [TP6 : Chat room](#tp6--chat-room)
    - [Sommaire](#sommaire)
    - [I. Débuts avec l'asynchrone](#i-débuts-avec-lasynchrone)
    - [II. Chat Room](#ii-chat-room)
    - [III. Bonus](#iii-bonus)

## I. Débuts avec l'asynchrone

# I. Faire joujou avec l'asynchrone

- [I. Faire joujou avec l'asynchrone](#i-faire-joujou-avec-lasynchrone)
    - [1. Premiers pas](#1-premiers-pas)
    - [2. Web Requests](#2-web-requests)

## 1. Premiers pas

🌞 **`sleep_and_print.py`**

[sleep_and_print.py](part1/sleep_and_print.py)

```bash
python part1/sleep_and_print.py
```

🌞 **`sleep_and_print_async.py`**

[sleep_and_print_async.py](part1/sleep_and_print_async.py)

```bash
python part1/sleep_and_print_async.py
```

## 2. Web Requests

🌞 **`web_sync.py`**

[web_sync.py](part1/web_sync.py)

```bash
pip install requests
python part1/web_sync.py https://www.ynov.com
```

🌞 **`web_async.py`**

[web_async.py](part1/web_async.py)

```bash
pip install aiohttp
pip install aiofiles
python part1/web_async.py https://www.ynov.com
```

🌞 **`web_sync_multiple.py`**

[web_sync_multiple.py](part1/web_sync_multiple.py)

```bash
import requests
python part1/web_sync_multiple.py urls.txt
```

🌞 **`web_async_multiple.py`**

[web_async_multiple.py](part1/web_async_multiple.py)

```bash
pip install aiohttp
pip install aiofiles
python part1/web_async_multiple.py urls.txt
```

🌞 **Mesure !**

[mesure.py](part1/mesure.py)

```bash
pip install requests
pip install aiohttp
pip install aiofiles
python part1/mesure.py urls.txt
```

## II. Chat Room

Document dédié à la partie II. [Chat Room](./chat_room.md)

## III. Bonus

Document dédié à la partie III. [Bonus](./bonus.md)