# Message-Search-Bot
A Telegram Bot for searching any channel messages from Inline by [@AbirHasan2005](https://github.com/AbirHasan2005).

I made this for [@AHListBot](https://t.me/AHListBot). You can use this for something else. Edit according to your use.

We have to use Bot for Inline Search & Userbot for Searching in Channels. So both Bot & Userbot will work together.

## Deploy to Heroku:
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AbirHasan2005/Message-Search-Bot)

### Support Group:
<a href="https://t.me/DevsZone"><img src="https://img.shields.io/badge/Telegram-Join%20Telegram%20Group-blue.svg?logo=telegram"></a>

### Follow on:
<p align="left">
<a href="https://github.com/AbirHasan2005"><img src="https://img.shields.io/badge/GitHub-Follow%20on%20GitHub-inactive.svg?logo=github"></a>
</p>
<p align="left">
<a href="https://twitter.com/AbirHasan2005"><img src="https://img.shields.io/badge/Twitter-Follow%20on%20Twitter-informational.svg?logo=twitter"></a>
</p>
<p align="left">
<a href="https://facebook.com/AbirHasan2005"><img src="https://img.shields.io/badge/Facebook-Follow%20on%20Facebook-blue.svg?logo=facebook"></a>
</p>
<p align="left">
<a href="https://instagram.com/AbirHasan2005"><img src="https://img.shields.io/badge/Instagram-Follow%20on%20Instagram-important.svg?logo=instagram"></a>
</p>

# GdriveSearcherBot
#### Google Drive Searcher Bot Written In Python Using Pyrogram. 


[![Python](http://forthebadge.com/images/badges/made-with-python.svg)](https://python.org)

<img src="https://i.imgur.com/MxrswfJ.png" width="370" align="right">


### Installation

##### Getting Google OAuth API credential file
- Visit the [Google Cloud Console](https://console.developers.google.com/apis/credentials)
- Go to the OAuth Consent tab, fill it, and save.
- Go to the Credentials tab and click Create Credentials -> OAuth Client ID
- Choose Desktop and Create.
- Use the download button to download your credentials.
- Move that file to the root of this bot, and rename it to credentials.json
- Visit [Google API page](https://console.developers.google.com/apis/library)
- Search for Drive and enable it if it is disabled
- Run these commands

```sh
$ pip3 install -U pip
$ pip3 install -U -r requirements.txt
$ python3 generate_drive_token.py
$ cp sample_config.py config.py
```
- Edit **config.py** with your own values
- Run  ```$ python3 main.py```  to start the bot.

### Docker Installation
```sh
$ git clone https://github.com/thehamkercat/GdriveSearcherBot
$ cd GdriveSearcherBot
$ sudo docker build . -t GdriveSearcherBot
$ sudo docker run GdriveSearcherBot
```
### Credits
[@SVR666](https://github.com/SVR666) For Drive module.

### Notes
- Join [PatheticProgrammers](https://t.me/patheticprogrammers) For Help.
