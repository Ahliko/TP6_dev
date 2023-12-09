import asyncio
import datetime
import os
import time
import uuid
from random import randint

from dotenv import load_dotenv


class Server:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__clients = {}
        asyncio.run(self.run())

    @staticmethod
    def generate_uuid():
        return uuid.uuid4()

    async def __handle_client_msg(self, reader, writer):
        print(f"New client : {writer.get_extra_info('peername')}")
        if writer.get_extra_info('peername') not in [i["addr"] for i in self.__clients.values()]:
            data = await reader.read(1024)
            if data == b'':
                writer.write("You must choose un nametag".encode())
                writer.close()
                return
            elif data.decode().startswith("Hello|"):
                id = self.generate_uuid()
                self.__clients[id] = {}
                self.__clients[id]["r"] = reader
                self.__clients[id]["w"] = writer
                self.__clients[id]["here"] = True
                self.__clients[id]["color"] = randint(0, 255)
                self.__clients[id]['pseudo'] = data.decode()[6:]
                self.__clients[id]["addr"] = writer.get_extra_info('peername')
                await self.__send(id)
                await self.__send_all("", id, True)
            elif data.decode() in self.__clients:
                id = data.decode()
                self.__clients[id]["r"] = reader
                self.__clients[id]["w"] = writer
                self.__clients[id]["here"] = True
                self.__clients[id]["addr"] = writer.get_extra_info('peername')
                await self.__send(id, accept=True)
                await self.__send_all("", id, reconnect=True)
            else:
                writer.write("You must choose un nametag".encode())
                writer.close()
                return
        else:
            id = await reader.read(1024).decode()
            if id in self.__clients:
                self.__clients[id]["r"] = reader
                self.__clients[id]["w"] = writer
                self.__clients[id]["here"] = True
                self.__clients[id]["addr"] = writer.get_extra_info('peername')
                await self.__send(id, accept=True)
            else:
                writer.write("Connection rejected".encode())
                writer.close()
                return
        while True:
            data = await \
                self.__clients[id][
                    "r"].read(
                    1024)
            client = id
            if data == b'':
                self.__clients[client]["here"] = False
                self.__clients[client]["w"].close()
                self.__clients[client]["w"] = None
                print(f"Client {self.__clients[client]['pseudo']} disconnected")
                await self.__send_all("", client, disconnect=True)
                break
            message = data.decode()
            self.__clients[client][
                "timestamp"] = f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]"
            print(
                f"Message received from {self.__clients[client]['addr'][0]}:{self.__clients[client]['addr'][1]} : {message!r}")
            await self.__send_all(message, client)

    async def __send(self, id, accept=False):
        if accept:
            self.__clients[id]["w"].write("200".encode())
        else:
            self.__clients[id]["w"].write(f"ID|{id}".encode())
        await self.__clients[id]["w"].drain()

    async def __send_all(self, message, localclient, annonce=False, disconnect=False, reconnect=False):
        for client in self.__clients:
            if self.__clients[client]["here"]:
                if not annonce:
                    if client != localclient:
                        if disconnect:
                            print(
                                f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a quitté la chatroom")
                            self.__clients[client]["w"].write(
                                f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a quitté la chatroom".encode())
                            await self.__clients[client]["w"].drain()
                        elif reconnect:
                            print(
                                f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} est de retour !")
                            self.__clients[client]["w"].write(
                                f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} est de retour !".encode())
                            await self.__clients[client]["w"].drain()
                        else:
                            self.__clients[client]["w"].write(
                                f"{self.__clients[localclient]['timestamp']}\033{self.__clients[localclient]['color']}\033{self.__clients[localclient]['pseudo']}\033 a dit : {message}".encode())
                            await self.__clients[client]["w"].drain()
                    else:
                        if not disconnect:
                            self.__clients[client]["w"].write(
                                f"{self.__clients[localclient]['timestamp']}\033Vous avez dit : {message}".encode())
                            await self.__clients[client]["w"].drain()
                        elif reconnect:
                            self.__clients[client]["w"].write(
                                f"{self.__clients[localclient]['timestamp']}\033Welcome back  !".encode())
                            await self.__clients[client]["w"].drain()
                else:
                    print(
                        f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom")

                    self.__clients[client]["w"].write(
                        f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom".encode())
                    print(client)
                    await self.__clients[client]["w"].drain()
        if disconnect:
            self.__clients.pop(localclient)

    async def run(self):
        server = await asyncio.start_server(self.__handle_client_msg, self.__host, self.__port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    load_dotenv(dotenv_path="config")
    Server(os.getenv("HOST"), int(os.getenv("PORT")))
