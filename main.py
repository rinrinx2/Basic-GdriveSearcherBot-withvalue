from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageEmpty, MessageNotModified
from config import BOT_TOKEN, RESULTS_COUNT, SUDO_CHATS_ID
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
    await message.reply_text("𝐖𝐡𝐚𝐭 𝐝𝐢𝐝 𝐲𝐨𝐮 𝐞𝐱𝐩𝐞𝐜𝐭 𝐭𝐨 𝐡𝐚𝐩𝐩𝐞𝐧? 𝐓𝐫𝐲 /help 💚@BangladeshHoarding💚")


@app.on_message(filters.command("help") & ~filters.edited)
async def help_command(_, message):
    await message.reply_text("/search [Query]")


@app.on_message(filters.command("search") & ~filters.edited & filters.chat(SUDO_CHATS_ID))
async def search(_, message):
    global i, m, data
    if len(message.command) < 2:
      await message.reply_text('/seach Filename')
      return
    query = message.text.split(' ',maxsplit=1)[1]
    m = await message.reply_text("**🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 🔍..𝐏𝐥𝐞𝐚𝐬𝐞🙏𝐰𝐚𝐢𝐭..💚@BangladeshHoarding💚**")
    data = drive.drive_list(query)
    
    results = len(data)
    i = 0
    i = i + RESULTS_COUNT

    if results == 0:
        await m.edit(text="sorry😐 Found Literally Nothing.You have to mirror it...💚@BangladeshHoarding💚")
        return

    text = f"**🔎 𝐓𝐨𝐭𝐚𝐥 𝐑𝐞𝐬𝐮𝐥𝐭𝐬:** __{results}__ (Use Index Links)\n"
    for count in range(min(i, results)):
        if data[count]['type'] == "file":
            text += f"""
📄  [{data[count]['name']}
**Size:** __{data[count]['size']}__
**[❌ 𝐃𝐫𝐢𝐯𝐞]({data[count]['drive_url']})**   |🟠|   **[✅📄 𝐃𝐢𝐫𝐞𝐜𝐭 𝐅𝐢𝐥𝐞 𝐋𝐢𝐧𝐤]({data[count]['url']})**\n"""

        else:
            text += f"""
📂  __{data[count]['name']}__
**[❌ 𝐃𝐫𝐢𝐯𝐞]({data[count]['drive_url']})**   |🟠|   **[✅📂 𝐈𝐧𝐝𝐞𝐱 𝐅𝐨𝐥𝐝𝐞𝐫 𝐋𝐢𝐧𝐤]({data[count]['url']})**

*𝙎𝙚𝙖𝙧𝙘𝙝 𝙄𝙣𝙙𝙚𝙭𝙚𝙙 𝘽𝙮 💚@BangladeshHoarding\n"""
    if len(data) > RESULTS_COUNT:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="<< ⏮️ Previous",
                        callback_data="previous"
                    ),
                    InlineKeyboardButton(
                        text="Next ⏭️ >>",
                        callback_data="next"
                    )
                ]
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
            "𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐚𝐭 𝟏𝐬𝐭 𝐩𝐚𝐠𝐞, 𝐂𝐚𝐧'𝐭 𝐠𝐨 𝐛𝐚𝐜𝐤.",
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
📄  [{data[count]['name']}
**Size:** __{data[count]['size']}__
**[❌ 𝐃𝐫𝐢𝐯𝐞]({data[count]['drive_url']})**   |🟠|   **[✅📄 𝐃𝐢𝐫𝐞𝐜𝐭 𝐅𝐢𝐥𝐞 𝐋𝐢𝐧𝐤]({data[count]['url']})**\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
**[❌ 𝐃𝐫𝐢𝐯𝐞]({data[count]['drive_url']})**  |🟠|  **[✅📂 𝐈𝐧𝐝𝐞𝐱 𝐅𝐨𝐥𝐝𝐞𝐫 𝐋𝐢𝐧𝐤]({data[count]['url']})**

*𝙎𝙚𝙖𝙧𝙘𝙝 𝙄𝙣𝙙𝙚𝙭𝙚𝙙 𝘽𝙮 💚@BangladeshHoarding\n"""
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<< ⏮️ Previous",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text="Next ⏭️ >>",
                    callback_data="next"
                )
            ]
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
📄  [{data[count]['name']}
**Size:** __{data[count]['size']}__
**[❌ 𝐃𝐫𝐢𝐯𝐞]({data[count]['drive_url']})**   |🟠|   **[✅📄𝐃𝐢𝐫𝐞𝐜𝐭 𝐅𝐢𝐥𝐞 𝐋𝐢𝐧𝐤]({data[count]['url']})**\n"""

            else:
                text += f"""
📂  __{data[count]['name']}__
**[❌ 𝐃𝐫𝐢𝐯𝐞]({data[count]['drive_url']})**   |🟠|   **[✅📂𝐈𝐧𝐝𝐞𝐱 𝐅𝐨𝐥𝐝𝐞𝐫 𝐋𝐢𝐧𝐤]({data[count]['url']})**

*𝙎𝙚𝙖𝙧𝙘𝙝 𝙄𝙣𝙙𝙚𝙭𝙚𝙙 𝘽𝙮 💚@BangladeshHoarding\n"""
        except IndexError:
            continue

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="<< ⏮️ Previous",
                    callback_data="previous"
                ),
                InlineKeyboardButton(
                    text="Next ⏭️ >>",
                    callback_data="next"
                )
            ]
        ]
    )
    try:
        await m.edit(text=text, disable_web_page_preview=True, reply_markup=keyboard)
    except (MessageEmpty, MessageNotModified):
        pass


app.run()
