from riotwatcher import LolWatcher, ApiError
import pandas as pd

API_KEY = 'RGAPI-8451d9b1-4ee5-4a02-a8ae-da4dfee0aa7d'

my_region = 'la2'
regions = ('br1', 'eun1', 'euw1', 'jp1', 'kr', 'la1', 'la2', 'na1', 'oc1', 'tr1', 'ru')
queue = 'RANKED_SOLO_5x5'
tiers = ('IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND')
divisions = ('I', 'II', 'III', 'IV')

lol_watcher = LolWatcher(API_KEY)

summoners = lol_watcher.league.entries(my_region,queue,tiers[0],divisions[0], 1)
print(len(summoners))