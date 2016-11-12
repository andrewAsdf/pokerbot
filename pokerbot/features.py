import deuces.card
import deuces.evaluator


def raise_count(game_state):
    return game_state.raise_count


def pot_odds(game_state):
    seat_index = game_state.table.current_seat
    called_chips = game_state.to_call - game_state.table[seat_index].chips_bet

    return called_chips / (game_state.pot + called_chips)


def position(game_state):
    active_players = list(game_state.table.activePlayersOrdered())

    current_seat = game_state.table.current_seat
    current_player = game_state.table[current_seat]

    player_number = active_players.index(current_player)
    players_count = len(active_players)

    return (players_count - player_number) / players_count


def bets_to_call(game_state):
    current_seat = game_state.table.current_seat
    betsize = game_state.current_bet_size

    return (game_state.to_call - game_state.table[current_seat].chips_bet) / betsize



def committed(game_state):
    current_seat = game_state.table.current_seat
    return game_state.table[current_seat].chips_bet > 0


def stage(game_state):
    return game_state.stage / 3


def board_wetness(game_state):
    """TODO"""
    return 0


functions = [raise_count, pot_odds, position, bets_to_call, committed, stage]


def get_features(game_state):
    return {f.__name__ : f(game_state) for f in functions}

    

