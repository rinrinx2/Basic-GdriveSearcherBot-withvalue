import os
import aiohttp
import json
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
@Client.on_message(filters.command(["imdb", 'im']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('🔎 আইএমডিবি তে খোঁজা হচ্ছে .. \n 🔍...𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐈𝐌𝐃𝐛')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("❌ কিছু পাওয়া যায়নি ❌\n 𝐍𝐨 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐅𝐨𝐮𝐧𝐝 ❌")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('আইএমডিবি হতে যা পেলুম... \n 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐰𝐡𝐚𝐭 𝐢 𝐟𝐨𝐮𝐧𝐝 𝐨𝐧 𝐈𝐌𝐃𝐛', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('মুভি/ সিরিজ এর নাম দিন...\n । 𝐆𝐢𝐯𝐞 𝐦𝐞 𝐚 𝐦𝐨𝐯𝐢𝐞 / 𝐒𝐞𝐫𝐢𝐞𝐬 𝐍𝐚𝐦𝐞')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')} - {imdb.get('year')}",
                    url=imdb['url'],
                )
            ]
        ]
    if imdb.get('poster'):
        await query.message.reply_photo(photo=imdb['poster'], caption=f"IMDb Data:\n\n🏷 <a href={imdb['url']}>{imdb.get('title')}</a>\n\n<b>🎭 Genres:</b> {imdb.get('genres')}\n<b>📆 Year:</b><a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n<b>🌟 Rating:</b> <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10\n\n<i><b>🖋 StoryLine:</b>{imdb.get('plot')} </i>", reply_markup=InlineKeyboardMarkup(btn))
        await query.message.delete()
    else:
        await query.message.edit(f"IMDb Data:\n\n🏷 <a href={imdb['url']}>{imdb.get('title')}</a>\n\n<b>🎭 Genres:</b> {imdb.get('genres')}\n<b>📆 Year:</b> <a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a>\n<b>🌟 Rating:</b>  <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10\n\n<i><b>🖋 StoryLine:</b> {imdb.get('plot')} </i>", reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    await query.answer(b)

posttem = """\n\n ▬▬▬ [❝ 🄻🄸🄽🄺🅂 ❞](https://t.me/BangladeshHoarding) ▬▬▬ \n\n\n\n ▬▬▬▬ [❝ 🄱🄳🄷 ❞](https://t.me/BangladeshHoarding) ▬▬▬▬ \n\n[🚀 𝐉𝐨𝐢𝐧 𝐍𝐨𝐰](https://t.me/BangladeshHoarding) | [💬 𝐈𝐧𝐛𝐨𝐱](https://t.me/BDH_PM_bot) | [🙏 𝐃𝐢𝐬𝐜𝐥𝐚𝐢𝐦𝐞𝐫](https://t.me/BangladeshHoarding/282)"""
@Client.on_message(filters.command(["post", 'p']))
async def postt(client, message):
    if ' ' in message.text:
        k = await message.reply('🔎 আইএমডিবি তে খোঁজা হচ্ছে .. \n 🔍...𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐈𝐌𝐃𝐛')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("❌ কিছু পাওয়া যায়নি ❌\n 𝐍𝐨 𝐫𝐞𝐬𝐮𝐥𝐭𝐬 𝐅𝐨𝐮𝐧𝐝 ❌")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"post#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('আইএমডিবি হতে যা পেলুম... \n 𝐇𝐞𝐫𝐞 𝐢𝐬 𝐰𝐡𝐚𝐭 𝐢 𝐟𝐨𝐮𝐧𝐝 𝐨𝐧 𝐈𝐌𝐃𝐛', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('পোস্ট টেম্পলেট পেতে মুভি/ সিরিজ এর নাম দিন...\n । 𝐆𝐢𝐯𝐞 𝐦𝐞 𝐚 𝐦𝐨𝐯𝐢𝐞 / 𝐒𝐞𝐫𝐢𝐞𝐬 𝐍𝐚𝐦𝐞 To get BDH post template')

@Client.on_callback_query(filters.regex('^post'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')} - {imdb.get('year')}",
                    url=imdb['url'],
                )
            ]
        ]
    if imdb.get('poster'):
        await query.message.reply_photo(photo=imdb['poster'], caption=f"🏷 <b><a href={imdb['url']}>{imdb.get('title')}</a></b>\n\n<b>🎭 Genres:</b> <i>{imdb.get('genres')}</i>\n<b>📆 Year:</b> <i><a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a></i>\n<b>🌟 Rating:</b> <a href={imdb['url']}/ratings>{imdb.get('rating')}</a> / 10\n\n<i><b>🖋 StoryLine:</b> {imdb.get('plot')}</i> {posttem}", reply_markup=InlineKeyboardMarkup(btn))
        await query.message.delete()
    else:
        await query.message.edit(f"🏷 <b><a href={imdb['url']}>{imdb.get('title')}</a></b>\n\n<b>🎭 Genres:</b> <i>{imdb.get('genres')}</i>\n<b>📆 Year:</b> <i><a href={imdb['url']}/releaseinfo>{imdb.get('year')}</a></i>\n<b>🌟 Rating:</b> <i><a href={imdb['url']}/ratings>{imdb.get('rating')}</a></i> / 10\n\n<i><b>🖋 StoryLine:</b> {imdb.get('plot')} </i>{posttem}", reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    await query.answer(b)
      
app.run()   
