from config import TOKEN
from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import os
import webbrowser
import keyboard
import pyautogui
import time

# OPTIONS - - -
mousepix = 50 
keyboardtime = .5
# - - - - - - -

TOKEN = TOKEN

mode: str = "keyboard" # [ keyboard, mouse ]

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

bMode1 = KeyboardButton('💻')
bMode2 = KeyboardButton('🖱️')
modeboard = ReplyKeyboardMarkup(resize_keyboard = True).add(bMode1, bMode2)

bUP = KeyboardButton('⬆️')
bDOWN = KeyboardButton('⬇️')
bLEFT = KeyboardButton('⬅️')
bRIGHT = KeyboardButton('➡️')
bEmpty = KeyboardButton(' ')
bSpace = KeyboardButton('⚪')
moveboard = ReplyKeyboardMarkup(resize_keyboard=True).add(bEmpty, bUP, bEmpty, bLEFT, bSpace, bRIGHT, bEmpty, bDOWN, bEmpty)

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await bot.send_message(message.chat.id, "✔️ Status [ + ]", reply_markup=moveboard)
    await bot.send_message(message.chat.id, f"🚀 Current mode [ {mode} ]\n🖱️ Mouse sensivity [ {mousepix} ] pixels\n💻 Keyboard time [ {keyboardtime} ] seconds")

@dp.message_handler()
async def all_messages(message: types.Message):
    text = message.text
    pos = pyautogui.position()
    px = pos.x
    py = pos.y
    if text.startswith("/mode"):
        global mode
        await bot.send_message(message.chat.id, f"Mode [ {mode} ]", reply_markup=modeboard)
    if text == '🖱️':
        mode = "mouse"
        await bot.send_message(message.chat.id, f"Mode switched to [ {mode} ]", reply_markup=moveboard)
    if text == '💻':
        mode = "keyboard"
        await bot.send_message(message.chat.id, f"Mode switched to [ {mode} ]", reply_markup=moveboard)
    if text.startswith("/set"):
        command = text.split()
        if mode == "mouse":
            global mousepix
            mousepix = int(command[1])
            await bot.send_message(message.chat.id, f"Changed Pixels [ {mousepix} ]", reply_markup=moveboard)
        else:
            global keyboardtime
            keyboardtime = int(command[1])
            await bot.send_message(message.chat.id, f"Changed Time [ {keyboardtime} ]", reply_markup=moveboard)
# - - - - - - - - - - - - - - - MODE - 
    if text == '⬆️':
        if mode == "mouse":
            pyautogui.moveTo(px, py - mousepix)
        else:
            keyboard.press('w')
            time.sleep(keyboardtime)
            keyboard.release('w')
    if text == '⬇️':
        if mode == "mouse":
            pyautogui.moveTo(px, py + mousepix)
        else:
            keyboard.press('s')
            time.sleep(keyboardtime)
            keyboard.release('s')
    if text == '⬅️':
        if mode == "mouse":
            pyautogui.moveTo(px - mousepix, py)
        else:
            keyboard.press('a')
            time.sleep(keyboardtime)
            keyboard.release('a')
    if text == '➡️':
        if mode == "mouse":
            pyautogui.moveTo(px + mousepix, py)
        else:
            keyboard.press('d')
            time.sleep(keyboardtime)
            keyboard.release('d')
    if text == '⚪':
        if mode == "mouse":
            pyautogui.click()
        else:
            keyboard.press('space')
            time.sleep(keyboardtime)
            keyboard.release('space')
# - - - - - - - - - - - - - - - - - - - 
    if text.startswith("/cmd"):
        command = text.split()
        n = command[1::]
        n = ' '.join(n)
        os.system(str(n))
    if text.startswith("/text"):
        command = text.split()
        n = command[1::]
        n = ' '.join(n)
        for c in n:
            keyboard.press(c)
    if text.startswith("/press"):
        command = text.split()
        if len(command) == 2:
            n = command[1]
            keyboard.press(n)
    if text.startswith("/rel"):
        command = text.split()
        if len(command) == 2:
            n = command[1]
            keyboard.release(n)
    if text.startswith("/web"):
        command = text.split()
        if len(command) == 2:
            s = command[1]
            webbrowser.open(f"https://www.google.com/search?q={s}")
    if text.startswith("/url"):
        command = text.split()
        if len(command) == 2:
            s = command[1]
            webbrowser.open(s)
    if text.startswith("/key"):
        command = text.split()
        if len(command) == 2:
            n = command[1]
            keyboard.press_and_release(n)
    if text.startswith("/click"):
        command = text.split()
        if len(command) == 3:
            n = command[1]
            n2 = command[2]
            pyautogui.click(int(n), int(n2))
    if text.startswith("/off "):
        command = text.split()
        if len(command) == 2:
            n = command[1]
            os.system(f"shutdown /s /t {n}")
        elif len(command) == 3:
            if command[1] == "/h":
                n = int(command[2]) * 3600
                os.system(f"shutdown /s /t {n}")
            elif command[1] == "/m":
                n = int(command[2]) * 60
                os.system(f"shutdown /s /t {n}")
    if message.text == "/cancel":
        os.system("shutdown /a")
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('s')
        keyboard.release('d')
        keyboard.release('space')

if __name__ == '__main__':
    executor.start_polling(dp)