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

- [II. Chat room](#ii-chat-room)
  - [2. Première version](#2-première-version)
  - [3. Client asynchrone](#3-client-asynchrone)
  - [4. Un chat fonctionnel](#4-un-chat-fonctionnel)
  - [5. Gérer des pseudos](#5-gérer-des-pseudos)
  - [6. Déconnexion](#6-déconnexion)

## 2. Première version



🌞 `chat_server_ii_2.py`

[chat_server_ii_2.py](part2/chat_server_ii_2.py)
```bash
python part2/chat_server_ii_2.py
```

🌞 `chat_client_ii_2.py`

[chat_client_ii_2.py](part2/chat_client_ii_2.py)
```bash
python part2/chat_client_ii_2.py
```
## 3. Client asynchrone


🌞 `chat_client_ii_3.py`

[chat_client_ii_3.py](part2/chat_client_ii_3.py)
```bash
pip install aioconsole
python part2/chat_client_ii_3.py
```

🌞 `chat_server_ii_3.py`

[chat_server_ii_3.py](part2/chat_server_ii_3.py)
```bash
python part2/chat_server_ii_3.py
```

## 4. Un chat fonctionnel


🌞 `chat_server_ii_4.py`

[chat_server_ii_4.py](part2/chat_server_ii_4.py)
```bash
python part2/chat_server_ii_4.py
```

## 5. Gérer des pseudos


🌞 `chat_client_ii_5.py`

[chat_client_ii_5.py](part2/chat_client_ii_5.py)
```bash
python part2/chat_client_ii_5.py -p <PORT> -a <HOST>
```

🌞 `chat_server_ii_5.py`

[chat_server_ii_5.py](part2/chat_server_ii_5.py)
```bash
python part2/chat_server_ii_5.py -p <PORT> -a <HOST>
```

## 6. Déconnexion

Enfin, gérer proprement la déconnexion des clients.

Pendant vos tests, vous avez du apercevoir des comportements rigolos quand un client est coupé pendant que le serveur tourne.

Quand un client se déconnecte, il envoie un message vide facilement reconnaissable. Idem si le serveur se déconnecte, il envoie au client un message vide assez reconnaissable.

🌞 `chat_server_ii_6.py` et `chat_client_ii_6.py`

- côté client, si le serveur se déco
  - afficher un message et quitter l'app
- côté serveur, si un client se déco
  - l'enlever du dictionnaire global `CLIENTS`
  - envoyer un message à tout le monde comme quoi `Annonce : <PSEUDO> a quitté la chatroom`

## III. Bonus

Document dédié à la partie III. [Bonus](./bonus.md)