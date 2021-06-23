from riotwatcher import LolWatcher
import pandas as pd

# API OPTIONS
regions = ('br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru')
queue = 'RANKED_SOLO_5x5'
tiers = ('IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND')
divisions = ('I', 'II', 'III', 'IV')

# PARAMETERS
total_summoners = 2 # 205 by page
matchs_by_summoner = 2 # 100 by summoner
region = regions[6]
tier = tiers[4]
division = divisions[0]
page = 1

# GET DATA
API_KEY = 'RGAPI-172c38e7-4f3e-49d8-a49b-cbb4f31ed835'
lol_watcher = LolWatcher(API_KEY)
summoners = lol_watcher.league.entries(region,queue,tier,division, page)

summoners_cols = []
summoners_count = 0
for row in summoners:
    if(summoners_count >= total_summoners):
        break
    summoners_count += 1

    user_name = row['summonerName']
    user = lol_watcher.summoner.by_name(region, user_name)
    user_matches = lol_watcher.match.matchlist_by_account(region, user['accountId'])

    match_count = 0
    for match in user_matches['matches']:
        if(match_count >= matchs_by_summoner):
            break
        match_count += 1

        match_detail = lol_watcher.match.by_id(region, match['gameId'])

        summoners_row = {}
        for participant in match_detail["participantIdentities"]:
            if(user_name == participant["player"]['summonerName']):
                participant_id = participant["participantId"]

        for participant in match_detail['participants']:
            if(participant_id == participant['participantId']):
                team_id = participant['teamId']
                for team in match_detail['teams']:
                    if(team['teamId'] == team_id):

                        # game id
                        summoners_row['gameId'] = match_detail['gameId']

                        # summoner data
                        summoners_row['region'] = region
                        summoners_row['summonerName'] = row['summonerName']
                        summoners_row['tier'] = row['tier']
                        summoners_row['rank'] = row['rank']
                        summoners_row['wins'] = row['wins']
                        summoners_row['losses'] = row['losses']

                        # match summoner data
                        summoners_row['win'] = participant['stats']['win']
                        summoners_row['lane'] = participant['timeline']['lane']
                        summoners_row['role'] = participant['timeline']['role']
                        summoners_row['championId'] = participant['championId']
                        summoners_row['spell1Id'] = participant['spell1Id']
                        summoners_row['spell2Id'] = participant['spell2Id']

                        # match performance - KDA
                        summoners_row['kills'] = participant['stats']['kills']
                        summoners_row['deaths'] = participant['stats']['deaths']
                        summoners_row['assists'] = participant['stats']['assists']

                        # match performance - massacres
                        summoners_row['largestKillingSpree'] = participant['stats']['largestKillingSpree']
                        summoners_row['largestMultiKill'] = participant['stats']['largestMultiKill']
                        summoners_row['killingSprees'] = participant['stats']['killingSprees']
                        summoners_row['longestTimeSpentLiving'] = participant['stats']['longestTimeSpentLiving']
                        summoners_row['doubleKills'] = participant['stats']['doubleKills']
                        summoners_row['tripleKills'] = participant['stats']['tripleKills']
                        summoners_row['quadraKills'] = participant['stats']['quadraKills']
                        summoners_row['pentaKills'] = participant['stats']['pentaKills']

                        # match performance - performance?
                        summoners_row['totalDamageDealt'] = participant['stats']['totalDamageDealt']
                        summoners_row['totalDamageDealtToChampions'] = participant['stats']['totalDamageDealtToChampions']
                        summoners_row['totalHeal'] = participant['stats']['totalHeal']
                        summoners_row['totalUnitsHealed'] = participant['stats']['totalUnitsHealed']
                        summoners_row['damageDealtToObjectives'] = participant['stats']['damageDealtToObjectives']
                        summoners_row['timeCCingOthers'] = participant['stats']['timeCCingOthers']
                        summoners_row['totalDamageTaken'] = participant['stats']['totalDamageTaken']
                        summoners_row['totalMinionsKilled'] = participant['stats']['totalMinionsKilled']
                        summoners_row['goldEarned'] = participant['stats']['goldEarned']
                        summoners_row['goldSpent'] = participant['stats']['goldSpent']
                        summoners_row['visionScore'] = participant['stats']['visionScore']

                        # team info
                        summoners_row['team-firstBlood'] = team['firstBlood']
                        summoners_row['team-firstTower'] = team['firstTower']
                        summoners_row['team-firstInhibitor'] = team['firstInhibitor']
                        summoners_row['team-firstBaron'] = team['firstBaron']
                        summoners_row['team-firstDragon'] = team['firstDragon']
                        summoners_row['team-firstRiftHerald'] = team['firstRiftHerald']
                        summoners_row['team-towerKills'] = team['towerKills']
                        summoners_row['team-inhibitorKills'] = team['inhibitorKills']
                        summoners_row['team-baronKills'] = team['baronKills']
                        summoners_row['team-dragonKills'] = team['dragonKills']
                        summoners_row['team-vilemawKills'] = team['vilemawKills']
                        summoners_row['team-riftHeraldKills'] = team['riftHeraldKills']

                        # add row :3
                        summoners_cols.append(summoners_row)

df = pd.DataFrame(summoners_cols)
file_name = 'rifeco.csv'

# to override
df.to_csv(file_name, encoding='utf-8', index=False)

# to add data
# df.to_csv(file_name, , mode='a', header=False,encoding='utf-8', index=False)
