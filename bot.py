from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from decouple import config

TOKEN = config("TOKEN")

# Список админов
ADMINS = [5983514379]

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def ignore_start(message: Message):
    await message.answer('Опишите, с какой проблемой вы столкнулись — мы обязательно вам поможем!')


# -------- Пользователь пишет в поддержку --------
@dp.message(~F.from_user.id.in_(ADMINS))
async def user_message(message: Message):
    username = f"@{message.from_user.username}" if message.from_user.username else "—"

    header = (
        f"Новое сообщение от пользователя:\n\n"
        f"👤 ID: {message.from_user.id}\n"
        f"🟦 Username: {username}\n"
    )

    # Кнопка «Ответить»
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Ответить",
            callback_data=f"reply_{message.from_user.id}"
        )
    ]])

    for admin_id in ADMINS:

        # Если фото
        if message.photo:
            await bot.send_message(admin_id, header, reply_markup=kb)
            await bot.send_photo(
                admin_id,
                message.photo[-1].file_id,
                caption=message.caption or ""
            )
            continue

        # Если документ
        if message.document:
            await bot.send_message(admin_id, header, reply_markup=kb)
            await bot.send_document(
                admin_id,
                message.document.file_id,
                caption=message.caption or ""
            )
            continue

        # Видео
        if message.video:
            await bot.send_message(admin_id, header, reply_markup=kb)
            await bot.send_video(
                admin_id,
                message.video.file_id,
                caption=message.caption or ""
            )
            continue

        # Голос
        if message.voice:
            await bot.send_message(admin_id, header, reply_markup=kb)
            await bot.send_voice(
                admin_id,
                message.voice.file_id,
                caption=message.caption or ""
            )
            continue

        # Текст
        if message.text:
            await bot.send_message(
                admin_id,
                header + "\n💬 " + message.text,
                reply_markup=kb
            )

    await message.answer("Ваше сообщение отправлено в поддержку.")


# -------- Админ нажимает «Ответить» --------
@dp.callback_query(F.data.startswith("reply_"))
async def admin_reply_button(callback):
    user_id = int(callback.data.split("_")[1])
    await callback.message.answer(
        f"Введите сообщение для отправки пользователю {user_id}:"
    )
    # сохраняем, кому нужно ответить
    dp["reply_to"] = user_id


# -------- Админ пишет ответ --------
@dp.message(F.from_user.id.in_(ADMINS))
async def admin_send_answer(message: Message):
    user_id = dp.get("reply_to")
    if not user_id:
        return await message.answer("Используйте кнопку 'Ответить' под сообщением.")

    await bot.send_message(user_id, f"Ответ поддержки:\n\n{message.text}")
    await message.answer("Ответ отправлен пользователю.")
    dp["reply_to"] = None


# -------- Старт --------
if __name__ == "__main__":
    dp.run_polling(bot)
