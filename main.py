import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty, MessageNotModified
from config import BOT_TOKEN, RESULTS_COUNT, SUDO_CHATS_ID, SUDO_CHATS_ID_GS
from drive import drive
from requests import get as g

app = Client(":memory:", bot_token=BOT_TOKEN, api_id=6,
             api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

i = 0
ii = 0
m = None
keyboard = None
data = None


@app.on_message(filters.command("start") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def start_command(_, message):
    await message.reply_text("হ্যালো, সার্চ কমান্ড জানতে /help দেখুন।  \n💚@BangladeshHoarding💚")


@app.on_message(filters.command("help") & ~filters.edited)
async def help_command(_, message):
    await message.reply_text("ফাইল খুঁজতে /search [FileName] অথবা /find [FileName] অথবা /s [FileName] অথবা /f [FileName] কমান্ড ব্যবহার করুন")


@app.on_message(filters.command(["search", "find", "f", "s", "list"]) & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def search(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('ফাইল খুঁজতে নিচের কমান্ড গুলো ব্যবহার করুন \n /search [FileName] \n /find [FileName] \n /s [FileName] \n /f [FileName] \n\n এইভাবে খুঁজুনঃ /s Avenger')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 ফাইলটি খোঁজা হচ্ছে 🔎..অপেক্ষা করুন 🙏.. \n\n 💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="দুঃখিত 😐, কোন ফাইল পাওয়া যায়নি, অথবা আপনি ভুল নামে খুঁজছেন... @imdb বট হতে সঠিক নাম জেনে নিন । \n\n 💚@BangladeshHoarding💚")
        return

    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ \n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
✅**[ {data[count]['name']} ]({data[count]['url']})**
**📀𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
"""

        else:
            text += f"""
✅**[ {data[count]['name']} ]({data[count]['url']})**
"""
    if len(data) > RESULTS_COUNT:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="<< ⏮️ পূর্ববর্তী",
                        callback_data="previous"
                    ),
                    InlineKeyboardButton(
                        text="পরবর্তী ⏭️ >>",
                        callback_data="next"
                    )                  
                ],
                [
                    InlineKeyboardButton("🔍 টেলিগ্রাম ফাইল সার্চ 🔍", switch_inline_query_current_chat="")
                ],
            ]
        )
        try:
            await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
        except (MessageEmpty, MessageNotModified):
            pass
        return
    try:
        await m.edit(text=text, disable_web_page_preview=True)
    except (MessageEmpty, MessageNotModified):
        pass


@app.on_callback_query(filters.regex("previous"))
async def previous_callbacc(_, CallbackQuery):
    global i, ii, m, data
    if i < RESULTS_COUNT:
        await CallbackQuery.answer(
            "আপনি প্রথম পেইজে আছেন...",
            show_alert=True
        )
        return
    ii -= RESULTS_COUNT
    i -= RESULTS_COUNT
    text = ""

    for count in range(ii, i):
        try:
            if data[count]['type'] == "file":
                text += f"""
✅**[ {data[count]['name']} ]({data[count]['url']})**
**📀𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
"""

            else:
                text += f"""
✅**[ {data[count]['name']} ]({data[count]['url']})**
"""
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<< ⏮️ পূর্ববর্তী",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text="পরবর্তী ⏭️ >>",
                    callback_data="next"
                )              
            ],
            [
                InlineKeyboardButton("🔍 টেলিগ্রাম ফাইল সার্চ 🔍", switch_inline_query_current_chat="")
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass


@app.on_callback_query(filters.regex("next"))
async def next_callbacc(_, CallbackQuery):
    global i, ii, m, data
    ii = i
    i += RESULTS_COUNT
    text = ""

    for count in range(ii, i):
        try:
            if data[count]['type'] == "file":
                text += f"""
✅**[ {data[count]['name']} ]({data[count]['url']})**
**📀𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
"""

            else:
                text += f"""
✅**[ {data[count]['name']} ]({data[count]['url']})**
"""
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<< ⏮️ পূর্ববর্তী",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text="পরবর্তী ⏭️ >>",
                    callback_data="next"
                )              
            ],
            [
                InlineKeyboardButton("🔍 টেলিগ্রাম ফাইল সার্চ 🔍", switch_inline_query_current_chat="")
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass
      
      
app.run()   
