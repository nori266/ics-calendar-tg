import asyncio
from os import environ
import re

from dotenv import load_dotenv
from ics import Calendar, Event
from telethon import TelegramClient, events

load_dotenv()
API_ID = int(environ.get('API_ID'))
API_HASH = environ.get('API_HASH')


def create_calendar_event(name: str, time: str):
    c = Calendar()
    e = Event()

    # TODO parse 5 last messages to get time
    # TODO ask for date
    e.name = "Our cool meeting"
    e.begin = f'2021-11-08 {time}:00'
    e.end = f'2021-11-08 {time}:00'
    c.events.add(e)

    with open(f'{name}.ics', 'w') as my_file:
        my_file.writelines(c)


def parse_messages(messages):
    time = "12:00"
    # print([m.message for m in list(messages)])
    for mes in messages:

        search = re.search(r"\d{2}:\d{2}", mes.message)
        if search:
            time = search.group(0)
            break
    return time


async def main():
    async with TelegramClient('parse_session', API_ID, API_HASH) as client:

        @client.on(events.NewMessage(pattern='-ics'))
        async def handler(event):
            time = parse_messages(await client.get_messages(event.chat_id, limit=10))

            await event.reply(f'Event scheduled at {time} tomorrow!')
            event_name = 'our_cool_event'
            create_calendar_event(event_name, time)
            await client.send_file(event.peer_id.user_id, f"{event_name}.ics")



        await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
