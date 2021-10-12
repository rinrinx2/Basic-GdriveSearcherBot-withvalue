import os
from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty, MessageNotModified
from pyrogram.errors import QueryIdInvalid
from configs import RESULTS_COUNT, SUDO_CHATS_ID, SUDO_CHATS_ID_GS
from drive import drive
from requests import get as g

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

i = 0
ii = 0
m = None
keyboard = None
data = None

@Bot.on_message(filters.command("help") & ~filters.edited)
async def help_command(_, message):
    await message.reply_text("গুগল ড্রাইভ হতে ফাইল খুঁজতে /search [FileName] অথবা /find [FileName] অথবা /s [FileName] অথবা /f [FileName] কমান্ড ব্যবহার করুন, টেলিগ্রাম ফাইল খুঁজতে ইনলাইন সার্চ ব্যাবহার করুন")


@Bot.on_message(filters.command("search") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
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


@Bot.on_callback_query(filters.regex("previous"))
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


@Bot.on_callback_query(filters.regex("next"))
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

      
@Bot.on_message(filters.command("find") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
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


@Bot.on_callback_query(filters.regex("previous"))
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


@Bot.on_callback_query(filters.regex("next"))
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

@Bot.on_message(filters.command("gs") & ~filters.edited & filters.chat(SUDO_CHATS_ID_GS))
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


@Bot.on_callback_query(filters.regex("previous"))
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


@Bot.on_callback_query(filters.regex("next"))
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

@Bot.on_message(filters.command("s") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
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


@Bot.on_callback_query(filters.regex("previous"))
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


@Bot.on_callback_query(filters.regex("next"))
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

@Bot.on_message(filters.command("f") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
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


@Bot.on_callback_query(filters.regex("previous"))
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


@Bot.on_callback_query(filters.regex("next"))
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
      
@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
    await event.reply_text(
        "হ্যালো, সার্চ কমান্ড জানতে /help দেখুন।  \n💚@BangladeshHoarding💚\n\n"
        "**Mod By Alex Stuart:**\n",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Support", url="https://t.me/BDH_PM_bot"),
             InlineKeyboardButton("Bangladesh Hoarding", url="https://t.me/Bangladeshhoarding")],
            [InlineKeyboardButton("Mod by Alex Stuart", url="https://t.me/BDH_PM_bot")],
            [InlineKeyboardButton("Search TG Files Inline", switch_inline_query_current_chat=""), InlineKeyboardButton("Go Inline", switch_inline_query="")]
        ])
    )


@Bot.on_inline_query()
async def inline_handlers(_, event: InlineQuery):
    answers = list()
    # If Search Query is Empty
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="Inline Telegaram Search Bot!",
                description="You can search telegaram files using this bot.",
                input_message_content=InputTextMessageContent(
                    message_text="Using this Bot you can Search telegram files using this bot.\n\n"
                                 "Made by Alex Stuart",
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Search Here", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton("Support", url="https://t.me/BDH_PM_bot"),
                     InlineKeyboardButton("Channel", url="https://t.me/Bangladeshhoarding")],
                    [InlineKeyboardButton("Mod By Alex Stuart", url="https://t.me/BDH_PM_bot")]
                ])
            )
        )
    # Search Channel Message using Search Query Words
    else:
        async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.query):
            if message.text:
                answers.append(InlineQueryResultArticle(
                    title="{}".format(message.text.split("\n", 1)[0]),
                    description="{}".format(message.text.rsplit("\n", 1)[-1]),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]]),
                    input_message_content=InputTextMessageContent(
                        message_text=message.text.markdown,
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                ))
    try:
        await event.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.BOT_SESSION_NAME}] - Answered Successfully - {event.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")

# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.run()
User.run()

