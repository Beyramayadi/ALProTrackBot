# Import the necessary modules
from pymongo import MongoClient
import requests
import apikeys
import json
from bson import ObjectId
from datetime import date
import tweepy


import tweepy
import apikeys
# import all twitter keys/secrets

api_key = apikeys.api_key
api_key_secret = apikeys.api_key_secret
access_token = apikeys.access_token
access_token_secret = apikeys.access_token_secret
bearer_token = apikeys.bearer_token


# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["alpros"]
collection = db["players"]
collection2 = db["teams"]

"""
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

"""
"""
# Print all the documents in the collection
documents = list(collection.find())

# Convert the documents to JSON format using the custom encoder
json_data = json.dumps(documents, cls=CustomJSONEncoder)

# Print the JSON data to the console
print(json_data.name)
"""


def update_stats():
    for document in collection.find():
        print(document["accName"])
        response = requests.get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" +
                                document["acc_id"]+"?api_key=" + apikeys.riot_api)
        data = response.json()
        for item in data:
            if (item["queueType"] == "RANKED_SOLO_5x5"):

                print(item["tier"])
                tier = item["tier"]
                print(item["rank"])
                rank = item["rank"]
                print(item["leaguePoints"])
                leaguePoints = item["leaguePoints"]
                print(item["wins"])
                wins = item["wins"]
                print(item["losses"])
                losses = item["losses"]
                print(item["summonerName"])
                summonerName = item["summonerName"]
                filter = {"acc_id": document["acc_id"]}
                update = {"$set": {"tier": tier, "wins": wins,
                                   "losses": losses, "lp": leaguePoints, "rank": rank, "accName": summonerName}}

                result = collection.update_many(filter, update)


def get_best_player():
    max = -100
    best_player = ""
    for document in collection.find():
        print(document["accName"])
        print(document["name"])
        print(document["tier"])
        response = requests.get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" +
                                document["acc_id"]+"?api_key=" + apikeys.riot_api)
        data = response.json()
        for item in data:
            if (item["queueType"] == "RANKED_SOLO_5x5"):
                leaguePoints = item["leaguePoints"]
                oldLeaguePoints = document["lp"]
                print("new lp : "+str(leaguePoints))
                print("old lp : "+str(oldLeaguePoints))
                print(leaguePoints-oldLeaguePoints)
                if (leaguePoints-oldLeaguePoints > max):
                    max = leaguePoints-oldLeaguePoints
                    best_player = document["acc_id"]
                    best_player_name = document["name"]
                    best_player_wins = item["wins"] - document["wins"]
                    best_player_losses = item["losses"] - document["losses"]
                    best_player_twitter = document["twitter"]
                    best_player_team = document["team"]
                    best_player_country = document["country"]

    print("best player : "+best_player_name)
    print("lp gained : "+str(max))
    print("games played :"+str(best_player_wins+best_player_losses))
    print("games won :"+str(best_player_wins))
    print("games lost :"+str(best_player_losses))
    print("twitter :"+best_player_twitter)
    # today's day dd-mm-yyyy format
    day = date.today()
    tweet = "✅ Today's " + str(day) + " results ✅ \n The player who earned the most LP is " + best_player_team + " " + best_player_name + " "+best_player_country + " (" + best_player_twitter + ") with "+str(max)+" LP gained in "+str(
        best_player_wins+best_player_losses)+" games played ("+str(best_player_wins)+" wins and "+str(best_player_losses)+" losses). "
    return tweet

# calculate the total of lp for all players from the same team only for those who have a tier of master /grandmaster/challenger


def get_team_lp():

    for document in collection2.find():
        total_lp = 0
        print(document["name"])
        abbreviation = document["abbreviation"]
        for document2 in collection.find():
            if (document2["team"] == abbreviation):
                if (document2["tier"] == "MASTER" or document2["tier"] == "GRANDMASTER" or document2["tier"] == "CHALLENGER"):
                    total_lp += document2["lp"]
        print(total_lp)
        filter = {"abbreviation": abbreviation}
        update = {"$set": {"total_lp": total_lp}}
        result = collection2.update_many(filter, update)


def get_best_team():
    max = -100
    best_team = ""
    for document in collection2.find():
        abbreviation = document["abbreviation"]
        print(document["name"])
        total_lp = 0
        for document2 in collection.find():
            if (document2["team"] == abbreviation):
                response = requests.get("https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/" +
                                        document2["acc_id"]+"?api_key=" + apikeys.riot_api)
                data = response.json()
                for item in data:
                    if (item["queueType"] == "RANKED_SOLO_5x5"):
                        if (item["tier"] == "MASTER" or item["tier"] == "GRANDMASTER" or item["tier"] == "CHALLENGER"):
                            total_lp += item["leaguePoints"]
        difference = total_lp - document["total_lp"]
        print("difference : "+str(difference))
        if (difference > max):
            max = difference
            best_team = document["name"]
            best_team_abbreviation = document["abbreviation"]
            best_team_lp = total_lp
            best_team_twitter = document["twitter"]
    tweet2 = "And the team who got the most LP is "+best_team + \
        " ("+best_team_twitter+")" + "with "+str(max)+" LP gained"
    return tweet2


tweet = get_best_player()
# print(tweet)
# update_stats()
# get_team_lp()
tweet2 = get_best_team()
print(tweet+"\n" + tweet2)

# accountId = response.json()["id"]
# filter = {"accName": document["accName"]}
# update = {"$set": {"acc_id": accountId}}
# result = collection.update_many(filter, update)

# tweet
# Authenticate to Twitter


"""
for document in collection.find():
    response = requests.get(
    "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+document. +"?api_key=" + apikeys.riot_api)
    data = response.json()
"""
# print(data)
