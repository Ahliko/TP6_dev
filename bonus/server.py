import asyncio
import os
from random import randint

from dotenv import load_dotenv


class Server:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__clients = {}
        asyncio.run(self.run())

    async def __handle_client_msg(self, reader, writer):
        print(f"New client : {writer.get_extra_info('peername')}")
        if writer.get_extra_info('peername') not in self.__clients:
            data = await reader.read(1024)
            if data == b'':
                writer.write("You must choose un nametag".encode())
                writer.close()
                return
            if data.decode().startswith("Hello|"):
                self.__clients[writer.get_extra_info('peername')] = {}
                self.__clients[writer.get_extra_info('peername')]["r"] = reader
                self.__clients[writer.get_extra_info('peername')]["w"] = writer
                self.__clients[writer.get_extra_info('peername')]["here"] = True
                self.__clients[writer.get_extra_info('peername')]["color"] = randint(0, 255)
                self.__clients[writer.get_extra_info('peername')]['pseudo'] = data.decode()[6:]
                await self.__send_all("", writer.get_extra_info('peername'), True)
            else:
                writer.write("You must choose un nametag".encode())
                writer.close()
                return
        else:
            self.__clients[writer.get_extra_info('peername')]["r"] = reader
            self.__clients[writer.get_extra_info('peername')]["w"] = writer
            self.__clients[writer.get_extra_info('peername')]["here"] = True
        while True:
            data = await \
                self.__clients[writer.get_extra_info('peername')][
                    "r"].read(
                    1024)
            client = writer.get_extra_info('peername')
            if data == b'':
                self.__clients[client]["here"] = False
                self.__clients[client]["w"].close()
                self.__clients[client]["w"] = None
                print(f"Client {self.__clients[client]['pseudo']} disconnected")
                await self.__send_all("", client, disconnect=True)
                break
            message = data.decode()
            print(
                f"Message received from {self.__clients[client]['w'].get_extra_info('peername')[0]}:{self.__clients[client]['w'].get_extra_info('peername')[1]} : {message!r}")
            await self.__send_all(message, client)

    async def __send_all(self, message, localclient, annonce=False, disconnect=False):
        for client in self.__clients:
            if self.__clients[client]["here"]:
                if not annonce:
                    if client != localclient:
                        if disconnect:
                            print(f"Annonce : {self.__clients[localclient]['pseudo']} a quitté la chatroom")
                            self.__clients[client]["w"].write(
                                f"Annonce : {self.__clients[localclient]['pseudo']} a quitté la chatroom".encode())
                            await self.__clients[client]["w"].drain()
                        else:
                            self.__clients[client]["w"].write(
                                f"\033{self.__clients[localclient]['color']}\033{self.__clients[localclient]['pseudo']}\033 a dit : {message}".encode())
                            await self.__clients[client]["w"].drain()
                    else:
                        if not disconnect:
                            self.__clients[client]["w"].write(
                                f"Vous avez dit : {message}".encode())
                            await self.__clients[client]["w"].drain()
                else:
                    print(f"Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom")

                    self.__clients[client]["w"].write(
                        f"Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom".encode())
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
