"""The client to connect to my gpg-server (go app)"""

import asyncio
import contextlib
from asyncio.streams import StreamReader, StreamWriter


async def handle_input(writer: StreamWriter, done: asyncio.Event):
    loop = asyncio.get_event_loop()
    try:
        while not done.is_set():
            message = await loop.run_in_executor(None, input, "You: ")
            if message.lower() in ("exit", "quit"):
                done.set()
                break
            writer.write(message.encode() + b"\n")
            await writer.drain()

    except (asyncio.CancelledError, EOFError):
        pass

    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


async def handle_server(reader: StreamReader, done: asyncio.Event):
    try:
        while not done.is_set():
            data = await reader.readline()
            if not data:
                print("Disconnected from server.")
                done.set()
                break
            print(f"\n[Server] {data.decode().rstrip()}")
    except asyncio.CancelledError:
        pass


async def main():
    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 4242)
        print("Connected to server.")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    done = asyncio.Event()

    input_task = asyncio.create_task(handle_input(writer, done))
    server_task = asyncio.create_task(handle_server(reader, done))

    _, pending = await asyncio.wait([input_task, server_task], return_when=asyncio.FIRST_COMPLETED)

    done.set()

    for task in pending:
        _ = task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task

    print("Client shutdown cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nclient terminated.")
