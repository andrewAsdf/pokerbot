import deuces.card
import deuces.evaluator


def raise_count(game_state):
    if (game_state.stage == 0):
        return (game_state.to_call / game_state.current_bet_size) - 1
    else:
        return game_state.to_call / game_state.current_bet_size


def pot_odds(game_state):
    table = game_state.table

    called_chips = game_state.to_call - table.current_seat.chips_bet

    return called_chips / (game_state.pot + called_chips)


def position(game_state):
    table = game_state.table

    active_players = list(table.active_players_ordered())

    player_number = active_players.index(table.current_seat)
    players_count = len(active_players)

    return (players_count - player_number) / players_count


def bets_to_call(game_state):
    table = game_state.table
    betsize = game_state.current_bet_size

    return (game_state.to_call - table.current_seat.chips_bet) / betsize


def committed(game_state):
    return game_state.table.current_seat.chips_bet > 0


def active_player_number(game_state):
    return len(list(game_state.table.active_players_ordered()))


def stage(game_state):
    return game_state.stage / 3


def board_wetness(game_state):
    """TODO"""
    return 0


functions = [raise_count, pot_odds, position, bets_to_call, committed,
             active_player_number, stage]


def get_features(game_state):
    return {f.__name__ : f(game_state) for f in functions}
