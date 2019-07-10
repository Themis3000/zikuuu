#Zikuuu
######*A fun(ish) discord bot*
##Setup
* Set local var "TOKEN" to your discord bot token
* Set local var "MONGO_SERVER", "MONGO_USER", and "MONGO_PASS" to your mongodb server's address, username, and password
* Make sure you have all dependencies in "requirements.txt" fulfilled
* Rurururun that! (with python3)
* Change newly created config.json file to suit your needs (don't forget to make yourself admin of the bot)

##config.json
Config.json is set up in an, erm, *interesting* way. So let me take you through the basics of the structure
```
"repository": [
   {
      "current": "https://github.com/Themis3000/zikuuu.git"
   },
   {
      "options": [
         "ANY"
      ]
   }
```
So here's an example of a setting called "repository". The "current" is what "repository" is currently set to. "options"
tells you what you are allowed to set it to (in this case anything)

Here's another example:
```
"status_booting": [
   {
      "current": "idle"
   },
   {
      "options": [
         "online",
         "idle",
         "offline",
         "dnd"
      ]
   }
]
```
So here "status_booting" is set to "idle" and it can only be set to "online", "idle", "offline", or "dnd"
####config.json reference
Setting | Meaning
--------|--------
status | The default status the bot will mark it's self as when it finishes starting up
status_booting | The status for the bot when it is starting up
game | The default game the bot will mark it's self as playing after it starts up
game_booting | The default game the bot will mark it's self as playing while it is starting up
prefix | The prefix before a command (eg. +/! +slots/!slots)
unload_cog | Does absolutely nothing!
bot_owners | Set who owns the bot
repository | The repo link for this bot

##commands reference
Command | Function
--------|---------
allow | Allow someone to join the voice channel you are in one time only
change_config | Allows the bot owner to change the bots config settings
ping | Pong!
repo | View the git repo for this bot
set_game | Sets the status of the bot (online, offline, dnd, busy)
set_status | Sets the bot online status
battle | Heck someone up and take their coinz gang gang style
buypet | Get yo self a pet for your travels
coinz | Checks the amount of cool coinz you have
getcoinz | Claim some of that mulah
slots | Lose your life savings in a game of slots!
slotspayouts | Get tempted into playing slots
stats | Show off your superiority
dadjoke | Get a dad joke from the dada-base (aka icanhazdadjoke.com)
help | Shows the help message


Be sure to send all of your money to tcm4760@gmail.com on paypal