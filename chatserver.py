import asyncio
from gtts import gTTS # tts package
import os

writers = []

nameDict = {}

def say(text):
    auOut = gTTS(text, lang='en')
    auOut.save("out.mp3")
    os.system("afplay out.mp3")

def processAudioMessage(name, message):
    message = message[2:]
    if message != '':
        say(name + ' said: ' + message)
    return f'*audio* {message}'
    



def decorateMessage(message, writer):
    global nameDict
    addrInfo = writer.get_extra_info('peername')
    addr = addrInfo[0] + str(addrInfo[1])
    name = 'anonymous'
    if message.startswith('/n'):
        temp = message[2:].strip()
        if temp != '':
            nameDict[addr] = temp
            say(temp + " joined.")
            return temp + " joined."
    else:
        if addr in nameDict:
            name = nameDict[addr]
        if message.startswith('/a'):
            message = processAudioMessage(name, message)
        if message.startswith('/a'):
            say(name + ' left.')
            return 'exit'
        return f'[{name}] {message}'

    

    

def forward(writer, addr, message):
    for w in writers:
        if w != writer:
            w.write(f"{message!r}\n".encode())

async def handle(reader, writer):
    writers.append(writer)
    addr = writer.get_extra_info('peername')
    message = f"{addr!r} is connected !!!!"
    print(message)
    forward(writer, addr, message)
    while True:
        data = await reader.read(100)
        message = data.decode().strip()
        message = decorateMessage(message, writer)
        forward(writer, addr, message)
        await writer.drain()
        if message == "exit":
            message = f"{addr!r} wants to close the connection."
            print(message)
            forward(writer, "Server", message)
            break
    writers.remove(writer)
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle, '0.0.0.0', 8888)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())