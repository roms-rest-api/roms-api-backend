import asyncio
import requests
import os

from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Telegram:
    def __init__(self, bot_token, rom_pic_url, buttons):
        self.__BUTTONS = buttons
        self.__ROM_URL = rom_pic_url
        self.__ROM_PIC = self.get_image()
        self.bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot)

    async def send_message(
        self,
        chat_id: str,
        device: str,
        link: str,
        rom_name: str,
        group_name: str,
    ):

        inline_buttons = (InlineKeyboardButton(key, url=link) for key in self.__BUTTONS)
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(*inline_buttons)

        message = (
            f"#{device}\n\n"
            f"{rom_name} for {device}\n\n"
            f"Support group 👉🏻 {group_name}\n"
        )

        # https://github.com/aiogram/aiogram/blob/1e2fe72aca12a3fc6f2d1f66c71539af5a84ea00/examples/broadcast_example.py#L25
        try:
            with open(self.__ROM_PIC, "rb") as photo:
                await self.bot.send_photo(
                    chat_id, photo, caption=message, reply_markup=markup
                )
        except exceptions.BotBlocked:
            logger.error(f"Target [ID:{chat_id}]: blocked by user")
        except exceptions.ChatNotFound:
            logger.error(f"Target [ID:{chat_id}]: invalid user ID")
        except exceptions.RetryAfter as e:
            logger.error(
                f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds."
            )
            await asyncio.sleep(e.timeout)
            return await self.bot.send_photo(
                    chat_id, photo, caption=message, reply_markup=markup
                )  # Recursive call
        except exceptions.UserDeactivated:
            logger.error(f"Target [ID:{chat_id}]: user is deactivated")
        except exceptions.TelegramAPIError:
            logger.exception(f"Target [ID:{chat_id}]: failed")
        else:
            logger.info(f"Target [ID:{chat_id}]: success")
            return True
        return False

    def get_image(self):
        try:
            response = requests.get(self.__ROM_URL)
            pic_name = os.path.basename(self.__ROM_URL)
            open(pic_name, "wb").write(response.content)
            return pic_name
        except Exception as e:
            logger.error(e)
            return None
