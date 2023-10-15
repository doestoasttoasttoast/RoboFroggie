import discord
import os
import sys
from dotenv import load_dotenv

from event_handler import saveScoreEvent, requestPlayerStatsEvent, leaderboardEvent, deleteAllCollectionsEvent

load_dotenv()
# grab bot token from .env file
FROGGIE_TOKEN = os.environ.get( 'DISCORD_TOKEN' )

# intents are basically permissions for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# initialize bot object
client = discord.Client( intents=intents )

@client.event
async def on_ready():
    print( f'{client.user.name} has connected!' )
    sys.stdout.flush()

# react when a message is sent
@client.event
async def on_message( message ):
    # only listen to these two channels
    if not ( message.channel.id == 986042095322144819 
            or message.channel.id == 1159553384999813160 ):
        return
    # ensure the bot doesn't respond to its own messages
    msgAuthor = message.author
    if ( msgAuthor == client.user ):
        return
    
    messageContent = message.content
    print( f'-----Message sent-----\n{msgAuthor}: \n{message.content}')

    # block for saving wordle scores
    if ( messageContent.startswith( 'Wordle ' ) ):
        returnMsg = saveScoreEvent( message )
        await message.channel.send( f'```{returnMsg}```' )
        print( returnMsg )

    # block for seeing player stats
    if ( messageContent.startswith( 'stats ' ) ):
        returnMsg = requestPlayerStatsEvent( message )
        await message.channel.send( f'```{returnMsg}```' )
        print( returnMsg )

    # block for displaying a leaderboard
    if ( messageContent == 'leaderboard' ):
        returnMsg = leaderboardEvent( message, client )
        await message.channel.send( f'```{returnMsg}```' )
        print( returnMsg )

    # block for deleting all collections in mongoDB
    if ( messageContent == 'delete all' and message.channel.id == 1159553384999813160 ):
        returnMsg = deleteAllCollectionsEvent()
        await message.channel.send( f'```{returnMsg}```' )
        print( returnMsg )

    print( '----------------------' )
    sys.stdout.flush()
        

#start bot
client.run( FROGGIE_TOKEN )