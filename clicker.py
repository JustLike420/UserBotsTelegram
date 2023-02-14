from pyrogram import Client, types
import asyncio
from pyrogram.errors.exceptions.bad_request_400 import DataInvalid


class UserClicker:
    def __init__(self, name: str):
        self.api_id = 19767206
        self.api_hash = '9e750bc8b88f3612465d6784d6a3f44c'
        self.chat_id = 6096397107  # https://t.me/DHDGame_Bot
        self.client = Client('accounts/' + name, self.api_id, self.api_hash)

    async def get_last_message(self) -> types.Message:
        last_messages = self.client.get_chat_history(chat_id=self.chat_id, limit=1)
        async for message in last_messages:
            return message

    @staticmethod
    async def get_captcha_answer(button_text: str, message: types.Message):
        keyboard = message.reply_markup.inline_keyboard
        for line in keyboard:
            for button in line:
                if button.text == button_text:
                    callback_answer = button.callback_data
                    return callback_answer

    async def validate_captcha(self, message: types.Message) -> str:
        message_text = message.caption
        if 'Нажми на радугу' in message_text:
            button_text = '🌈'
            callback_answer = await self.get_captcha_answer(button_text, message)
        elif 'Нажми на банан' in message.caption:
            button_text = '🍌'
            callback_answer = await self.get_captcha_answer(button_text, message)
        else:
            callback_answer = message.reply_markup.inline_keyboard[1][0].callback_data
        return callback_answer

    async def make_callback(self, callback_answer: str, message_id: int) -> None:
        await self.client.request_callback_answer(
            chat_id=self.chat_id,
            message_id=message_id,
            callback_data=callback_answer,
            timeout=5
        )


async def main():
    account = UserClicker('+380 94 491 70 35')
    await account.client.start()
    while True:
        try:
            last_message = await account.get_last_message()
            callback_answer = await account.validate_captcha(last_message)
            await account.make_callback(callback_answer, last_message.id)
        except DataInvalid:
            pass
        except Exception as e:
            print(e)


if __name__ == '__main__':
    asyncio.run(main())
