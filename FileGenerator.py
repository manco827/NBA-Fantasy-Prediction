# File:        FileGenerator.py
# Description: This file creates CSV files with historical player data and team data. These files will be used by Backend.py
#              to predict Fantasy Points

# Import all necessary libraries
import pandas as pd # Used for data processing and manipulation
from nba_py import player # Access to API used to retrieve NBA data
import boto3 # Used to connect and upload to S3

# Creates a list of all available seasons to pull data from and creates pandas DF (dataframe) to store player averages
seasons = ['2013-14','2014-15','2015-16','2016-17','2017-18']
playerAvgDF = pd.DataFrame()
curSeason = '2017-18'

# Creates an S3 client to upload files to S3
s3 = boto3.client('s3', aws_access_key_id='********************', aws_secret_access_key='****************************************')
bucket = 'hadoop-data-bucket'

# Iterate through season list and retrieve data
for season in seasons:

    # Create DF to store season player data and retrieve list of all players as a JSON
    seasonDF = pd.DataFrame()
    playerList = player.PlayerList(league_id='00', season=season, only_current=1).json

    #  Iterate through each player in player
    for players in playerList['resultSets'][0]['rowSet']:

        # Use player ID to retrieve all games for that player and store as a pandas DF
        playerID = players[0]
        gameJSON = player.PlayerGameLogs(playerID, '00', season).json
        gameList = gameJSON['resultSets'][0]['rowSet'][::-1]
        gameDF = pd.DataFrame(gameList) # Use .head(num) to limit game data used (useful for lcoal testing)

        # Get only certain stats and append to overall season dataframe, skip if no games played
        try:
            seasonDF=seasonDF.append(gameDF[[4, 6] + range(18,25)],ignore_index=True)
        except:
            continue

        # For the current season only, get player name, calculate averages and store them in dataframe
        if season == curSeason:
            playerName = players[2]
            meanStats = pd.DataFrame([[playerID, playerName] + gameDF[range(6, 25)].mean().tolist()])
            playerAvgDF=playerAvgDF.append(meanStats,ignore_index=True)

    # Split the vs column to indicate which team is home and which is away
    seasonDF['loc'] = seasonDF[4].apply(lambda x: 'HOME' if x[4] == 'v' else 'AWAY')
    seasonDF['opp'] = seasonDF[4].apply(lambda x: x[-3:])

    # Calculate Fantasy Points using dot product and scoring coefficients as given by Yahoo Fantasy
    fantasyCoeff = [1.2, 1.5, 3, 3, -1, 1]
    seasonDF['fp']= seasonDF[range(18,23)+[24]].dot(fantasyCoeff)
    # Performance improvement using log transformation, maybe... .apply(lambda x: np.log(float(x)) if x > 1 else 0)

    # Label columns and turn location (home or away) and opponent played into categorical/dummy variables
    seasonDF.columns = ['MATCH','MINS','REB','ASST','STL','BLK','TOV','PF','PTS','LOC','OPP','FP']
    loc = pd.get_dummies(seasonDF.LOC)
    opp = pd.get_dummies(seasonDF.OPP)

    # Create new DF using only information needed for model training data, save to csv and upload to S3
    modelData = pd.concat([seasonDF[['FP','MINS','TOV','PF']], loc, opp], axis=1)
    csvName = season+'Data.csv'
    modelData.to_csv(csvName, sep=',',index=False)
    s3.upload_file(csvName, bucket, "NEW/" + csvName)

# Label player average data frame, save to csv and upload to S3
csvName = 'PlayerAVG.csv'
playerAvgDF.columns = ['ID','NAME','MINS','FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','STL','BLK','TOV','PF','PTS']
playerAvgDF.to_csv(csvName, sep=',',index=False)
s3.upload_file(csvName, bucket, "NEW/" + csvName)
