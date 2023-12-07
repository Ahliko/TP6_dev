import asyncio

CLIENTS = {}


async def handle_client_msg(reader, writer):
    global CLIENTS
    CLIENTS[writer.get_extra_info('peername')] = {}
    CLIENTS[writer.get_extra_info('peername')]["r"] = reader
    CLIENTS[writer.get_extra_info('peername')]["w"] = writer
    while True:
        data = await CLIENTS[CLIENTS[writer.get_extra_info('peername')]["w"].get_extra_info('peername')]["r"].read(1024)
        addr = CLIENTS[writer.get_extra_info('peername')]["w"].get_extra_info('peername')
        if data == b'':
            break
        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message!r}")
        for client in CLIENTS:
            if client["w"] is None:
                CLIENTS.pop(client)
            elif client != writer.get_extra_info('peername'):
                await CLIENTS[client]["w"].write(f"{addr[0]}:{addr[1]} a dit : {message}".encode())
                await CLIENTS[client]["w"].drain()


async def main():
    server = await asyncio.start_server(handle_client_msg, '0.0.0.0', 8888)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
