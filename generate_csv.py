from riotwatcher import LolWatcher, ApiError
import pandas as pd
import time

start_time = time.time()

# GET DATA
API_KEY = 'RGAPI-d5e5d356-d3a2-41d4-a272-01deb5de86fd'
lol_watcher = LolWatcher(API_KEY)

# PARAMETERS
total_summoners = 200 # 205 by page
matchs_by_summoner = 10 # 100 by summoner

def add_to_csv(region, tier, division):
    print('obteniendo datos:')
    print(region+' '+ tier+ ' '+ division)
    print('')

    try:
        summoners = lol_watcher.league.entries(region,queue,tier,division, 1)
        summoners_cols = []
        summoners_count = 0
        for row in summoners:
            if(summoners_count >= total_summoners):
                break
            summoners_count += 1

            user_name = row['summonerName']

            try:
                user = lol_watcher.summoner.by_name(region, user_name)
                user_matches = lol_watcher.match.matchlist_by_account(region, user['accountId'])

                match_count = 0
                for match in user_matches['matches']:
                    if(match_count >= matchs_by_summoner):
                        break
                    match_count += 1

                    try:
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
                                        summoners_row['tierRank'] = row['tier'] + '-' + row['rank']
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
                                        # print(summoners_row)

                    except ApiError as err1:
                        print(err1)
                        pass

            except ApiError as err2:
                print(err2)
                pass 
        # ADD DATA TO A CSV:
        df = pd.DataFrame(summoners_cols)
        file_name = 'la2_rankIIIonly_extended.csv'
        # df.to_csv(file_name, encoding='utf-8', index=False) # to override
        df.to_csv(file_name,  mode='a',encoding='utf-8', index=False, header=False) # to add data
        print("--- %s seconds ---" % (time.time() - start_time))

    except ApiError as err3:
        print(err3)
        pass

    


# API OPTIONS
regions = ( 'la2','la1', 'na1','jp1', 'kr','br1', 'eun1', 'euw1', 'oc1', 'tr1', 'ru')
queue = 'RANKED_SOLO_5x5'
tiers = ('IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND')
divisions = ('I', 'II', 'III', 'IV')
region = regions[0]

# CSV HEADER
#gameId,region,summonerName,(tier,rank),,wins,losses,win,lane,role,championId,spell1Id,spell2Id,kills,deaths,assists,largestKillingSpree,largestMultiKill,killingSprees,longestTimeSpentLiving,doubleKills,tripleKills,quadraKills,pentaKills,totalDamageDealt,totalDamageDealtToChampions,totalHeal,totalUnitsHealed,damageDealtToObjectives,timeCCingOthers,totalDamageTaken,totalMinionsKilled,goldEarned,goldSpent,visionScore,team-firstBlood,team-firstTower,team-firstInhibitor,team-firstBaron,team-firstDragon,team-firstRiftHerald,team-towerKills,team-inhibitorKills,team-baronKills,team-dragonKills,team-vilemawKills,team-riftHeraldKills
#for tier in tiers:
    #for division in divisions:
add_to_csv(region, tiers[5], divisions[2])