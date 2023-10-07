# FroggieBot
This is a discord bot used in the FroggiePond discord to keep track of everyoness Wordle scores.
Developed by: [Seab](https://github.com/doestoasttoasttoast)

## Development and Technologies
The bot was developed in Python 3.11, using the library [discord.py](https://discordpy.readthedocs.io/en/stable/index.html)
An image was created using Docker, and hosted by Oracle
Data storage is handled by [MongoDB](cloud.mongodb.com), and can be interacted with in Python using [pymongo](https://pymongo.readthedocs.io/en/stable/)

## Usage
- Users can store their score by simply pasting their wordle clipboard into the `word-nerds` channel. Doing so will prompt the bot to respond with their history of attempts and their total score.
- Users can request the stats of a certain player to see their history of attempts and total score.
     - `stats <username>`, replacing \<username\> with the desired user.
- Users can see the leaderboard, which is listed in order of the users with the highest scores.
     - `leaderboard`
     - Scoring is done by the following metrics:
          - 1/6 attempts: 7 points
          - 2/6 attempts: 6 points
          - 3/6 attempts: 5 points
          - 4/6 attempts: 4 points
          - 5/6 attempts: 3 points
          - 6/6 attempts: 2 points
          - X/6 attempts: 1 point
     - This is done so that users still get a point just for trying, even if they fail. This is to encourage people to post even their bad scores. Leaderboards will not track which users score the lowest on average, as this is easily exploitable by someone only posting scores which they do good with.
