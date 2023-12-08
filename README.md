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


  - [1. Basic Cosmetic](#1-basic-cosmetic)
  - [2. Gestion d'ID](#2-gestion-did)
  - [2. Logs](#2-logs)
  - [3. Config et arguments](#3-config-et-arguments)
  - [4. Encodage maison](#4-encodage-maison)
  - [5. Envoi d'image](#5-envoi-dimage)
  - [6. Gestion d'historique](#6-gestion-dhistorique)
  - [7. Plusieurs rooms](#7-plusieurs-rooms)

## 1. Basic Cosmetic

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



Parlons un peu cosmétique côté client.

➜ **`Vous avez dit`**

- côté client, quand le user saisit et envoie un message, ça s'affiche de son côté dans l'historique sous la forme `Vous avez dit : {msg}`

➜ **Colors**

- côté serveur
  - une couleur random est générée pour chaque nouveau client qui se connecte
  - elle est stockée dans la variable globale `CLIENTS`, une couleur par client, choisie aléatoirement à sa connexion donc
  - dès qu'un message est reçu, et redistribué aux autres, la couleur associé au user qui a envoyé le message est aussi envoyée
- côté client
  - affiche le nom de l'utilisateur qui a parlé en couleur

> Ca augmente fortement la lisibilité du chat d'avoir une couleur unique associée à chaque user 💄

![Yet another](./img/not_sure.jpg)

➜ **Timestamp**

- **côté serveur**
  - quand un message est reçu, vous **enregistrer dans une variable l'heure et la date actuelle** : l'heure de réception du message en soit
  - quand il est redistribué aux clients, **l'heure est envoyée aussi**, pour que le client l'affiche
- **côté client**
  - affiche l'heure sous la forme `[hh:mm]` devant chaque message

## 2. Gestion d'ID

Bon c'est bien les pseudos étou, mais on aime bien les IDs pour gérer des users normalement. Ca apporte plein d'avantage quand on gère des applications à grandes échelle, ou juste en terme de conception si on commence à ajouter de la base de données dans le mix.

Surtout surtout, ça va nous permettre de gérer la déco/reco des clients. Quand un client se co, on peut vérifier si on le connaît déjà ou non.

➜ **Gestion d'ID uniques pour les utilisateurs**

- à la nouvelle connexion d'un client, un nouvel ID unique lui est attribué
- à vous de choisir une méthode, quelques idées :
  - juste un bête incrément : premier user c'est 1, deuxième 2, etc
    - mais... faut garder un trace de l'incrément actuel en permanence
    - et si un user est supprimé, ça crée un ID vaquant
  - un hash
    - le hash de la concaténation `IP:port:pseudo` par exemple, ça me paraît assez unique
    - ça implique qu'on reconnaît un user que s'il se co depuis la même IP et le même port aussi
- si un client se déco/reco
  - le serveur lui envoie un ptit message "Welcome back <PSEUDO> !"
  - le serveur envoie aux autres "<PSEUDO> est de retour !"

> Vous pouvez par exemple, dans le dictionnaire `CLIENTS` ajouter une propriété pour chaque client : `connected` qui est un booléen. Les clients qui sont à `connected = True` reçoivent des messages. Le serveur n'envoie pas de messages aux clients qui sont à `connected = False` mais peut les reconnaître en cas de reconnexion.

## 2. Logs

➜ **Gestion de logs côté client**

- un fichier dans `/var/log/chat_room/client.log`
- contient tout l'historique de conversation

➜ **Gestion de logs côté serveur**

- un fichier dans `/var/log/chat_room/server.log`
  - contient tout l'historique de conversation
  - contient l'heure d'arrivée et départ des clients
- logs console propres. Un message pour :
  - connexion d'un client
  - réception d'un message
  - envoi d'un message à un client
  - déconnexion d'un client

> Logs logs logs 📜 everywhere. Indispensable pour n'importe quelle application sérieuse.

## 3. Config et arguments

➜ **Gestion d'arguments et d'un fichier de conf**

- côté client
  - choisir l'IP et le port auxquels on se conncte
- côté serveur
  - choisir l'IP et le port sur lesquels écouter

> Ui parce que c'est super chiant de devoir éditer directement le code pour trouver la variable qui déclare l'IP et celle qui déclare le port.

**Le fichier de conf pour le client**, par exemple, doit pouvoir supporter cette syntaxe :

```
HOST=127.0.0.1
PORT=9999
```

> *Vous êtes libres de choisir une autre syntaxe ou d'autres mots-clés. Restez standards SVP, inventez pas un truc de ouf.*

Et toujours l'exemple avec le client, on doit pouvoir **appeler le script** comme ça :

```python
$ python client.py --port 9999 --address 127.0.0.1
$ python client.py -p 9999 -a 127.0.0.1
```

> *S'il existe un fichier de conf ET que des options sont précisées, ce sont les options qui sont prioritaires normalement.*

## 4. Encodage maison

Une des parties les plus tricky mais les plus abouties et qui fait suite au TP précédent.

La perf la perf la perf ! On va gérer des en-têtes pour indiquer la taille des messages et arrêter les `recv(1024)`.

➜ **Inventez un encodage maison pour la chatroom.**

---

➜ Par exemple, dès qu'un user envoie un message, le client pourrait formater son message comme ça :

```
1|32|salut à tous dans la chat room !
```

- `1` indique que le client envoie un message court qui doit être redistribué à tout le monde
- `32` est la longueur du message
- `salut à tous dans la chat room !` est le message que client a saisi
- les `|` ne sont pas envoyés : c'est juste pour faciliter votre lecture

Autrement dit on a :

- le premier octet qui contient le type de message
  - un `1` c'est un simple texte court à renvoyer aux autres (court = 2 octets)
- si le premier octet est un `1`, les deux octets suivants contiennent la taille du message
  - ici on lira 32 qui **doit** être encodé sur deux octets
- on peut ensuite lire autant d'octets que la valeur qu'on vient d'apprendre
  - ici on lira donc les 32 octets suivants, qui contiennent le message

➜ **On peut même faire mieux et imaginer un header lui-même à taille variable** (et pas que le message)

Par exemple, le client, à la saisie d'un message long, pourrait envoyer :

```
2|7|48038396025285290|<MSG TRES LONG>
```

- `2` indique que le client envoie un message long qui doit être redistribué à tout le monde
- `7` est le nombre d'octets qui contient la taille
- `48038396025285290` est la taille du message
- `<MSG TRES LONG>` c'est... le très long message

Le serveur :

- lit un octet et découvre `1` ou `2`
- si c'est un `1`
  - il lit 2 octets pour apprendre la taille du message
- si c'est un `2`
  - il lit 1 octet pour apprendre la taille du header de la taille
  - il lit n octets (valeur qu'il vient d'apprendre) pour apprendre la taille du message
- il lit le message en précisant le bon nombre d'octets à lire

➜ **Côté serveur, il faudrait aussi encoder les messages qui sont envoyés aux clients.**

Par exemple, si `toto` dit `bonjour`, le serveur pourrait envoyer le message suivant aux clients :

```
1|4|toto|1|7|bonjour
```

- `1` indique un message court (sur 1 octet)
- `4` indique la taille du pseudo (sur 1 octet, 256 caractères max par pseudo donc)
- `toto` le pseudo (taille variable, annoncée juste avant)
- `1` indique la taille du header du message (sur 1 octet)
- `7` indique la taille du message (taille variable, annoncée juste avant)
- `bonjour` le message

➜ **Ce n'est ici qu'un exemple, une proposition, inventez votre propre protocole/encodage :D**

![Pretend](./img/pretend.jpg)

## 5. Envoi d'image

**Euh j'ai trouvé cette lib hihihi** : https://pypi.org/project/ascii-magic/.

Ca convertit des PNG ou des JPG (j'ai testé avec ça) en ASCII art.

Genre de ça :

![Fleur](./img/flower.png)

A ça :

![ASCII Fleur](./img/flower_ascii.png)

➜ **Supporter l'envoi d'image**

- libre à vous de transformer l'image sur le client puis envoyer
- ou envoyer l'image et transformer sur le serveur
- utilisez `ascii-magic` pour la conversion
- les autres clients ont l'ASCII art qui s'affiche

> *Si t'as fait la partie sur l'encodage, on peut imaginer que l'envoi d'une image, c'est le message de type `3`... :)*

## 6. Gestion d'historique

Quand tu rejoins la conversation en retard, t'as pas l'historique, relou.

➜ **Gérer un historique de conversation**

- oui oui y'a déjà les logs, mais tu vas pas envoyer les logs comme ça au client pour qu'il affiche l'historique
- donc : enregistrer les conversations au format JSON côté serveur
  - à chaque réception d'un message, il faut l'enregistrer
  - attention, ça devient vite très violent si vous demandez une lecture puis une écriture sur le disque à chaque réception d'un message...
- quand un nouveau client arrive, lui envoyer en format JSON l'historique
- le client le réceptionne et fait l'affichage nécessaire

![JSON](img/json.png)

## 7. Plusieurs rooms

Quand un client se connecte, après avoir envoyé son pseudo, on lui propose de créer une nouvelle room ou d'en rejoindre une existante.

➜ **Côté serveur**

- entretient une liste des rooms, et qui y est connecté
- quand il reçoit un message, il ne le renvoie qu'aux users de la room concernée
- peut-être intéressant d'ajouter un niveau au dictionnaire `CLIENTS` par exemple : `CLIENTS["room 1"][addr]`

➜ **Côté client**

- le choix de la room se fait de façon synchrone (pas asynchrone) après le choix du pseudo