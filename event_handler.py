import re
import os
import pymongo

def saveScoreEvent( message ):
    messageContent = message.content
    messageAuthor = message.author
    day = getDayFromMessage( messageContent )
    if ( day == -1 ):
        return 'Invalid day in your attempt'
    score = getScoreFromMessage( messageContent )
    if ( score == -1 ):
        return 'Invalid score in your attempt'
    
    # store user submission in MongoDB
    froggieDB = getMongoDBClient()
    attempts = froggieDB['Attempts']
    users = froggieDB['Users']
    userExists = users.find_one( {'_id': messageAuthor.display_name} )
    if ( not userExists ):
        userEntry = { '_id': messageAuthor.display_name, 'discordUserID': messageAuthor.id }
        users.insert_one( userEntry )
        print( 'new user added to DB' )

    entry = { 'discordUserID': messageAuthor.id, 'nickname': messageAuthor.display_name, 'day': day, 'score': score }
    attempts.insert_one( entry )

    return f'{messageAuthor.display_name}, your score has been saved.'

def retrievePlayerStats( message ):
    froggieDB = getMongoDBClient()
    users = froggieDB['Users']
    attempts = froggieDB['Attempts']

    requestedUser = getUserFromStatRequestMessage( message )
    requestedUserEntry = users.find_one( {'_id': requestedUser} )
    if ( not requestedUserEntry ):
        return f'could not find user with name of {requestedUser}'
    requestedUserID = requestedUserEntry['discordUserID']

    userPoints = 0
    numAttempts = attempts.count_documents( {'discordUserID': requestedUserID} )
    numOneAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 1} )
    userPoints = userPoints + 7
    numTwoAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 2} )
    userPoints = userPoints + 6
    numThreeAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 3} )
    userPoints = userPoints + 5
    numFourAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 4} )
    userPoints = userPoints + 4
    numFiveAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 5} )
    userPoints = userPoints + 3
    numSixAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 6} )
    userPoints = userPoints + 2
    numFailedAttempts = attempts.count_documents( {'discordUserID': requestedUserID, 'score': 0} )
    userPoints = userPoints + 1
    
    return f'''{requestedUser} has {numAttempts} total attempts with {userPoints} points
    > 1/6 attempts: {numOneAttempts}
    > 2/6 attempts: {numTwoAttempts}
    > 3/6 attempts: {numThreeAttempts}
    > 4/6 attempts: {numFourAttempts}
    > 5/6 attempts: {numFiveAttempts}
    > 6/6 attempts: {numSixAttempts}
    > X/6 attempts: {numFailedAttempts}'''

# open a new MongoDB client to store and request data
def getMongoDBClient():
    froggieDBPassword = os.environ.get( 'ROBO_FROGGIE_DB_PASSWORD' )
    dbclient = pymongo.MongoClient( f'mongodb+srv://Seeeab:{froggieDBPassword}@cluster0.c01nt6l.mongodb.net/' )
    print( 'connected to MongoDB successfully' )
    return dbclient['FroggieDB']

# use regex to get the day (3-4 digit number) from the message
def getDayFromMessage( messageContent ):
    dayGroup = re.search( r'(\s[0-9]{3}\s)|(\s[0-9]{4}\s)', messageContent )
    if (not dayGroup):
        return -1
    day = int( dayGroup.group().strip() )
    return day

# use regex to get the score (digits 1-6 or X for failure) from the message
def getScoreFromMessage( messageContent ):
    scoreGroup = re.search( r'\s([1-6]|X)/6', messageContent )
    if (not scoreGroup):
        return -1
    scoreStr = scoreGroup.group().strip()[0]
    if ( scoreStr == 'X' ):
        scoreStr = '0'
    score = int( scoreStr )
    return score

def getUserFromStatRequestMessage( message ):
    messageContent = message.content
    whitespaceIndex = messageContent.find( " " )
    requestedUser = messageContent[whitespaceIndex + 1 : ]
    return requestedUser