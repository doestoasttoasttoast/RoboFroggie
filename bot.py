import discord
import os
import re
import pymongo
from dotenv import load_dotenv

load_dotenv()
# grab bot token from .env file
FROGGIE_TOKEN = os.environ.get( 'DISCORD_TOKEN' )

# intents are basically permissions for the bot
intents = discord.Intents.default()
intents.message_content = True

# initialize bot object
client = discord.Client( intents=intents )

    
# connect to and create references to database and collections
froggieDBPassword = os.environ.get( 'ROBO_FROGGIE_DB_PASSWORD' )
dbclient = pymongo.MongoClient( f'mongodb+srv://Seeeab:{froggieDBPassword}@cluster0.c01nt6l.mongodb.net/' )
print( f'connected to mongoDB successfully' )
froggieDB = dbclient['FroggieDB']
attempts = froggieDB['Attempts']
users = froggieDB['Users']

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

    # block for saving wordle scores
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
        
        # store user submission in MongoDB
        entry = { 'discordUserID': msgAuthor.id, 'nickname': msgAuthor.display_name, 'day': day, 'score': score }
        x = users.find_one({}, {'discordUserID': msgAuthor.id} )
        if ( not x ):
            userEntry = { '_id': msgAuthor.id, 'nickname': msgAuthor.display_name }
            users.insert_one( userEntry )
            print( 'user entry added' )
        print( f'attempt entry created for score' )
        attempts.insert_one( entry )
        await message.channel.send( f'{msgAuthor.display_name}, your score has been saved.' )

    if ( messageContent.startswith( 'stats' ) ):
        whitespaceIndex = messageContent.find( " " )
        requestedUser = messageContent[whitespaceIndex + 1 : ]
        requestedUserEntry = users.find_one( {}, { 'nickname': requestedUser} )
        requestedUserID = requestedUserEntry['_id']
        print(requestedUserID)
        queryRequest = { 'discordUserID': requestedUserID }
        query = users.find( queryRequest )
        # TODO: iterate over query ( CURSOR object )
        

#start bot
client.run( FROGGIE_TOKEN )