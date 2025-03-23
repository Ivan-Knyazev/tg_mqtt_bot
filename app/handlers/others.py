from aiogram import types, Dispatcher


# @nto_dp.message_handler(regexp='(^cat[s]?$|pussy)')
async def cat(message: types.Message):
    with open('data/hello_cat.jpg', 'rb') as photo:
        await message.reply_photo(photo=photo, caption='Привет от котэ 😺')


def register_handlers_others(dp: Dispatcher):
    dp.register_message_handler(cat, regexp='(^cat[s]?$|pussy)')
