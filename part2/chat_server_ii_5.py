import argparse
import asyncio


class Server:
    def __init__(self, host="127.0.0.1", port=8888):
        self.__host = host
        self.__port = port
        self.__clients = {}
        asyncio.run(self.run())

    async def __handle_client_msg(self, reader, writer):
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
                self.__clients[writer.get_extra_info('peername')]['pseudo'] = data.decode()[6:]
                for client in self.__clients:
                    await self.__send_all("", client, True)
            else:
                writer.write("You must choose un nametag".encode())
                writer.close()
                return
        else:
            self.__clients[writer.get_extra_info('peername')]["r"] = reader
            self.__clients[writer.get_extra_info('peername')]["w"] = writer
        while True:
            data = await \
                self.__clients[writer.get_extra_info('peername')][
                    "r"].read(
                    1024)
            client = writer.get_extra_info('peername')
            if data == b'':
                break
            message = data.decode()
            print(
                f"Message received from {self.__clients[client]['w'].get_extra_info('peername')[0]}:{self.__clients[client]['w'].get_extra_info('peername')[1]} : {message!r}")
            await self.__send_all(message, client)

    async def __send_all(self, message, localclient, annonce=False):
        for client in self.__clients:
            if self.__clients[client]["w"] is None:
                self.__clients.pop(client)
            else:
                try:
                    if not annonce:
                        if client != localclient:
                            await self.__clients[client]["w"].write(
                                f"{self.__clients[localclient]['pseudo']} a dit : {message}".encode())
                            await self.__clients[client]["w"].drain()
                    else:
                        print(self.__clients[client]["w"])
                        await self.__clients[client]["w"].write(
                            f"Annonce : {self.__clients[localclient]['pseudo']} a rejoint la chatroom".encode())
                        await self.__clients[client]["w"].drain()
                except TypeError:
                    print("TypeError")
                    pass

    async def run(self):
        server = await asyncio.start_server(self.__handle_client_msg, self.__host, self.__port)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Client de chat.")
    argparser.add_argument("-p", "--port", type=int, help="Port de connexion du serveur")
    argparser.add_argument("-a", "--address", type=str, help="Adresse de connexion du serveur")
    argv = argparser.parse_args()
    if argv.port:
        if argv.address:
            Server(host=argv.address, port=argv.port)
        else:
            Server(port=argv.port)
    elif argv.address:
        Server(host=argv.address)
    else:
        Server()
