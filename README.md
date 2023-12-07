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
  - [1. Intro](#1-intro)
  - [2. Première version](#2-première-version)
  - [3. Client asynchrone](#3-client-asynchrone)
  - [4. Un chat fonctionnel](#4-un-chat-fonctionnel)
  - [5. Gérer des pseudos](#5-gérer-des-pseudos)
  - [6. Déconnexion](#6-déconnexion)

## 1. Intro

![Yet another](./img/yet_another.jpg)

L'idée de la ***chatroom*** c'est :

- **serveur**
  - écoute sur un port TCP
  - accueille des clients
  - entretient une liste de tous les clients connectés
  - à la réception d'un message d'un client, il le redistribue à tous les autres
  - **l'asynchrone** va permettre de gérer plusieurs clients "simultanément"
- **client**
  - se connecte au port TCP du serveur
  - peut envoyer des messages
  - reçoit les messages des autres
  - **l'asynchrone** va permettre d'attendre une saisie utilisateur et en même temps recevoir et afficher les messages des autres

Dans les deux cas, on va utiliser la lib Python `asyncio` pour mettre ça en place, mais on va utiliser deux choses différentes :

➜ **le serveur**

- on va utiliser la méthode `asyncio.start_server(handle_packet)` qui permet d'écouter sur un port TCP
- à chaque fois qu'un paquet est reçu, la méthode `handle_packet` (qu'on aura défini) le traite
- à chaque paquet reçu il est facile de lire le contenu, ou de formuler une réponse
- il pourra traiter en parallèle la réception/l'envoi de plusieurs messages

➜ **le client**

- on reste sur la lib `socket` pour la connexion TCP
- on pourra créer des *tasks* à exécuter de façon asynchrones :
  - une *task* pour la saisie utilisateur (le message que le user veut envoyer)
  - une *task* réception de données (les messages reçus des autres users)

## 2. Première version

Là on veut juste un truc qui ressemble de trèèès loin à un outil de chat. On va avancer ptit à ptit.

🌞 `chat_server_ii_2.py`

- utilise un `asyncio.start_server()` pour écouter sur un port TCP
- si un client se connecte
  - il affiche le message du client
  - il envoie `"Hello {IP}:{Port}"` au client
    - `{IP}` est l'IP du client
    - `{Port}` est le port utilisé par le client

> *Vous pouvez utiliser des `recv(1024)` partout pour le moment on s'en fout, on gérera des headers plus tard pour annoncer des tailles précises en bonus.*

🌞 `chat_client_ii_2.py`

- rien de nouveau pour le moment
- juste utilisation de `socket` comme aux TPs précédents
- quand le client se connecte
  - il envoie `"Hello"` au serveur
  - il attend une réponse du serveur et l'affiche

> Seul changement pour le moment, par rapport à ce qu'on a fait à avant : le serveur utilise `asyncio` pour écouter sur le port TCP. Ainsi, à chaque fois que des données sont reçues, on peut les traiter de manière concurrente (si par exemple, plus tard, deux clients envoient des données).

## 3. Client asynchrone

Adapter le code du client pour qu'il contienne deux fonctions asynchrones :

- **une qui attend une saisie utilisateur** : `async input()`
  - y'a un `while True:`
  - si le user saisit un truc
  - vous l'envoyez au serveur
- **une autre qui attend les messages du serveur** : `async_receive()`
  - y'a un `while True:` là aussi
  - si un message du serveur est reçu
  - afficher le message

Oui oui, un seul programme, deux `while True:`. Ils seront exécutés de façon concurrente, en asynchrone, grâce à `asyncio`.

➜ N'utilisez pas la fonction native `input()` de Python pour la saisie utilisateur : elle ne permet pas l'asynchrone. Il existe `aioconsole.ainput()` qui fait ça ! Il sera peut-être nécessaire d'installer le package `aioconsole`

➜ On peut pas non plus utiliser `sock.recv(1024)` comme d'hab : cette méthode `recv()` ne supporte pas `await`. Pas de `socket` en fait.

Comme chaque méthode qui génère de l'attente, il existe (probablement) une autre méthode qui fait ça en asynchrone (et qu'on peut donc await) en Python.

Pour le `sock.recv(1024)`, on va plutôt utiliser une version asynchrone de la gestion de socket client :

```python
# ouvrir une connexion vers un serveur
reader, writer = await asyncio.open_connection(host="127.0.0.1", port=8888)

# lire des données qui arrive du serveur
data = await reader.read(1024)
print(data.decode())

# envoyer des données
msg = 'hello'.encode()
writer.write(msg)
await writer.drain()
```

🌞 `chat_client_ii_3.py`

- **exécute de façon asynchrone une saisie utilisateur et la réception des messages**
- faites en sorte que l'affichage soit *pas trop* chaotique (vous prenez pas la tête non plus s'il y a quelques bugs/mochetés, on s'en fout pour le moment)
- le client ne quitte pas tant qu'on press pas `<CTRL + C>`
  - on peut donc saisir un message, l'envoyer, en saisir un deuxième, l'envoyer, etc
  - pendant que les messages reçus des autres clients s'affichent s'il y en a !

> **Pas de *loop* uniquement du `gather()`.**

🌞 `chat_server_ii_3.py`

- quand un message est reçu, il l'affiche dans le terminal au format
  - `Message received from {IP}:{Port} : {msg}`

➜ Bon bah tout est asynchrone là déjà ?

- normalement, plusieurs clients peuvent se co et envoyer des messages
- les uns ne reçoivent pas les messages des autres, mais ça fonctionne le traitement de plusieurs clients propres

## 4. Un chat fonctionnel

➜ **Pour avoir un chat fonctionnel** *(sûrement moche, mais fonctionnel techniquement)* il reste plus qu'à **redistribuer le message quand un client envoie un truc**.

Le serveur donc, s'il reçoit un message d'un client, il le renvoie à tous les autres clients. Un chat quoi !

➜ Pour ça, il faut connaître que **le serveur connaisse à chaque instant la liste des clients connectés**.

On va rester simple ici et utiliser une **variable globale**. Ce sera un dictionnaire qui contiendra les infos des clients connectés.

A chaque fois qu'un client se connecte, ses infos sont ajoutées au dictionnaire.

Quand on veut envoyer un message à tout le monde, suffit de l'envoyer à tous les membres du dictionnaire.

Déclaration d'un dictionnaire global :

```python
global CLIENTS
CLIENTS = {}
```

🌞 `chat_server_ii_4.py`

- utilise une variable globale `CLIENTS`
- quand un client se co : son IP, son port, son reader et son writer sont stockées dans `CLIENTS`
  - si le client s'est déjà co (s'il est déjà dans `CLIENTS`) on ne fait rien
- soyons smart, vous stockerez sous cette forme là :

```python
# addr est le tuple (IP, port) du client : ce sera la clé de notre dico
# le reader nous permet de recevoir des données de ce client là
# le writer permet d'envoyer à ce client là
CLIENTS[addr] = {}
CLIENTS[addr]["r"] = reader
CLIENTS[addr]["w"] = writer
```

- quand un message d'un client est reçu
  - parcours du dictionnaire `CLIENTS`
  - envoi du message à tout le monde (sauf celui qui l'a envoyé)
  - le message doit être sous la forme `{IP}:{Port} a dit : {msg}`
    - `{IP}` est l'IP du client qui a envoyé le message
    - `{Port}` est le port utilisé par le client qui a envoyé le message

## 5. Gérer des pseudos

On va faire en sorte que chaque user choisisse un pseudo, et que le serveur l'enregistre. Ce sera plus sympa que `{IP}:{port}` pour identifier les clients.

🌞 `chat_client_ii_5.py`

- avant de lancer les deux tâches asynchrones (saisie user et réception de données)
- au début du code donc, de façon synchrone (PAS asynchrone)
  - une saisie utilisateur pour qu'il saisisse son pseudo
  - le client envoie le pseudo saisi au serveur
  - il envoie exactement : `Hello|<PSEUDO>`, par exemple `Hello|it4`

> **Si vous avez encore le client qui envoie juste la string "Hello" à la connexion, enlevez-le !**

➜ Dès sa connexion, le client envoie donc un message contenant son pseudo

- on peut utiliser ce savoir côté serveur : le premier message d'un client contient le pseudo

🌞 `chat_server_ii_5.py`

- à la réception d'un message
  - si le client est nouveau
  - on vérifie que la data commence par `Hello`
  - on stocke son pseudo dans le dictionnaire des clients
  - on envoie à tout le monde `Annonce : <PSEUDO> a rejoint la chatroom`

```python
# avant, isoler le pseudo du message "Hello|<PSEUDO>" dans une variable "pseudo"
CLIENTS[addr] = {}
CLIENTS[addr]["r"] = reader
CLIENTS[addr]["w"] = writer
CLIENTS[addr]["pseudo"] = pseudo
```

- quand il redistribue les messages il envoie `<PSEUDO> a dit : {msg}`

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