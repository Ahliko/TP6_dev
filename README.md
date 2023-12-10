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


🌞 `chat_server_ii_6.py` et `chat_client_ii_6.py`

[chat_server_ii_6.py](part2/chat_server_ii_6.py)
```bash
python part2/chat_server_ii_6.py -p <PORT> -a <HOST>
python part2/chat_client_ii_6.py -p <PORT> -a <HOST>
```


## III. Bonus

[chat_server_iii_1.py](bonus/server.py)

```bash
pip install aioconsole
pip install python-dotenv
python bonus/server.py
```

[chat_client_iii_1.py](bonus/client.py)

```bash
python bonus/client.py
```

Ce qui est fait :
- [x] Ajout d'un fichier `config` pour la configuration serveur
- [x] Ajout des arguments de lancement pour le client
- [x] Gestions des couleurs
- [x] Gestion d'ID par UUID
- [x] Encodage maison
- [x] Re-identification à la reconnection
- [x] Gestion de message personnalisé