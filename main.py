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


@app.on_message(filters.command("search") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def search(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('ফাইল খুঁজতে /search [FileName] কমান্ড ব্যবহার করুন')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 ফাইলটি খোঁজা হচ্ছে 🔎..অপেক্ষা করুন 🙏.. \n 💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="দুঃখিত 😐, কোন ফাইল পাওয়া যায়নি, অথবা আপনি ভুল নামে খুঁজছেন... @imdbot বট হতে সঠিক নাম জেনে নিন । \n 💚@BangladeshHoarding💚")
        return

    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ \n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
  |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                    InlineKeyboardButton(
                        text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                        url="https://t.me/Bangladeshhoarding"
                    )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|  **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
 |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass

      
@app.on_message(filters.command("find") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def find(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('ফাইল খুঁজতে /find [FileName] কমান্ড ব্যবহার করুন')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 ফাইলটি খোঁজা হচ্ছে 🔎..অপেক্ষা করুন 🙏.. \n 💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="দুঃখিত 😐, কোন ফাইল পাওয়া যায়নি, অথবা আপনি ভুল নামে খুঁজছেন... @imdbot বট হতে সঠিক নাম জেনে নিন । \n 💚@BangladeshHoarding💚")
        return 
      
    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ \n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
  |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                    InlineKeyboardButton(
                        text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                        url="https://t.me/Bangladeshhoarding"
                    )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|  **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
 |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass

@app.on_message(filters.command("gs") & ~filters.edited & filters.chat(SUDO_CHATS_ID_GS))
async def gs(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('😡 এডমিন কমান্ড 😡')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 ফাইলটি খোঁজা হচ্ছে 🔎..অপেক্ষা করুন 🙏.. \n 💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="দুঃখিত 😐, কোন ফাইল পাওয়া যায়নি, অথবা আপনি ভুল নামে খুঁজছেন... @imdbot বট হতে সঠিক নাম জেনে নিন । \n 💚@BangladeshHoarding💚")
        return 
      
    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ \n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
   **[✅📄 ⚡️ড্রাইভ লিংক⚡️]({data[count]['drive_url']})** |🇧🇩| **[✅📄 ⚡ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
  **[✅📂 ⚡️ড্রাইভ লিংক⚡️]({data[count]['drive_url']})** |🇧🇩| **[✅📂 ⚡ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                    InlineKeyboardButton(
                        text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                        url="https://t.me/Bangladeshhoarding"
                    )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
   **[✅📄 ⚡️ড্রাইভ লিংক⚡️]({data[count]['drive_url']})** |🇧🇩| **[✅📄 ⚡ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
  **[✅📂 ⚡️ড্রাইভ লিংক⚡️]({data[count]['drive_url']})** |🇧🇩| **[✅📂 ⚡ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
   **[✅📄 ⚡️ড্রাইভ লিংক⚡️]({data[count]['drive_url']})** |🇧🇩| **[✅📄 ⚡ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
  **[✅📂 ⚡️ড্রাইভ লিংক⚡️]({data[count]['drive_url']})** |🇧🇩| **[✅📂 ⚡ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass

@app.on_message(filters.command("s") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def s(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('ফাইল খুঁজতে /s [FileName] কমান্ড ব্যবহার করুন')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 ফাইলটি খোঁজা হচ্ছে 🔎..অপেক্ষা করুন 🙏.. \n 💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="দুঃখিত 😐, কোন ফাইল পাওয়া যায়নি, অথবা আপনি ভুল নামে খুঁজছেন... @imdbot বট হতে সঠিক নাম জেনে নিন । \n 💚@BangladeshHoarding💚")
        return

    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ \n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
  |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                    InlineKeyboardButton(
                        text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                        url="https://t.me/Bangladeshhoarding"
                    )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|  **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
 |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass

@app.on_message(filters.command("f") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def f(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('ফাইল খুঁজতে /f [FileName] কমান্ড ব্যবহার করুন')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 ফাইলটি খোঁজা হচ্ছে 🔎..অপেক্ষা করুন 🙏.. \n 💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="দুঃখিত 😐, কোন ফাইল পাওয়া যায়নি, অথবা আপনি ভুল নামে খুঁজছেন... @imdbot বট হতে সঠিক নাম জেনে নিন । \n 💚@BangladeshHoarding💚")
        return

    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ \n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
  |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                    InlineKeyboardButton(
                        text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                        url="https://t.me/Bangladeshhoarding"
                    )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
  |🇧🇩|  **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
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
📄  {data[count]['name']}
**📀 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞:** __{data[count]['size']}__
 |🇧🇩|   **[✅📄 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
 |🇧🇩|   **[✅📂 ⚡️ইনডেক্স লিংক⚡️]({data[count]['url']})**
╠▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬╣
@BangladeshHoarding\n"""
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
                InlineKeyboardButton(
                    text="🇧🇩 𝕭𝖆𝖓𝖌𝖑𝖆𝖉𝖊𝖘𝖍 𝕳𝖔𝖆𝖗𝖉𝖎𝖓𝖌 🇧🇩", 
                    url="https://t.me/Bangladeshhoarding"
                )
            ],
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass      
      
app.run()   
