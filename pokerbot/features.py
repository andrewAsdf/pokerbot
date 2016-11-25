"""Functions for deriving game features from game state.
Public module variables:

    functions -- A list containing the feature functions.

"""

from deuces.card import Card


def _get_board_card_rank(game_state, index):
    board = game_state.table.board
    card = board[index] if index < len(board) else None

    if card is not None:
        return (Card.get_rank_int(Card.new(card)) + 1) / 13
    else:
        return 0


def _get_board_cards(game_state):
    board = game_state.table.board
    return [Card.get_rank_int(Card.new(c)) + 1 for c in board]


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


def first_card_rank(game_state):
    return _get_board_card_rank(game_state, 0)


def second_card_rank(game_state):
    return _get_board_card_rank(game_state, 1)


def third_card_rank(game_state):
    return _get_board_card_rank(game_state, 2)


def fourth_card_rank(game_state):
    return _get_board_card_rank(game_state, 3)


def fifth_card_rank(game_state):
    return _get_board_card_rank(game_state, 4)


def ace_on_board(game_state):
    try:
        _get_board_cards(game_state).index(13)
        return True
    except ValueError:
        return False


def king_on_board(game_state):
    try:
        _get_board_cards(game_state).index(12)
        return True
    except ValueError:
        return False


def queen_on_board(game_state):
    try:
        _get_board_cards(game_state).index(11)
        return True
    except ValueError:
        return False


def board_wetness(game_state):
    """TODO"""
    return 0


functions = [raise_count, pot_odds, position, bets_to_call, committed,
            active_player_number, stage, ace_on_board, king_on_board,
            queen_on_board]
