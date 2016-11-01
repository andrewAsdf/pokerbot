
def raise_count(game_state):
    return game_state.raise_count


def pot_odds(game_state):

    seat_index = game_state.table.current_seat

    called_chips = game_state.to_call - game_state.table[seat_index].chips_bet

    return called_chips / (game_state.pot + called_chips)
