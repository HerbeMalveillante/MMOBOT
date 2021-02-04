![image](https://img.shields.io/github/languages/code-size/HerbeMalveillante/MMOBOT)
![image](https://img.shields.io/tokei/lines/github/herbemalveillante/MMOBOT)
![image](https://img.shields.io/github/languages/top/herbemalveillante/mmobot)
![image](https://img.shields.io/github/license/herbemalveillante/mmobot)
![image](https://img.shields.io/github/last-commit/herbemalveillante/mmobot)
[<img src="https://img.shields.io/discord/799331612918939688">](https://discord.gg/vRA4gdraaC)

# MMOBOT

MMOBOT is a powerful discord bot providing an immersive command-line based MMORPG experience in a group chat or server. 

To invite the bot in your server, follow [this link](https://discord.com/oauth2/authorize?client_id=793928798298177537&scope=bot&permissions=379969) (minimal permissions by default)
To join the official bot server, follow [this link](https://discord.gg/vRA4gdraaC)


## Installation and usage

Running an instance of my bot is not recommended. [Just add the official bot instance to your server instead.](https://discord.com/oauth2/authorize?client_id=793928798298177537&scope=bot&permissions=379969)

If you want to run an instance of my bot, you can simply clone the project and run the main.py file. You may need to install modules, including (but not limited to) :

```bash
pip install discord.py
pip install psutils
pip install sqlite3
pip install jishaku
```
### IMPORTANT NOTICE :

To work, the program needs a file named `config.txt` in the root folder containing the following informations :

```JSON
{
	"prefix":"<BOT PREFIX>",
	"description":"<BOT DESCRIPTION>",
	"token":"<BOT TOKEN>",
	"botActivity":"<DEFAULT BOT ACTIVITY>",
	"color":"<DEFAULT (int type) COLOR>",
	"timeout":"<DEFAULT TIME (float, in seconds) BEFORE TIMEOUT>"
}
```

You should also create an empty `stats.csv` file.

## Commands

`help` allow you to see the commands and cog list

`ping` pings the bot

`info` displays infos about the bot

`profile` displays your profile or the profile of an user if specified


Find the complete commands list with the `help` command !

## Contributing
I'm very open if you have any ideas for the bot, improvement and/or bugs to fix.

Send me a message on Discord or open an issue on the GitHub page to fix a bug.

I'm also open if you have any random events / monsters / weapons / items idea. You can write them in English or in French and I would be happy to include them in the content database.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)


Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

## Attributions

Bot custom emotes (icons folder) and pfp from [Flaticon](https://flaticon.com)
