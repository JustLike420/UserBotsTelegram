import asyncio
from pyrogram import Client


async def main():
    api_id = 19767206
    api_hash = '9e750bc8b88f3612465d6784d6a3f44c'
    phone_number = input('Input phone: ')
    phone_number = phone_number.strip().replace('-', '')
    async with Client('accounts/' + phone_number, api_id, api_hash) as client:
        await client.send_message('me', "Done!")


if __name__ == '__main__':
    asyncio.run(main())
