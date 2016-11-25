#This script starts model and feature recalculation. The stored features and
#player models will be remade according to stored games in database.

import pokerbot.database
import pokerbot.opponent_modeller
import pokerbot.features as features
import pokerbot.learning as learning
import pokerbot.stats as stats

db = pokerbot.database.Database()
print("Setting last processed game ID to null...")
db.last_processed_game = pokerbot.database.NULL_ID #All games should be processed

print("Starting recalculation...")
opponent_modeller = pokerbot.opponent_modeller.OpponentModeller(features.functions, db, 1, learning, stats.functions)
opponent_modeller.process_games()
print("Done!")
