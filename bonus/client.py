import asyncio
import os.path
import sys

import aioconsole
import argparse

import aiofiles
import colored
import json


class Client:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.__pseudo = None
        self.__reader = None
        self.__writer = None
        self.__link = f"{os.path.abspath(os.path.curdir)}/info.json"
        self.__data = {}
        asyncio.run(self.run())

    @staticmethod
    def unjson(data):
        return json.loads(data)

    @staticmethod
    def to_json(data):
        return json.dumps(data)

    @staticmethod
    async def write_content(content, file):
        async with aiofiles.open(file, mode="w") as f:
            await f.write(content)
            await f.flush()

    @staticmethod
    async def read_content(file):
        async with aiofiles.open(file, mode="r") as f:
            return await f.read()

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

    async def decode(self, reader):
        len_header = self.unbinaire(await reader.read(1))
        msg_len = self.unbinaire(await reader.read(len_header))
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
                raise RuntimeError('Invalid chunk received bro')
            else:
                # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message

                return b"".join(chunks)

    async def __async_input(self):
        while True:
            try:
                input_coro = await aioconsole.ainput("Enter your message: ")
                self.__writer.write(input_coro.encode())
                await self.__writer.drain()
            except KeyboardInterrupt:
                print("Bye!")
                self.__writer.write(self.encode(""))
                self.__writer.close()
                await self.__writer.wait_closed()
                exit(0)

    async def __async_receive(self):
        while True:
            try:
                data = await self.decode(self.__reader)
                if data == b'':
                    print("Server disconnected")
                    self.__writer.close()
                    exit(0)
                message = data.decode()
                if message.startswith("Annonce : "):
                    print(colored.stylize(message, colored.fg("red")))
                elif len(message.split("\x1b")) == 4:
                    print("\n" + message.split("\x1b")[0],
                          colored.stylize(message.split("\x1b")[2], colored.fg(message.split("\x1b")[1])) +
                          colored.stylize(message.split("\x1b")[3], colored.fg(15)))
                elif len(message.split("\x1b")) == 2:
                    print("\n" + message.split("\x1b")[0], colored.stylize(message.split("\x1b")[1], colored.fg(15)))
            except KeyboardInterrupt:
                print("Bye!")
                self.__writer.write(self.encode(""))
                self.__writer.close()
                await self.__writer.wait_closed()
                exit(0)

    async def __async_pseudo(self):
        input_coro = await aioconsole.ainput("Enter your pseudo: ")
        if input_coro == "":
            print("Pseudo cannot be empty.")
            return False
        self.__pseudo = input_coro
        self.__writer.write(self.encode(f"Hello|{self.__pseudo}"))
        await self.__writer.drain()
        data = await self.decode(self.__reader)
        self.__data["id"] = data.decode().split("|")[1]
        self.to_json(self.__data)
        await self.write_content(self.to_json(self.__data), self.__link)
        return True

    async def __async_id(self):
        self.__writer.write(self.encode(f"ID|{self.__data['id']}"))
        await self.__writer.drain()
        data = await self.decode(self.__reader)
        if data.decode() != "200":
            return False
        return True

    async def run(self):
        try:
            if os.path.exists(self.__link):
                self.__data = await self.read_content(self.__link)
                self.__data = self.unjson(self.__data)
                self.__reader, self.__writer = await asyncio.open_connection(host=self.__host, port=self.__port)
                if await self.__async_id():
                    while True:
                        await asyncio.gather(*[self.__async_input(),
                                               self.__async_receive()])
                else:
                    print("Connection rejected")
                    os.remove(self.__link)
                    self.__writer.write(self.encode(""))
                    self.__writer.close()
                    await self.__writer.wait_closed()
                    exit(1)
            else:
                self.__reader, self.__writer = await asyncio.open_connection(host=self.__host, port=self.__port)
                if await self.__async_pseudo():
                    while True:
                        await asyncio.gather(*[self.__async_input(),
                                               self.__async_receive()])
                else:
                    print("Connection rejected")
                    self.__writer.write(self.encode(""))
                    self.__writer.close()
                    await self.__writer.wait_closed()
                    exit(1)
        except KeyboardInterrupt:
            print("Bye!")
            self.__writer.write(self.encode(""))
            self.__writer.close()
            await self.__writer.wait_closed()
            exit(0)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Client de chat.")
    argparser.add_argument("-p", "--port", type=int, help="Port de connexion du serveur")
    argparser.add_argument("-a", "--address", type=str, help="Adresse de connexion du serveur")
    argv = argparser.parse_args()
    if argv.port:
        if argv.address:
            Client(host=argv.address, port=argv.port)
        else:
            Client(port=argv.port)
    elif argv.address:
        Client(host=argv.address)
    else:
        Client()
