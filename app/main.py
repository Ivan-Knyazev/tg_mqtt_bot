import logging
import asyncio
from aiogram import executor

import app.settings as sets
from app.utils.callback import check
from app.handlers import about, mqtt, others

# TELEGRAM BOT
nto_dp = sets.nto_dp

about.register_handlers_about(nto_dp)
mqtt.register_handlers_mqtt(nto_dp)
others.register_handlers_others(nto_dp)


async def on_startup(_):
    # print('Bot is running')
    asyncio.create_task(check())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(nto_dp, skip_updates=True, on_startup=on_startup)
