"""Functions for deriving player statistics from games.
Public module variables:

    functions -- A list containing the stat functions.

"""

def _is_voluntary_play(action_type):
    return action_type in {'call', 'raise', 'bet'}


def _get_player_paying(game):
    seat_to_player = {p['seat_number'] : p['name'] for p in game['table']}

    played_this_round = {p['name'] : False for p in game['table']}

    for action in game['actions']:
        if _is_voluntary_play(action['type']):
            player_name = seat_to_player[action['seat']]
            played_this_round[player_name] = True

    return played_this_round


def vpip(games):
    """Calculate VPIP (voluntary put $ in pot). Assumes dict game data
    format.
    """
    player_pays = {}

    game_results = [_get_player_paying(game) for game in games]

    for result in game_results:
        for name, payed in result.items():
            if player_pays.get(name) is None:
                player_pays[name] = {'payed' : 0, 'total' : 0}

            player_pays[name]['total'] += 1
            if payed:
                player_pays[name]['payed'] += 1


    return {k : {'vpip' : v['payed'] / v['total']} for k, v in player_pays.items()}
    

functions = [vpip] #more stats could be added to this list
