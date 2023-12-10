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

    @staticmethod
    def unbinaire(msg):
        return int.from_bytes(msg, byteorder='big')

    @staticmethod
    def binaire(msg):
        return msg.to_bytes((msg.bit_length() + 7) // 8, byteorder='big')

    def encode(self, data: str):
        header = self.binaire(len(data))
        len_header = self.binaire(len(header))
        seq_fin = "<clafin>".encode()
        return len_header + header + data.encode() + seq_fin

    async def receive(self, reader):
        data_header = await reader.read(1)
        if data_header == b'<':
            data_header += await reader.read(7)
            data_header = await reader.read(1)
        len_header = self.unbinaire(data_header)
        data_len = await reader.read(len_header)
        msg_len = self.unbinaire(data_len)
        chunks = []

        bytes_received = 0
        while bytes_received < msg_len:
            # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
            chunk = await reader.read(min(msg_len - bytes_received,
                                          1024))
            if not chunk:
                raise RuntimeError('Invalid chunk received bro')

            # on ajoute le morceau de 1024 ou moins à notre liste
            chunks.append(chunk)

            # on ajoute la quantité d'octets reçus au compteur
            bytes_received += len(chunk)
            fin: bytes = await reader.read(8)
            if fin.decode() != "<clafin>":
                print(fin.decode())
                raise RuntimeError('Invalid chunk received bro')
            else:
                # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message

                return b"".join(chunks)

    async def __handle_client_msg(self, reader, writer):
        print(f"New client : {writer.get_extra_info('peername')}")
        if writer.get_extra_info('peername') not in [i["addr"] for i in self.__clients.values()]:
            data = await self.receive(reader)
            if data == b'':
                writer.write(self.encode("You must choose un nametag"))
                writer.close()
                return
            elif data.decode().startswith("Hello|"):
                id = str(self.generate_uuid())
                self.__clients[id] = {}
                self.__clients[id]["r"] = reader
                self.__clients[id]["w"] = writer
                self.__clients[id]["here"] = True
                self.__clients[id]["color"] = randint(0, 255)
                self.__clients[id]['pseudo'] = data.decode()[6:]
                self.__clients[id]["addr"] = writer.get_extra_info('peername')
                await self.__send(id)
                await self.__send_all("", id, True)
            elif data.decode().split('ID|')[1] in self.__clients:
                id = data.decode().split('ID|')[1]
                self.__clients[id]["r"] = reader
                self.__clients[id]["w"] = writer
                self.__clients[id]["here"] = True
                self.__clients[id]["addr"] = writer.get_extra_info('peername')
                self.__clients[id][
                    "timestamp"] = f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]"
                await self.__send(id, accept=True)
                await self.__send_all("", id, reconnect=True)
            else:
                writer.write(self.encode("You must choose un nametag"))
                writer.close()
                return
        else:
            id = await self.receive(reader)
            if id in self.__clients:
                self.__clients[id]["r"] = reader
                self.__clients[id]["w"] = writer
                self.__clients[id]["here"] = True
                self.__clients[id]["addr"] = writer.get_extra_info('peername')
                await self.__send(id, accept=True)
            else:
                writer.write(self.encode("Connection rejected"))
                writer.close()
                return
        while True:
            data = await self.receive(self.__clients[id][
                                          "r"])
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
            self.__clients[id]["w"].write(self.encode("200"))
        else:
            self.__clients[id]["w"].write(self.encode(f"ID|{id}"))
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
                                self.encode(
                                    f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a quitté la chatroom"))
                            await self.__clients[client]["w"].drain()
                        elif reconnect:
                            print(
                                f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} est de retour !")
                            self.__clients[client]["w"].write(
                                self.encode(
                                    f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} est de retour !"))
                            await self.__clients[client]["w"].drain()
                        else:
                            self.__clients[client]["w"].write(
                                self.encode(
                                    f"{self.__clients[localclient]['timestamp']}\033{self.__clients[localclient]['color']}\033{self.__clients[localclient]['pseudo']}\033 a dit : {message}"))
                            await self.__clients[client]["w"].drain()
                    else:
                        if not disconnect and not reconnect:
                            self.__clients[client]["w"].write(
                                self.encode(f"{self.__clients[localclient]['timestamp']}\033Vous avez dit : {message}"))
                            await self.__clients[client]["w"].drain()
                        elif reconnect:
                            self.__clients[client]["w"].write(
                                self.encode(f"{self.__clients[localclient]['timestamp']}\033Welcome back  !"))
                            await self.__clients[client]["w"].drain()
                else:
                    print(
                        f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom")

                    self.__clients[client]["w"].write(
                        self.encode(
                            f"[{datetime.datetime.today().hour}:{datetime.datetime.today().minute}]\033Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom"))
                    print(client)
                    await self.__clients[client]["w"].drain()

    async def run(self):
        server = await asyncio.start_server(self.__handle_client_msg, self.__host, self.__port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    load_dotenv(dotenv_path="config")
    Server(os.getenv("HOST"), int(os.getenv("PORT")))
