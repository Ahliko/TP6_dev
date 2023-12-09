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

    async def __async_input(self):
        while True:
            try:
                input_coro = await aioconsole.ainput("Enter your message: ")
                self.__writer.write(input_coro.encode())
                await self.__writer.drain()
            except KeyboardInterrupt:
                print("Bye!")
                self.__writer.write("".encode())
                self.__writer.close()
                await self.__writer.wait_closed()
                exit(0)

    async def __async_receive(self):
        while True:
            try:
                data = await self.__reader.read(1024)
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
                self.__writer.write("".encode())
                self.__writer.close()
                await self.__writer.wait_closed()
                exit(0)

    async def __async_pseudo(self):
        input_coro = await aioconsole.ainput("Enter your pseudo: ")
        if input_coro == "":
            print("Pseudo cannot be empty.")
            return False
        self.__pseudo = input_coro
        self.__writer.write(f"Hello|{self.__pseudo}".encode())
        await self.__writer.drain()
        data = await self.__reader.read(1024)
        self.__data["id"] = data.decode().split("|")[1]
        self.to_json(self.__data)
        await self.write_content(self.to_json(self.__data), self.__link)
        return True

    async def __async_id(self):
        self.__writer.write(f"ID|{self.__data['id']}".encode())
        await self.__writer.drain()
        data = await self.__reader.read(1024)
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
                    self.__writer.close()
                    await self.__writer.wait_closed()
                    exit(1)
        except KeyboardInterrupt:
            print("Bye!")
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
