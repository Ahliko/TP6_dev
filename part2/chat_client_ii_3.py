import asyncio
import aioconsole


async def async_input(writer):
    input_coro = await aioconsole.ainput("Enter your message: ")
    writer.write(input_coro.encode())
    await writer.drain()


async def async_receive(reader):
    data = await reader.read(1024)
    if data == b'':
        return
    message = data.decode()
    print(f"Received {message!r}")


async def main():
    try:
        while True:
            reader, writer = await asyncio.open_connection(host="127.0.0.1", port=8888)
            await asyncio.gather(*[async_input(writer),
                                   async_receive(reader)])
            writer.close()
            await writer.wait_closed()

    except KeyboardInterrupt:
        print("Bye!")
        exit(0)


if __name__ == "__main__":
    asyncio.run(main())
