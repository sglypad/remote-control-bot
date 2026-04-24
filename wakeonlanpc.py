import psutil
import subprocess
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio
import time
import os
import datetime 
from datetime import timedelta

TOKEN = "IMPORT TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)
def main_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 System Status", callback_data="sys_monitor")],
        [InlineKeyboardButton(text="🕒 Uptime", callback_data="uptime")],
        [InlineKeyboardButton(text="😴 Sleep", callback_data="sleep")],
        [InlineKeyboardButton(text="🔴 Turn Off", callback_data="off")]
    ])
    return keyboard

# --- Команды (сообщения) ---
@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello! I control your PC🖥", reply_markup=main_keyboard())

@router.message(Command("status"))
async def status(message: Message):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    await message.answer(f"📈 CPU: {cpu}%\n🧠 RAM: {ram.percent}%")

@router.message(Command("off"))
async def off(message: Message):
    await message.answer("Turning off.... 🔌")
    # subprocess.run(["shutdown", "-h", "now"]) # Пока закомментил, чтоб случайно не выключил

# --- Кнопки (колбэки) ---
@router.callback_query(F.data == "sys_monitor")
async def monitor_callback(callback: CallbackQuery):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()

    used_gb = round(ram.used / (1024**3), 2)
    total_gb = round(ram.total / (1024**3), 2)
    

    text = (
        f"📊 **System status:**\n\n"
        f"📈 CPU: {cpu}%\n"
        f"🧠 RAM: {ram.percent}% {used_gb} ГБ / {total_gb} ГБ")
    await callback.message.answer(text) # type: ignore
    await callback.answer()
@router.callback_query(F.data == "uptime")
async def uptime_callback(callback: CallbackQuery):
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot_time

    uptime_str = str(uptime).split('.')[0]

    await callback.message.answer(f"🕒 PC Uptime: {uptime_str}")
    await callback.answer()

@router.callback_query(F.data == "sleep")
async def sleep_callback(callback: CallbackQuery):
    await callback.message.answer("Going into sleep... 😴")
    await callback.answer

    subprocess.run(["systemctl", "suspend"])

@router.callback_query(F.data == "off")
async def off_callback(callback: CallbackQuery):
    text = "In case I don't see ya, good afternoon, good evening and good night.."

    await callback.message.answer(text)
    await callback.bot.send_message()

    import asyncio
    await asyncio.sleep(1)


    subprocess.run(["systemctl", "poweroff"])



# --- ЗАПУСК (самый низ файла) ---
async def main():
    print(">>> BOT IS WORKING! Type /start in telegram.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot is turned off.")
