import asyncio

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

debug = False

async def exit_loop(nc):
    await nc.close()
    return

async def run(loop):
    nc = NATS()

    await nc.connect("nats://nats:4222", loop=loop)

    try:
        if debug:
            print(f'Asking for min/max')
        response = await nc.request("min_max", b'', 0.5)
        if debug:
            print("Received response: {message}".format(
                message=response.data.decode()))
        min_max_str = response.data.decode()
        split_min_max_str = min_max_str.split(':')
        if len(split_min_max_str) is not 2:
            await nc.close()
            return
        else:
            min_rand = int(split_min_max_str[0])
            max_rand = int(split_min_max_str[1])
            if debug:
                print(f'min_rand={min_rand}')
                print(f'max_rand={max_rand}')
    except ErrTimeout:
        print("Request timed out")

    guessed = False
    while (guessed is False):
        for guess in range(min_rand,max_rand+1):
            try:
                if debug:
                    print(f'Guessing: {guess}')
                response = await nc.request("guess", str(guess).encode(), 0.5)
                if debug:
                    print("Received response: {message}".format(
                        message=response.data.decode()))
                if response.data.decode() == "Right":
                    print(f'We guessed it. {guess}')
                    guessed = True
                    break
            except ErrTimeout:
                print("Request timed out")
                break
    
        guessed = True

    await exit_loop(nc)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()