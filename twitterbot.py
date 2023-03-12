# Import the necessary modules
from pymongo import MongoClient
import requests
import apikeys
import json
from bson import ObjectId


# Connect to the MongoDB database
client = MongoClient("mongodb://localhost:27017/")
db = client["alpros"]
collection = db["players"]

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
'''

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
            filter = {"accName": document["accName"]}
            update = {"$set": {"tier": tier, "wins": wins,
                               "losses": losses, "lp": leaguePoints, "rank": rank}}

            result = collection.update_many(filter, update)
'''
max = -100
best_player = ""
for document in collection.find():
    print(document["accName"])
    print(document["name"])
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


print("best player : "+best_player_name)
print("lp gained : "+str(max))
print("games played :"+str(best_player_wins+best_player_losses))
print("games won :"+str(best_player_wins))
print("games lost :"+str(best_player_losses))
print("twitter :"+best_player_twitter)


# accountId = response.json()["id"]
# filter = {"accName": document["accName"]}
# update = {"$set": {"acc_id": accountId}}
# result = collection.update_many(filter, update)


"""
for document in collection.find():
    response = requests.get(
    "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+document. +"?api_key=" + apikeys.riot_api)
    data = response.json()
"""
# print(data)
