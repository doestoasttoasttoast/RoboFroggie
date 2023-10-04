import discord
import os
import re
from dotenv import load_dotenv

load_dotenv()
# grab bot token from .env file
FROGGIE_TOKEN = os.environ.get( 'DISCORD_TOKEN' )

# TODO: learn what this is
intents = discord.Intents.default()
intents.message_content = True

# initialize bot object
client = discord.Client( intents=intents )

@client.event
async def on_ready():
    print( f'{client.user.name} has connected!' )

@client.event
async def on_message( message ):
    msgAuthor = message.author
    if ( msgAuthor == client.user ):
        return
    
    messageContent = message.content
    print( f'-----Message sent-----\n{msgAuthor}: \n{message.content}\n-----')
    if ( messageContent.startswith( 'Wordle ' ) ):
        # use regex to extract the day (either a 3 or 4 digit number)
        dayGroup = re.search( r'(\s[0-9]{3}\s)|(\s[0-9]{4}\s)', messageContent )
        if (not dayGroup):
            print( f'regex failed to parse day' )
            return
        day = int( dayGroup.group().strip() )
        
        # use regex to extract the score
        scoreGroup = re.search( r'\s([1-6]|X)/6', messageContent )
        if (not scoreGroup):
            print( f'regex failed to parse score' )
            return
        score = int( scoreGroup.group().strip()[0] )
        
        print( f'{msgAuthor} played Wordle {day} and got a score of {score}' )
        await message.channel.send( f'{msgAuthor}, your score has been saved.' )

#start bot
client.run( FROGGIE_TOKEN )