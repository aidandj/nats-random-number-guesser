import asyncio
import random

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

debug = False
min_rand = 0
max_rand = 1000
random_number = random.randint(min_rand,max_rand)

async def reset_random_number():
    if debug:
        print("Resetting")
    # I feel like this could be done better than global...
    global random_number 
    random_number = random.randint(min_rand,max_rand)
    print(f'Try and guess my number. (Hint: {random_number})')

async def number_guess(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    if debug:
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
    if (int(data) == random_number):
        await nc.publish(reply, b'Right')
        await reset_random_number()
    else:
        await nc.publish(reply, b'Wrong')

async def handle_min_max_request(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    if debug:
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
    await nc.publish(reply, f'{min_rand}:{max_rand}'.encode())

async def run(loop):

    await nc.connect("nats://nats:4222", loop=loop)

    try:
        await reset_random_number()

        # Handle guesses
        sid = await nc.subscribe("guess", "guesses", number_guess)

        sid2 = await nc.subscribe("min_max", "min_max_requests",handle_min_max_request)

        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        await nc.close()
        loop.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    nc = NATS()

    try:
        asyncio.ensure_future(run(loop))
        loop.run_forever()
        # loop.run_until_complete(run(loop))
    except KeyboardInterrupt:
        pass