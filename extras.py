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
from time import sleep
import fileio as f


class CustomException(Exception):
    """
    My custom exception class
    Just in case a Chess Logic Error that I had not anticipated happens!
    This definition is based on
    https://www.pythontutorial.net/python-oop/python-custom-exception/
    """
    pass


""" ROUTINES THAT GENERATE EACH OF THE PIECE'S MOVES """


def advance_vertical(rank, steps):
    """
    Calculate the new rank
    by adding 'steps' to the current 'rank'
    (8 at the top, 1 at the bottom)
    If the sum is not within the range 1 - 8
    then return None
    """

    newrank = chr(ord(rank) + steps)
    return newrank if "1" <= newrank <= "8" else None


def advance_horizontal(file, steps):
    """
    Calculate the new file
    by adding 'steps' to the current 'file'
    ('a' to the far left, 'h' to the far right)
    If the sum is not within the range a - h
    then return None
    """

    newfile = chr(ord(file) + steps)
    return newfile if "a" <= newfile <= "h" else None


def check_horizontally(chess, file_start, limit, step, rank,
                       moves_list, piece_sign):
    """
    Move either right to left OR left to right
    For each blank square append the square's coordinates
    When an opponent piece has been reached, append the square's coordinates
    and return the list
    When a piece of the same colour has been reached
    or the edge of the board has been reached,
    return the list
    """

    for m in range(file_start, limit, step):
        newfile = chr(m + constants.ASCII_A_MINUS1)  # 96
        square_sign = chess.piece_sign(newfile, rank)
        if piece_sign != square_sign:
            # Either an opponent piece or a blank square
            moves_list.append(newfile + rank)

        # Reached an occupied square - proceed no further
        if square_sign != constants.BLANK:
            return moves_list

    return moves_list


def check_vertically(chess, rank_start, limit, step,
                     file, moves_list, piece_sign):
    """
    Move either from top to bottom OR from bottom to top
    For each blank square append the square's coordinates
    When an opponent piece has been reached, append the square's coordinates
    and return the list
    When a piece of the same colour has been reached
    or the edge of the board has been reached,
    return the list
    """

    for m in range(rank_start, limit, step):
        newrank = chr(m + constants.ASCII_ZERO)  # 48
        square_sign = chess.piece_sign(file, newrank)
        if piece_sign != square_sign:
            # Either an opponent piece or a blank square
            moves_list.append(file + newrank)

        # Reached an occupied square - proceed no further
        if square_sign != constants.BLANK:
            return moves_list

    return moves_list


def horizontal_vertical(chess, file, rank, moves_list, piece_sign):
    """
    Record blank squares or an opponent's square
    whilst scanning both horizontally and vertically
    """

    # Convert 'file' i.e. 'a' to 'h' to a number between 1 to 8
    base_file_number = ord(file) - constants.ASCII_A_MINUS1  # 96

    # Move from the current piece's position,
    # towards the left until reaching a nonblank square
    # or the edge of the board
    moves_list = check_horizontally(chess, base_file_number - 1, 0, -1,
                                    rank, moves_list, piece_sign)

    # Move from the current piece's position,
    # towards the right until reaching a nonblank square
    # or the edge of the board
    moves_list = check_horizontally(chess, base_file_number + 1, 9, 1,
                                    rank, moves_list, piece_sign)

    # Convert 'rank' i.e. '1' to '8' to a number between 1 to 8
    base_rank_number = ord(rank) - constants.ASCII_ZERO  # 48

    # Move from the current piece's position,
    # towards the bottom until reaching a nonblank square
    # or the edge of the board
    moves_list = check_vertically(chess, base_rank_number - 1, 0, -1,
                                  file, moves_list, piece_sign)

    # Move from the current piece's position,
    # towards the top until reaching a nonblank square
    # or the edge of the board
    moves_list = check_vertically(chess, base_rank_number + 1, 9, 1,
                                  file, moves_list, piece_sign)

    return moves_list


def check_diagonally(chess, basefile, baserank,
                     horizontal, vertical, piece_sign):
    """
    Move diagonally by one square
    If the coordinates are off the board, return False
    If a piece of the same colour has been reached return False
    If the square is blank return the square's coordinates
    If an opponent piece has been reached return the square's coordinates
    """

    newfile = chr(basefile + horizontal)
    newrank = chr(baserank + vertical)
    if not (("a" <= newfile <= "h") and ("1" <= newrank <= "8")):
        return None

    square_sign = chess.piece_sign(newfile, newrank)
    if piece_sign == square_sign:
        # Same colour piece
        return None

    # Either an opponent piece or a blank square
    return newfile + newrank


def diagonal(chess, file, rank, moves_list, piece_sign):
    """
    Record blank squares or an opponent's square
    whilst scanning diagonally
    """

    # Convert 'file' i.e. 'a' to 'h' to its corresponding code
    base_file_number = ord(file)
    # Convert 'rank' i.e. '1' to '8' to its corresponding code
    base_rank_number = ord(rank)

    # Move from the current piece's position,
    # diagonally bottom-left until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  -m, -m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square
        moves_list.append(result)
        # Reached an occupied square - proceed no further
        if chess.piece_sign(result) != constants.BLANK:
            break

    # Move from the current piece's position,
    # diagonally bottom-right until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  -m, m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square
        moves_list.append(result)
        # Reached an occupied square - proceed no further
        if chess.piece_sign(result) != constants.BLANK:
            break

    # Move from the current piece's position,
    # diagonally top-left until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  m, -m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square
        moves_list.append(result)
        # Reached an occupied square - proceed no further
        if chess.piece_sign(result) != constants.BLANK:
            break

    # Move from the current piece's position,
    # diagonally top-right until reaching a nonblank square
    # or the edge of the board
    for m in range(1, 8):  # 1 to 7
        result = check_diagonally(chess, base_file_number, base_rank_number,
                                  m, m,
                                  piece_sign)
        if not result:
            # proceed no further
            break

        # Otherwise add the square
        moves_list.append(result)
        # Reached an occupied square - proceed no further
        if chess.piece_sign(result) != constants.BLANK:
            break

    return moves_list


def generate_moves_for_pawn(chess, file, rank,
                            moves_list, piece_sign):
    """
    Generate all the possible moves of the Pawn piece
    The legality of the moves are checked later
    """

    rank_plus1 = advance_vertical(rank, piece_sign)
    if not rank_plus1:
        # Reached the edge of the board
        return moves_list

    # Capture left?
    newfile = advance_horizontal(file, -1)
    # Is there an opponent piece present?
    if newfile and chess.piece_sign(newfile, rank_plus1) == -piece_sign:
        moves_list.append(newfile + rank_plus1)

    # Capture right?
    newfile = advance_horizontal(file, 1)
    # Is there an opponent piece present?
    if newfile and chess.piece_sign(newfile, rank_plus1) == -piece_sign:
        moves_list.append(newfile + rank_plus1)

    # one step forward
    # Is this square blank?
    if chess.piece_sign(file, rank_plus1) == constants.BLANK:
        moves_list.append(file + rank_plus1)

    # two steps forward
    if rank == "2" and piece_sign == constants.PLAYER:
        rank_plus2 = advance_vertical(rank, 2)
    elif rank == "7" and piece_sign == constants.COMPUTER:
        rank_plus2 = advance_vertical(rank, -2)
    else:
        rank_plus2 = False

    if rank_plus2:
        # Is this square blank?
        if chess.piece_sign(file, rank_plus2) == constants.BLANK:
            moves_list.append(file + rank_plus2)

    return moves_list


def generate_moves_for_rook(chess, file, rank,
                            moves_list, piece_sign):
    """
    Generate all the possible moves of the Rook piece
    The legality of the moves are checked later
    """
    return horizontal_vertical(chess, file, rank, moves_list, piece_sign)


def examine_this_square(diffs_tuple, chess, file, rank, piece_sign):
    """
    Check if it is possible for the piece to land on this square
    Calculate the square's coordinates using the numbers in 'diffs_tuple'
    """

    (file_diff, rank_diff) = diffs_tuple

    # Is it on the board?
    newfile = chr(ord(file) + file_diff)
    if not ("a" <= newfile <= "h"):
        return False

    newrank = chr(ord(rank) + rank_diff)
    if not ("1" <= newrank <= "8"):
        return False

    index = newfile + newrank
    square_sign = chess.piece_sign(newfile, newrank)

    # True: Either an opponent piece or a blank square
    # False: Otherwise same coloured piece
    return piece_sign != square_sign


def add_knight_king_square(diffs_tuple, file, rank):
    """
    Having determined that it is possible
    for a Knight piece or a King piece
    to land on a particular square
    Create the coordinates of this square using the numbers in 'diff_tuple'
    e.g. (1, 2) means file += 1, rank += 2.
    """

    (file_diff, rank_diff) = diffs_tuple
    newfile = chr(ord(file) + file_diff)
    newrank = chr(ord(rank) + rank_diff)
    return newfile + newrank


def generate_moves_for_knight(chess, file, rank,
                              moves_list, piece_sign):
    """
    Generate all the possible moves of the Knight piece
    The legality of the moves are checked later
    """

    knight_moves = [
        (-1, -2),  # down 1, left 2
        (-1, 2),   # down 1, right 2
        (-2, -1),  # down 2, left 1
        (-2, 1),   # down 2, right 1
        (1, -2),   # up 1, left 2
        (1, 2),    # up 1, right 2
        (2, -1),   # up 2, left 1
        (2, 1),    # up 2, right 1
    ]

    moves_list += [add_knight_king_square(diffs, file, rank)
                   for diffs in knight_moves
                   if examine_this_square(diffs, chess,
                                          file, rank, piece_sign)]

    return moves_list


def generate_moves_for_bishop(chess, file, rank,
                              moves_list, piece_sign):
    """
    Generate all the possible moves of the Bishop piece
    The legality of the moves are checked later
    """
    return diagonal(chess, file, rank, moves_list, piece_sign)


def generate_moves_for_queen(chess, file, rank,
                             moves_list, piece_sign):
    """
    Generate all the possible moves of the Queen piece
    The legality of the moves are checked later
    """
    moves_list = diagonal(chess, file, rank, moves_list, piece_sign)
    moves_list = horizontal_vertical(chess, file, rank, moves_list, piece_sign)
    return moves_list


def generate_moves_for_king(chess, file, rank,
                            moves_list, piece_sign):
    """
    Generate all the possible moves of the King piece
    The legality of the moves are checked later
    """

    king_moves = [
        (0, 1),     # up
        (0, -1),    # down
        (-1, 0),    # left
        (1, 0),     # right
        (-1, 1),    # diagonal up-left
        (1, 1),     # diagonal up-right
        (-1, -1),   # diagonal down-left
        (1, -1),    # diagonal down-right
    ]

    moves_list += [add_knight_king_square(diffs, file, rank)
                   for diffs in king_moves
                   if examine_this_square(diffs, chess,
                                          file, rank, piece_sign)]
    return moves_list


def determine_generate_move_method(piece_letter):
    """
    Use a dictionary to determine which method to call
    """

    methods_dictionary = {
        constants.PAWN_LETTER:      generate_moves_for_pawn,
        constants.ROOK_LETTER:      generate_moves_for_rook,
        constants.KNIGHT_LETTER:    generate_moves_for_knight,
        constants.BISHOP_LETTER:    generate_moves_for_bishop,
        constants.QUEEN_LETTER:     generate_moves_for_queen,
        constants.KING_LETTER:      generate_moves_for_king,
    }

    themethod = methods_dictionary.get(piece_letter, "Unknown letter: "
                                       + piece_letter)

    # Defensive Programming
    if isinstance(themethod, str):
        raise CustomException("Internal Error: " + themethod)

    return themethod


""" THE END OF PIECES' ROUTINES """


def movelist(chess, from_file, from_rank, piece_sign, evaluating=False):
    """
    Generate a list of possible moves for a particular piece
    """

    index = from_file + from_rank
    letter = chess.piece_letter(index)
    if not letter:
        return []  # blank square

    # Determine which function to call
    generate_moves_method = determine_generate_move_method(letter)
    all_the_moves = generate_moves_method(chess,
                                          from_file, from_rank,
                                          [],
                                          chess.board[index].sign)

    return all_the_moves


def append_to_output_stream(astring):
    """
    append string to Game.output_stream
    """
    Game.output_stream += astring


def goodbye():
    """
    End of Game Message
    """

    print()
    print("Thank You For Playing")
    print("Goodbye")
    quit()


def computer_resigns():
    """
    Computer has determined that its next course of action is to
    Resign! It cannot win!
    """

    print("Kool AI resigns!")
    append_to_output_stream(constants.PLAYER_WON)
    f.output_all_chess_moves()
    goodbye()
    # Computer Resigns
    # *** END PROGRAM ***


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

    # There is the need for a further delay here
    sleep(3)


def is_error_from_input_file():
    """
    Display a general message if an erroneous chess move
    had been read from the input file
    """
    if Game.reading_game_file:
        input_status_message(
                        "Since this Illegal Move came from the input file\n"
                        "moves will hereafter come "
                        "from your input via the keyboard")


def test_if_input_is_castling(chess, input_string):
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
    #      r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z"
    if not constants.castling_keyboard_pattern.match(input_string):
        # Not a Castling move. Determine what this chess move is
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
    m.castling_move_was_valid(chess)
    # Inform Player that Kool AI is thinking!
    print("I am evaluating my next move...")
    do_next = "return"
    return do_next


def handle_player_move_from_keyboard(chess):
    """
    Validate the chess move entered by the Player
    via the keyboard
    """
    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"

    input_string = input("YOUR MOVE (e.g. e2e4): ").strip()

    if input_string == "R" or input_string == "r":
        """
        If the Player Resigns at this point,
        a chess move has not yet been entered;
        the output stream may end with the move number.
        If so, remove the move number!
        """
        Game.output_stream = f.remove_the_suffix(Game.output_stream.rstrip(),
                                                 str(Game.move_count) + ".")
        chess.display("Player Resigned")
        if not Game.it_is_checkmate:
            # Since it was not Checkmate, Deem it a draw!
            if not Game.output_stream.endswith(constants.SPACE):
                Game.output_stream += constants.SPACE
            append_to_output_stream(constants.DRAW)
            f.output_all_chess_moves()

        goodbye()
        # Player Resigned
        # *** END PROGRAM ***

    # *** CASTLING ***
    # Check whether it is a Castling Move
    do_next = test_if_input_is_castling(chess, input_string)
    if do_next != "pass":
        return (do_next, None)

    # General User Input Validation
    if input_string == "":
        chess.display("Null Input! Enter r to Resign")
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
        print("\nEnter O-O for Queenside Castling; "
              "enter O-O-O for Kingside Castling")
        print("Enter r to Resign")
        do_next = "continue"

    return (do_next, lower_string)


def any_promotion(chess, to_file, to_rank):
    """
    Pawn Promotion:
    Promote Pawn Piece if it reaches the board edge
    This is done by adding the attributes
    'promote_letter' and 'promoted_value'
    using the 'promote' method
    """

    Game.promoted_piece = ""
    if to_rank not in ["1", "8"]:
        # Not the board edge
        return

    CHOICE_DICTIONARY = {
        constants.KNIGHT_LETTER: constants.KNIGHT_VALUE,
        constants.BISHOP_LETTER: constants.BISHOP_VALUE,
        constants.ROOK_LETTER: constants.ROOK_VALUE,
        constants.QUEEN_LETTER: constants.QUEEN_VALUE
    }

    CHOICE_LIST = [constants.ROOK_LETTER, constants.BISHOP_LETTER,
                   constants.KNIGHT_LETTER, constants.QUEEN_LETTER]

    to_square = to_file + to_rank
    if (to_rank == "1"
       and chess.piece_value(to_square) == -constants.PAWN_VALUE):

        # The Computer has reached the bottom of the board
        # Is the Piece an Unpromoted Pawn?

        if hasattr(chess.board[to_square], "promoted_value"):
            # No!
            return

        # Yes!
        # Promote the Black Pawn to a Black Queen
        chess.board[to_square].promote(constants.QUEEN_LETTER,
                                       constants.QUEEN_VALUE,
                                       constants.COMPUTER)
        # Record the Promotion in order to 'undo'
        # if function 'evaluate' has been called
        if Game.evaluating:
            Game.undo_stack[-1].add(to_square)
        else:
            # Set up a message regarding the promotion
            Game.promotion_message = "Pawn promoted to Queen"

        Game.promoted_piece = constants.QUEEN_LETTER
        return

    if (to_rank == "8"
       and chess.piece_value(to_square) == constants.PAWN_VALUE):

        # The Player has reached the top of the board
        # Is the Piece an Unpromoted Pawn?

        if hasattr(chess.board[to_square], "promoted_value"):
            # No!
            return

        # Yes!

        # Is Kool AI Evaluating White's Move?
        if Game.evaluating:
            # Promote the White Pawn to a White Queen
            chess.board[to_square].promote(constants.QUEEN_LETTER,
                                           constants.QUEEN_VALUE,
                                           constants.COMPUTER)
            # Record the Promotion in order to 'undo'
            # if function 'evaluate' has been called
            Game.undo_stack[-1].add(to_square)
            Game.promoted_piece = constants.QUEEN_LETTER
            return

        # Otherwise Promote the White Pawn to the Player's choice
        # First, redisplay board showing the Pawn at the top row/rank
        chess.display(Game.current_print_string)
        if Game.show_taken_message:
            # Show what piece the Player took
            print(Game.show_taken_message)

        print("What piece would you like to promote your Pawn to?")
        while True:
            print("Please enter either r for Rook, b for Bishop, n for Knight")
            choice = input("q or Enter for Queen. "
                           "Pick an answer [r/b/n/q/Enter] : ")
            choice = choice.strip().upper()
            if choice == "":
                choice = constants.QUEEN_LETTER
                break
            elif choice not in CHOICE_LIST:
                print("Not an appropriate choice.")
            else:
                print(Game.promotion_message)
                break

        # Promote the Pawn
        chess.board[to_square].promote(choice, CHOICE_DICTIONARY[choice],
                                       constants.PLAYER)
        # Record the Promotion in order to 'undo'
        # if function 'evaluate' has been called
        # Set up a message regarding the promotion
        Game.promotion_message = ("Pawn promoted to "
                                  + chess.board[to_square].piece_string())
        Game.promoted_piece = choice


def in_check(chess, user_sign):
    """
    To quote Rod Bird:
    this function [ scans ] all squares to see if any opposition piece
    has the King in Check
    """
    opponent_sign = -user_sign
    user_king_value = (constants.VALUE_OF_COMPUTER_KING
                       if user_sign == constants.COMPUTER
                       else constants.VALUE_OF_PLAYER_KING)

    # Go through each square on the board
    for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            index = letter + number
            if chess.piece_sign(index) == opponent_sign:
                all_the_moves = movelist(chess, letter, number,
                                         opponent_sign, False)
                # Start scanning each move
                for m in range(len(all_the_moves)):
                    if (chess.piece_letter(all_the_moves[m])
                       == constants.KING_LETTER
                       and chess.piece_value(all_the_moves[m])
                       == user_king_value):
                        # User King is in Check!
                        return True

    # Indicate that the Opponent King is not in Check at all
    return False


def make_move_to_square(chess, from_square, to_square, to_file, to_rank):
    """
    Fill the square with the chess piece
    """
    chess.board[to_square] = chess.board[from_square]

    # erase square vacated
    chess.board[from_square] = None
    # promote pawn if it reaches the board edge
    any_promotion(chess, to_file, to_rank)


def test_each_move(chess, who_are_you,
                   from_square,
                   to_square):
    """
    Go through each possible move
    To see if there is a chess move whereby the king
    is no longer 'in check'
    """

    # store From and To data so that it may be restored
    save_from_square = chess.board[from_square]
    save_to_square = chess.board[to_square]
    to_file = to_square[0]
    to_rank = to_square[1]

    # Make the move so that it can be tested for 'Check'
    make_move_to_square(chess,
                        from_square, to_square, to_file, to_rank)
    check_flag = in_check(chess, who_are_you)

    # Restore previous squares
    chess.board[from_square] = save_from_square
    chess.board[to_square] = save_to_square

    if not check_flag:
        # A suitable move has been found
        # Therefore, it is not Checkmate
        return True

    # Otherwise continue the loop i.e. continue testing
    return False


def is_it_checkmate(chess, who_are_you):
    """
    Determine whether the opponent is in Checkmate
    That is, the opponent's king is under attack,
    and there is no possible chess move available
    to save the king

    To determine whether Checkmate:
    This is done by going through each piece of the same colour as the King
    To see if there is any move generated which does not put the King in check
    If there is no such move then CHECKMATE!
    """

    # Filter all the squares containing the same colour
    same_colour_pieces_list = [index for index in constants.PRESET_CHESSBOARD
                               if chess.piece_sign(index) == who_are_you]

    # Go through each square and see if a piece can make a play
    # such that the king is no longer under threat
    for index in same_colour_pieces_list:
        from_file = index[0]
        from_rank = index[1]
        all_the_moves = movelist(chess, from_file, from_rank,
                                 who_are_you, False)

        # Loop through each possible move
        for m in range(len(all_the_moves)):
            exit_loop = test_each_move(chess, who_are_you,
                                       index, all_the_moves[m])

            if exit_loop:
                # Not Checkmate!
                return False

            # Otherwise continue testing
            continue

    # No move found so definitely Checkmate!
    Game.it_is_checkmate = who_are_you
    return True


def finalise_computer_move(chess, it_is_a_castling_move):
    """
    Now that the Computer's move has been performed
    Output the chess move to the output stream
    Determine whether the Computer's move has placed the Player in Check
    If so, determine to see if the Computer has won
    That is, is it Checkmate?

    If this is an En Passant move
    or if this is a Castling move
    there is no need to display the move
    This has already been done

    Game.en_passant_status != constants.VALID
    indicates a non-en-passant Chess Move
    """

    if (Game.en_passant_status != constants.VALID
       and not it_is_a_castling_move):
        # Display the Computer's move
        chess.display(Game.current_print_string)

        if Game.show_taken_message:
            # Show what piece the Computer took
            print(Game.show_taken_message)

        # Was there a Pawn Promotion? If so, Display a Message
        if Game.promotion_message:
            print(Game.promotion_message)
            Game.promotion_message = ""  # reset

        # If reading from a file
        # Pause the computer so that the Player can read the output
        if Game.reading_game_file:
            sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)

    # keep this flag unset from now on; so that the move count is incremented
    Game.move_count_incremented = False
    check_flag = in_check(chess, constants.PLAYER)
    if check_flag:
        print("You are in check")
        m.add_check_to_output()
        check_flag = is_it_checkmate(chess, constants.PLAYER)
        if check_flag:
            print("Checkmate!! I Win!")
            sleep(constants.SLEEP_VALUE)
            # Keep Linter happy - shorten name
            chess_move = Game.output_chess_move

            Game.output_chess_move = m.add_checkmate_to_output(chess_move)
            # Checkmate!
            append_to_output_stream(Game.output_chess_move + constants.SPACE
                                    + constants.COMPUTER_WON)
            f.output_all_chess_moves()
            # However do not end the program
            # Rather, the Player has to resign!
            print()
            return

    # Otherwise output the chess move to the output stream
    append_to_output_stream(Game.output_chess_move + constants.SPACE)
