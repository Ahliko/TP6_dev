import asyncio
import aioconsole
import argparse
import colored


class Client:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.__pseudo = None
        self.__reader = None
        self.__writer = None
        asyncio.run(self.run())

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
                elif len(message.split("\033")) == 2:
                    print(colored.stylize(message.split("\033")[1], colored.fg(message.split("\033")[0])))
                print(f"Received {message!r}")
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
        return True

    async def run(self):
        try:
            self.__reader, self.__writer = await asyncio.open_connection(host=self.__host, port=self.__port)
            if await self.__async_pseudo():
                while True:
                    await asyncio.gather(*[self.__async_input(),
                                           self.__async_receive()])
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