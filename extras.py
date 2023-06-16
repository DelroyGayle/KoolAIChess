"""
extras.py
To assist in the modularising of this project
I have introduced this module to resolve any circular import issues

All miscellaneous routines relating to
the formatting, displaying and output of chess moves are placed here

Will place any other miscellaneous routines here
"""

import constants
from game import Game
import moves as m


def append_to_output_stream(astring):
    """
    append string to Game.output_stream
    """
    Game.output_stream += astring

    # debugging TODO
    print("OS", Game.output_stream, Game.output_chess_move)


def output_message(message):
    """
    Output a message after first removing any superfluous blank lines
    """
    lines = message.splitlines()

    # Based on
    # https://stackoverflow.com/questions/3845423/
    # remove-empty-strings-from-a-list-of-strings
    stripped = [line.strip() for line in lines if line.strip()]

    if not stripped:
        # Print a blank line
        print()
        return

    for m in range(len(stripped)):
        print(stripped[m])
        return


def input_status_message(message):
    """
    Print a message, that is, inform the user
    regarding the status of the contents of the input file
    Reset flag accordingly
    """
    output_message(message)
    print(f"There will be no further input from '{constants.INPUT_PGN_NAME}'")
    print()
    # Reset Flag
    Game.reading_game_file = False


def is_error_from_input_file():
    """
    Display a general message if an erroneous chess move
    came from the input file
    """
    if Game.reading_game_file:
        input_status_message(
                        "Since This Illegal Move came from the input file\n"
                        "moves will hereafter come "
                        "from your input via the keyboard")


def handle_castling_input(chess, input_string):
    """
    *** CASTLING ***
    Has user entered a Castling move from the keyboard?
    This is denoted by using capital 'O'
    that is O-O and O-O-O
    It is not PGN notation to use ZEROS
    However will cater for 0-0 and 0-0-0
    """

    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"
    input_string = input_string.upper()
    if not constants.castling_keyboard_pattern.match(input_string):
        # r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z"
        # No Castling move. Determine what this chess move is
        return do_next

    Game.general_string_result = input_string
    just_performed_castling = m.perform_castling(chess, constants.PLAYER)
    if not just_performed_castling:
        # This Castling move is invalid!
        # 'perform_castling() redisplays the Board
        # and displays the appropriate error messaging
        do_next = "continue"
        return do_next

    # The Castling move was valid!
    m.castling_move_is_valid(chess)
    do_next = "return"
    return do_next


def handle_player_move_from_keyboard(chess):
    """
    Validate the chess move entered by the Player
    """
    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"

    input_string = input("YOUR MOVE (e.g. e2e4): ").strip()

    if input_string == "R" or input_string == "r":
        chess.display("Player Resigned")
        # output_all_chess_moves(chess.COMPUTER_WON) todo
        goodbye()
        # Player Resigned
        # *** END PROGRAM ***

    # *** CASTLING ***
    # Check whether it is a Castling Move
    do_next = handle_castling_input(chess, input_string)
    if do_next != "pass":
        return (do_next, None)

    # General User Input Validation
    if input_string == "":
        chess.display("Null Input! Enter 'R' to Resign")
        do_next = "continue"
        return (do_next, None)

    lower_string = input_string.lower()
    if (len(lower_string) != 4
        #               Pattern: ([a-h][1-8]){2}
       or not constants.chess_move_pattern.match(lower_string)):
        chess.display("")
        print("I do not understand this input:", input_string)
        print("Format of Chess moves ought to be 4 characters e.g. e2e4")
        print("Files should be a letter from a to h")
        print("Ranks should be a number from 1 to 8")
        do_next = "continue"

    return (do_next, lower_string)
