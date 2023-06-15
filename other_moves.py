"""
other_moves.py
This module contains the routines related to
# Castling and En Passant

Also all other extra and miscellaneous routines relating to 
the formatting, displaying and output of chess moves are placed here
"""

import constants
from game import Game
from run import handle_internal_error, finalise_computer_move

def output_attacking_move(chess, who_are_you,
                          from_file, from_rank, to_file, to_rank):
    """
    Create a output message for the current chess move
    Showing who played what, the from square and the to square
    """

    strings_dict = {
        constants.KING_LETTER:   "King",
        constants.QUEEN_LETTER:  "Queen",
        constants.ROOK_LETTER:   "Rook",
        constants.BISHOP_LETTER: "Bishop",
        constants.KNIGHT_LETTER: "Knight",
        constants.PAWN_LETTER:   "Pawn"
    }
    dict_entry = strings_dict.get(chess.piece_letter(from_file, from_rank), "")
    print_string = (from_file + from_rank + "-" + to_file + to_rank
                    + " Piece: " + dict_entry)

    if who_are_you == constants.PLAYER:
        return "Checking Player move for " + print_string
    else:
        return "Computer moves " + print_string


# Reset previous values for the relevant colour
def reset_2squares_pawn_positions(who_are_you):
    if who_are_you == constants.PLAYER:
           Game.player_pawn_2squares_advanced_file = constants.NOVALUE
           Game.player_pawn_2squares_advanced_rank = constants.NOVALUE
    else:
           Game.computer_pawn_2squares_advanced_file = constants.NOVALUE
           Game.computer_pawn_2squares_advanced_rank = constants.NOVALUE


def convert_played_piece(letter, from_file, from_rank, to_file, to_rank):
    """
    Convert the piece into output format
    e.g. e2e4 for a pawn move
         Ng1f3 for a knight move
    """

    Game.output_chess_move = letter if letter != constants.PAWN_LETTER else ""
    Game.output_chess_move += from_file + from_rank + to_file + to_rank


def add_capture_promotion(taken):
    """
    If a piece has been taken indicate this
    by adding 'x' before the last two characters e.g. e5d5 ==> e5xd4
    If a Pawn has been promoted to, for example, a Queen; indicate this
    by adding =Q at the end of the Chess move e.g. f1xg1=Q
    """

    if taken:
        # add 'x' before the last two characters e.g. e5d5 ==> e5xd4
        length = len(Game.output_chess_move)
        suffix = Game.output_chess_move[-2:]
        Game.output_chess_move = (Game.output_chess_move[0:length - 2] + "x"
                                  + suffix)

    if Game.promoted_piece:
        # EG Add =Q at the end if a Pawn was promoted to a Queen e.g. fxg1=Q
        Game.output_chess_move += "=" + Game.promoted_piece


def add_check_to_output():
    """
    Indicate Check!
    """
    Game.output_chess_move += constants.CHECK_INDICATION


def add_checkmate_to_output(thestring):
    """
    Indicate Checkmate!
    Remove any trailing '+' OR SPACE first; then add # and SPACE afterwards
    """

    return (thestring.rstrip(constants.CHECK_INDICATION + constants.SPACE)
            + constants.CHECKMATE_INDICATION + constants.SPACE)


def setup_output_chess_move_add_promotion(letter, from_file, from_rank,
                                          to_file, to_rank, taken):
    """
    Convert the current chess move into an output format
    to show
    1) What piece has been played
    2) Does it do a capture?
    3) Is it a promoted pawn?
    """

    # Convert the chess move in order to output it
    convert_played_piece(letter, from_file, from_rank, to_file, to_rank)

    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # this is denoted as =Q e.g. f1xg1=Q
    add_capture_promotion(taken)


def any_promotion(chess, to_file, to_rank):
    """
    Pawn Promotion
    Promote Pawn Piece if it reaches the board edge
    """

    to_square = to_file + to_rank
    if (to_rank == "8"
       and chess.piece_value(to_square) == constants.PAWN_VALUE):

        # The Player has reached the top of the board
        # Promote the White Pawn to a White Queen
        chess.board[to_square].value = constants.QUEEN_VALUE
        chess.board[to_square].letter = constants.QUEEN_LETTER
        Game.promoted_piece = constants.QUEEN_LETTER

    elif (to_rank == to_rank == "1"
          and chess.piece_value(to_square) == -constants.PAWN_VALUE):
        # The Computer has reached the bottom of the board
        # Promote the Black Pawn to a Black Queen
        chess.board[to_square].value = -constants.QUEEN_VALUE
        chess.board[to_square].letter = constants.QUEEN_LETTER
        Game.promoted_piece = constants.QUEEN_LETTER

    else:
        Game.promoted_piece = ""


"""
************ CASTLING ************
There are two types:
King-side castling - where the White king goes two spaces to his right,
and on the other side of the board the Black king can go two spaces to his left.
Queen-side castling - similar in that the king moves two spaces but this time
the White king goes left and the Black king goes right.
https://www.chessable.com/blog/how-to-castle-in-chess/
"""

def is_piece_a_king(chess, file, rank):
    """
    Is the piece on this square a King?
    Regardless of colour
    """
    return chess.piece_letter(file, rank) == constants.KING_LETTER


def record_if_king_or_rook_has_moved(chess, who_are_you, previous_file, previous_rank, current_file, current_rank):
    """
    Record whether either a king or rook piece has been moved
    Once such a piece has been move, the Castling move is no longer an option
    Note: the rooks are set up as follows:
        Designate the kingside rooks
        self.board["h8"].kingside = True
        self.board["h1"].kingside = True

        Designate the queenside rooks
        self.board["a8"].queenside = True
        self.board["a1"].queenside = True
    """
    print("CAME IN R" + previous_rank + "C" + previous_file + "CR" + current_rank + "CC" + current_file)
    print("WHO", who_are_you, "KING?", chess.piece_value(current_file, current_rank), 
        "ROOK?", chess.piece_value(current_file, current_rank))
    # todo

    # Note: 'is_piece_a_king' does not regard the colour of the piece
    print("REC IF", Game.player_king_moved, is_piece_a_king(chess, current_file, current_rank)) # todo

    index = current_file + current_rank
    if who_are_you == constants.PLAYER:
        # The Player

        # Only check that the king has been moved if the flag has has not been set prior
        # Has the player's king been moved?
        # Note: 'is_piece_a_king' does not regard the colour of the piece
        Game.player_king_moved = (not Game.player_king_moved
                                  and is_piece_a_king(chess, current_file, current_rank))

        """
        Has a rook been moved?
        Only check if the relevant flag has not been set prior
        """
        Game.player_queen_rook_moved = (not Game.player_queen_rook_moved
                                       and hasattr(chess.board[index], "queenside"))
        Game.player_king_rook_moved = (not Game.player_king_rook_moved
                                       and hasattr(chess.board[index], "kingside"))

        print("PLAYER", Game.player_king_moved,
                    Game.player_queen_rook_moved, Game.player_king_rook_moved) # TODO
        return

    # The Computer

    # Only check that the king has been moved if the flag has has not been set prior
    # Has the computer's king been moved?
    # Note: 'is_piece_a_king' does not regard the colour of the piece
    Game.computer_king_moved = (not Game.computer_king_moved
                               and is_piece_a_king(chess, current_file, current_rank))

    """
    Has a rook been moved?
    Only check if the relevant flag has has not been set prior
    """
    Game.computer_queen_rook_moved = (not Game.computer_queen_rook_moved
                                     and hasattr(chess.board[index], "queenside"))
    Game.computer_king_rook_moved = (not Game.computer_king_rook_moved
                                    and hasattr(chess.board[index], "kingside"))

    print("COMPUTER", Game.computer_king_moved,
                    Game.computer_queen_rook_moved, Game.computer_king_rook_moved) # TODO


def does_value_match(chess, file, rank, number, test_value):
    """
    Used for the Castling tests
    Check that the value of square[file + number, rank] is equal to 'test_value'
    """
    new_file = chr(ord(file) + number)
    print("SO", file, rank, number, test_value, new_file)  # TODO
    # Defensive Programming
    if not ("a" <= new_file <= "h"):
        print(f"Castling Internal Error: File is Off-board {new_file} = {file} + {number}")
        handle_internal_error()
        # *** END PROGRAM ***

    return chess.piece_value(new_file, rank) == test_value


def produce_error_message(error_type):
    """
    Illegal Castling Move
    Display a message explaining why
    """

    if error_type == constants.ALREADY_CASTLED:
        Game.error_message = "Castling has already been done. Each side can only castle once in a game."
    elif error_type == constants.NO_KING_ROOK:
        Game.error_message = "Either the king or chosen rook is in the wrong position for Castling."
    elif error_type == constants.KING_MOVED:
        Game.error_message = "Castling not allowed because the king has already been moved."
    elif error_type == constants.ROOK_MOVED:
        Game.error_message = "Castling not allowed because the chosen rook has already been moved."
    elif error_type == constants.NOT_ALL_BLANK:
        Game.error_message = "There must be no pieces between the king and the chosen rook."
    elif error_type == constants.KING_IN_CHECK:
        Game.error_message = "Castling cannot be done whilst the king is in check."
    elif error_type == constants.THROUGH_CHECK:
        Game.error_message = "The king must not pass through a square that is under attack by opponent pieces."
    elif error_type == constants.END_UP_IN_CHECK:
        Game.error_message = "The king must not end up in check."


def castling_movement_done_already(who_are_you):
    """
    Castling:
    Test 2 of 6 - Has Castling already taken place?
    Test 3 of 6 - Has the king been moved already?
    """

    if who_are_you == constants.PLAYER:
        if Game.player_castled:
            produce_error_message(constants.ALREADY_CASTLED)
            return True
        elif Game.player_king_moved:
            produce_error_message(constants.KING_MOVED)
            return True
        else:
            return False

    # who_are_you == constants.COMPUTER

    if Game.computer_castled:
        produce_error_message(constants.ALREADY_CASTLED)
        return True
    elif Game.computer_king_moved:
        produce_error_message(constants.KING_MOVED)
        return True
    else:
        return False


def check_adjacent_squares(chess, who_are_you, which_castle_side, king_rook_rank):
    """
    Castling:
    Test 4 of 6 - Has the chosen rook been moved already?
    Test 5 of 6 - Is there an actual rook in the right position to be moved?
    Test 6 OF 6 - Are there any pieces between the king and the rook?
    """
    result = False

    print("which1", which_castle_side,
      abs(chess.piece_value(constants.KINGSIDE_ROOK_FILE, king_rook_rank)),
      constants.ROOK_VALUE)  # todo

    if which_castle_side == constants.KINGSIDE:
    # Test kingside rook

    # Has it been moved prior?
        if ((who_are_you == constants.PLAYER and Game.player_king_rook_moved)
           or (who_are_you == constants.COMPUTER and Game.computer_king_rook_moved)):
                produce_error_message(constants.ROOK_MOVED)

        # Is there an actual rook in the right position to be moved?
        # Note:  different coloured rooks have different values/signs i.e. -500 and 500
        #        hence constants.ROOK_VALUE * who_are_you
        elif chess.piece_value(constants.KINGSIDE_ROOK_FILE, king_rook_rank) != constants.ROOK_VALUE * who_are_you:
            produce_error_message(constants.NO_KING_ROOK)

        # No pieces can be between the king and the rook
        # So, the two adjacent squares between the rook and the king must be blank
        elif (not does_value_match(chess, constants.KINGSIDE_ROOK_FILE, king_rook_rank, -1, constants.BLANK)
             or not does_value_match(chess, constants.KINGSIDE_ROOK_FILE, king_rook_rank, -2, constants.BLANK)):
            produce_error_message(constants.NOT_ALL_BLANK)

        else: # Valid!

            result = True
        
        return result

# Test queenside rook

# Has it been moved prior?
    if ((who_are_you == constants.PLAYER and Game.player_queen_rook_moved) 
       or (who_are_you == constants.COMPUTER and Game.computer_queen_rook_moved)):
        produce_error_message(constants.ROOK_MOVED)

    # Is there an actual rook in the right position to be moved?
    # Note:  different coloured rooks have different values/signs i.e. -500 and 500
    #        hence constants.ROOK_VALUE * who_are_you
    elif chess.piece_value(constants.QUEENSIDE_ROOK_FILE, king_rook_rank) != constants.ROOK_VALUE * who_are_you:
        produce_error_message(constants.NO_KING_ROOK)

# No pieces can be between the king and the rook
# So, the three adjacent squares between the rook and the king must be blank
    elif (not does_value_match(chess, constants.QUEENSIDE_ROOK_FILE, king_rook_rank, 1, constants.BLANK)
        or not does_value_match(chess, constants.QUEENSIDE_ROOK_FILE, king_rook_rank, 2, constants.BLANK)
        or not does_value_match(chess, constants.QUEENSIDE_ROOK_FILE, king_rook_rank, 3, constants.BLANK)):
            produce_error_message(constants.NOT_ALL_BLANK)
    
    else: # Valid!

        result = True
        
    return result


def check_castling_valid_part1(chess, who_are_you, which_castle_side, king_rook_rank):
    """
    Castling:
    Test 1 of 6 - Is there an actual king in the right position to be moved?
    Test 2 of 6 - Has Castling already taken place?
    Test 3 of 6 - Has the king been moved already?
    Test 4 of 6 - Has the chosen rook been moved already?
    Test 5 of 6 - Is there an actual rook in the right position to be moved?
    Test 6 OF 6 - Are there any pieces between the king and the rook?
    """

    result = False

# A king OF THE CORRECT COLOUR must be present in file 'e' of its colour's rank in order to be castled

    print("which2", abs(chess.piece_value(constants.CASTLING_KING_FILE, king_rook_rank)), constants.KING_VALUE,
         constants.CASTLING_KING_FILE, chess.piece_value(constants.CASTLING_KING_FILE, king_rook_rank))  # TODO
    print(constants.CASTLING_KING_FILE, king_rook_rank, )  # todo
    print("regarding the king")
    print("ROOKrank", king_rook_rank, is_piece_a_king(chess, constants.CASTLING_KING_FILE, king_rook_rank, ), 
           "KING=", chess.piece_value(constants.CASTLING_KING_FILE, king_rook_rank))
    print("ROOKS", chess.piece_value(constants.KINGSIDE_ROOK_FILE, king_rook_rank), 
        chess.piece_value(constants.QUEENSIDE_ROOK_FILE, king_rook_rank))

    if chess.piece_value(constants.CASTLING_KING_FILE, king_rook_rank) < 0:
         king_sign = constants.COMPUTER  # -1
    else:
         king_sign = constants.PLAYER  #  1

    print("WHO?", king_sign, who_are_you)  # TODO
    # Note: 'is_piece_a_king' does not regard the colour of the piece

    if not (is_piece_a_king(chess, constants.CASTLING_KING_FILE, king_rook_rank) and king_sign == who_are_you):
        produce_error_message(constants.NO_KING_ROOK)
        print("RES3.1", Game.error_message)  # todo
        return
    elif castling_movement_done_already(who_are_you):
        print("RES3.2")  # todo
        return
    else:
        return check_adjacent_squares(chess, who_are_you, which_castle_side, king_rook_rank)
        print("RES3.3")  # todo


def calculate_new_file(file, number):
    """
    Used for the Castling movement
    New file = Current file value + number
    EG h8 + -1 = g8; a8 + 2 = c8
    Add the value of square[file + number, rank] is equal to 'test_value'
    """

    new_file = chr(ord(file) + number)
    # Defensive Programming
    if not ("a" <= new_file <= "h"):
        raise CustomException(f"Internal Error: File is Off-board {newfile} = {file} + {number}")

    return new_file


def move_king_one_square(chess, the_king, king_file, king_rank, king_direction):
    """
    Move the king by one square according to the value of 'king_direction'
    """

    new_king_file = calculate_new_file(king_file, king_direction)

    # fill square with king
    chess.board[new_king_file + king_rank] = the_king

    # erase square of king now vacated
    chess.board[king_file + king_rank] = None
    return new_king_file


def restore_original_positions(chess, the_king, the_rook,
                               the_king_square, the_rook_square,
                               king_rook_rank, direction):
    """
    After attempting a Castle move
    Restore the king and rook to their original positions
    """

    chess.board[the_king_square] = the_king
    chess.board[the_rook_square] = the_rook
    # Erase the other squares
    current_square = the_rook_square
    new_file = the_rook_square[0]
    while True:
        new_file = calculate_new_file(new_king_file, direction)
        new_square = new_file + king_rook_rank
        if new_square == the_king_square:
            return
        chess.board[new_square] = None


def check_castling_valid_part2(chess, who_are_you, which_castle_side, king_rook_rank, evaluating):
    """
    Castling: The following must be true for the Castling move to be valid
    The king is not currently in check;
    Your king must not pass through a square that is under attack by enemy pieces;
    The king must not end up in check.    
    """

# Check that the king is not currently in check
    if incheck(who_are_you):
       produce_error_message(constants.KING_IN_CHECK)
       return

    the_king_square = constants.CASTLING_KING_FILE + king_rook_rank
    the_king = chess.board[the_king_square]
    king_sign = who_are_you

    if which_castle_side == constants.KINGSIDE:
            king_direction = 1  # RIGHT
            rook_direction = -1  # LEFT
            the_rook_square = constants.KINGSIDE_ROOK_FILE + king_rook_rank
            the_rook_file = constants.KINGSIDE_ROOK_FILE
            the_rook = chess.board[the_rook_square]
    else:
            king_direction = -1  # LEFT
            rook_direction = 1  # RIGHT
            the_rook_square = constants.QUEENSIDE_ROOK_FILE + king_rook_rank
            the_rook_file = constants.QUEENSIDE_ROOK_FILE
            the_rook = chess.board[the_rook_square]

    new_king_file = constants.CASTLING_KING_FILE

# Move the King by one square
    new_king_file = move_king_one_square(chess, the_king, new_king_file, king_rook_rank, king_direction)

# The king must not pass through a square that is under attack by opponent pieces
    if incheck(who_are_you):
        produce_error_message(constants.THROUGH_CHECK)
        restore_original_positions(chess, the_king, the_rook, 
                                    the_king_square, the_rook_square, 
                                    king_rook_rank, -rook_direction)
        return


# Move the King again by one square
    new_king_file = move_king_one_square(chess, the_king, new_king_file, king_rook_rank, king_rook_rank, king_direction)

# The king must not pass through a square that is under attack by opponent pieces
    if incheck(who_are_you):
        produce_error_message(constants.THROUGH_CHECK)
        restore_original_positions(chess, the_king, the_rook, 
                                    the_king_square, the_rook_square, 
                                    king_rook_rank, -rook_direction)
        return

# Now move the Rook on to the other side of the King
    new_rook_file = calculate_new_file(new_king_file,rook_direction)

# fill square with rook
    chess.board[new_rook_file + king_rook_rank] = the_rook

# erase square of rook now vacated
    chess.board[rook_file + king_rook_rank] = None

# The king must not end up in check
    if incheck(who_are_you):
        produce_error_message(constants.END_UP_IN_CHECK)
        restore_original_positions(chess, the_king, the_rook, 
                                    the_king_square, the_rook_square, 
                                    king_rook_rank, -rook_direction)
        return


# This Castling move is valid
# If evaluating, restore regardless
    if EVALUATING:
        restore_original_positions(chess, the_king, the_rook, 
                                    the_king_square, the_rook_square, 
                                    king_rook_rank, -rook_direction)
        showboard()  # todo

    return True # Successful Castling move


def check_if_castling_move_is_valid(chess, who_are_you, which_castle_side, evaluating):
    """
    Castling:
    Test 1 of 6 - Is there an actual king in the right position to be moved?
    Test 2 of 6 - Has Castling already taken place?
    Test 3 of 6 - Has the king been moved already?
    Test 4 of 6 - Has the chosen rook been moved already?
    Test 5 of 6 - Is there an actual rook in the right position to be moved?
    Test 6 of 6 - Are there any pieces between the king and the rook?
    """

    Game.error_message = ""
    if who_are_you == constants.PLAYER:
        king_rook_rank = constants.PLAYER_SIDE_RANK  # White - Bottom row i.e. "1"
    else:
        king_rook_rank = constants.COMPUTER_SIDE_RANK  # Black - Top row  i.e. "8"

    if not check_castling_valid_part1(chess, who_are_you, which_castle_side, king_rook_rank):
        print("FS1 FALSE")  # TODO
        return False

    if not check_castling_valid_part2(chess, who_are_you, which_castle_side, king_rook_rank, evaluating):
        print("FS2 FALSE")  # TODO
        return False

    return True


# At this point, castling has been executed.
# A post-examination of the move has been done to ensure that the king in question is not in check
# Therefore it is a legal castling move - no need for any further checks
# Record that Castling has been executed once for either the player or the computer
# Redisplay the Board
# Display a message

def indicate_castling_done(chess, who_are_you, which_side_castled):
    if who_are_you == constants.PLAYER:
        Game.player_castled = True
        Game.player_king_moved = True
        if which_side_castled == constants.KINGSIDE:
            Game.player_king_rook_moved = True
            chess.display("Player Castled Kingside O-O")
        else:
            Game.player_queen_rook_moved = True
            chess.display("Player Castled Queenside O-O-O")

# PRINT ' Player-wise - the blank line is printed here ' todo
        return

# PRINT ' Computer-wise - the blank line is printed here ' todo
    Game.computer_castled = True
    Game.computer_king_moved = True
    if which_side_castled == constants.KINGSIDE:
        Game.computer_king_rook_moved = True
        chess.display("Computer Castled Kingside O-O")
    else:
        Game.computer_queen_rook_moved = True
        chess.display("Computer Castled Queenside O-O-O")


def perform_castling(chess, who_are_you):
    """
    This is the base routine to handle the Chess move of Castling
    CASTLING_KINGSIDE = "O-O"
    CASTLING_QUEENSIDE = "O-O-O"
    Ensure Game.general_string_result has Capital 'O' and not Zeros '0'

    Use a tuple for 'which_castle_side', 'special_move_validation' TODO
    """
    Game.general_string_result = Game.general_string_result.replace("0", "O")

    # Use Constants for O-O and O-O-O
    if Game.general_string_result == constants.CASTLING_KINGSIDE:
            # kingside' castling
            which_castle_side = constants.KINGSIDE
            output_castling_move = constants.CASTLING_KINGSIDE
            castling_message = ("Player Attempted Castling Kingside O-O"
                               if who_are_you == constants.PLAYER
                               else "Computer Attempted Castling Kingside O-O")
    
    else:  # queenside' castling
             which_castle_side = constants.QUEENSIDE
             output_castling_move = constants.CASTLING_QUEENSIDE
             castling_message = ("Player Attempted Castling Queenside O-O-O"
                                if who_are_you == constants.PLAYER
                                else "Computer Attempted Castling Queenside O-O-O")

    result = check_if_castling_move_is_valid(chess, who_are_you, which_castle_side, False)

    print("IS CASTLING VALID", result, castling_message, Game.error_message)  # TODO

    if not result:
        # This Castling move is invalid!
        # Redisplay the Board
        # Display the reason why the Castling Move is Invalid
        chess.display(castling_message)
        print("Illegal Castling Move")
        print(Game.error_message)
        Game.general_string_result = output_castling_move  # Need this
        return False

    # This Castling move is valid! - Indicate this
    indicate_castling_done(chess, who_are_you, which_castle_side)
    # Castling Move will be written to the output file
    Game.output_chess_move = output_castling_move
    return True


"""
************ EN PASSANT ************

En Passant Rule:
The attacking pawn must be one square into your opponent's half of the board.
So, if you are White, your pawn must be on the fifth rank,
and if you are Black, then your pawn must be on the fourth rank
https://www.chessable.com/blog/the-en-passant-rule-in-chess/

Note: the ranks are always ordered from White's perspective, so it is labelled White's fourth rank
Likewise for the fifth rank
"""

def record_pawn_that_advanced_by2(chess, who_are_you, previous_file, previous_rank, current_file, current_rank):
    """
    Record a pawn if it has made its first initial two-square move
    """
    # TODO
    print("CAME IN RP> " + previous_file + " PFR " + previous_rank + " CFR " + current_file + " CC " + current_rank)
    print("WHO ", who_are_you, chess.piece_value(previous_file, previous_rank), chess.piece_value(current_file, current_rank))  # todo
    if (who_are_you == constants.PLAYER
       and previous_rank == constants.PLAYER_PAWNS_RANK and current_rank == constants.FOURTH_RANK):
            print("YES/player") # todo
            player_pawn_2squares_advanced_file = current_file
            player_pawn_2squares_advanced_rank = current_rank

    elif (who_are_you == constants.COMPUTER
          and previous_rank == constants.COMPUTER_PAWNS_RANK and current_rank == constants.FIFTH_RANK):
            print("YES/computer") #todo
            computer_pawn_2squares_advanced_file = current_file
            computer_pawn_2squares_advanced_rank = current_rank
    
    else:
# Since this chess move is not a pawn that has advanced two squares
# Ensure that previous values for this colour have been reset
           reset_2squares_pawn_positions(who_are_you)


def validate_player_en_passant_move(from_file, from_rank, to_file, to_rank):
    """
    Validate the Player's en passant move
    That is the human opponent, not the Computer!
    """
    # todo DIM isit_an_en_passant_move

    # Ensure that these are set correctly
    Game.who_are_you = constants.PLAYER
    Game.opponent_who_are_you = constants.COMPUTER

    isit_an_en_passant_move = check_for_en_passant(from_file, from_rank, to_file, to_rank)
    if isit_an_en_passant_move:

    # Valid en passant move
    # todo
        # output_chess_move = convert_indices_to_file_rank(Game.resultant_source_x,
        #                                                  Game.resultant_source_y, 
        #                                                  Game.resultant_destination_x,
        #                                                  Game.resultant_destination_y)
        return True

    # Illegal En Passant Move
    # If no message has been printed, then print one
    if not g_message_printed:
        print("Illegal En Passant Move or Illegal Pawn Move")

    return False



def indicate_en_passant_done(who_are_you):
    """
    At this point, en passant has been executed.
    A post-examination of the move has been done to ensure that the king in question is not in Check
    Therefore it is a legal en passant move - no need for any further checks
    Reset variables holding opponent's advanced-by-2 pawn positions
    Display a message
    """
    
    if who_are_you == constants.PLAYER:
            print("Player Took Pawn En Passant")
            reset_2squares_pawn_positions(constants.COMPUTER)
    else:
            print("Computer Took Pawn En Passant")
            reset_2squares_pawn_positions(constants.PLAYER)

    print()


def perform_en_passant(chess, from_file, from_rank, to_file, to_rank):
    """
    Chess move has been determined which matches an en passant move
    Therefore, perform it
    """

    
    # Erase square of opponent pawn now vacated
    if Game.opponent_who_are_you == constants.COMPUTER:
        save_captured_file = Game.computer_pawn_2squares_advanced_file
        save_captured_rank = Game.computer_pawn_2squares_advanced_rank
        save_captured_pawn = chess.board[save_captured_file + save_captured_rank]
        chess.board[save_captured_file + save_captured_rank] = None
    else:
        save_captured_file = Game.player_pawn_2squares_advanced_file
        save_captured_rank = Game.player_pawn_2squares_advanced_rank
        save_captured_pawn = chess.board[save_captured_file + save_captured_rank]
        chess.board[save_captured_file + save_captured_rank] = None

    # fill square with pawn
    # TODO
    # save_from_pawn = chess[from_file + from_rank]

    chess[to_file + to_rank] = chess[from_file + from_rank]

    # Erase square of 'from' pawn now vacated
    chess[from_file + from_rank] = None

    # The king must not end up in check
    if incheck(Game.who_are_you):
        # If so, then this en passant is invalid
        # Redisplay the Board
        chess.display("Invalid en passant - The king must not end up in check")
        Game.message_printed = True
        Game.en_passant_status = constants.INVALID
        return False

    # Otherwise successful en passant - update values
    indicate_en_passant_done(Game.who_are_you)
    Game.new_from_file = from_file
    Game.new_from_rank = from_rank
    Game.new_to_file = to_file
    Game.new_to_rank = to_rank
    Game.en_passant_status = constants.VALID
    return True


def valid_and_perform_en_passant(chess, from_file, from_rank, to_file, to_rank):
    """
    If an en passant move is possible, perform it
    """

    if chess.piece_value(to_file, to_rank) != constants.BLANK:
    # destination square is occupied so cannot be an en passant move
        return False
        return


    print("EPFIRST ? R> " + from_rank + "C" + from_file + "TO R " + to_file + "C " + to_rank)
    print("COMP CR>", Game.computer_pawn_2squares_advanced_col, Game.computer_pawn_2squares_advanced_rank)
    print("PLAY CR>", Game.player_pawn_2squares_advanced_col, Game.player_pawn_2squares_advanced_rank)
    print("WHO/1", Game.opponent_who_are_you, chess.piece_value(to_file, to_rank))
    # todo

# Player is White
# Is there a black pawn (which advanced 2 squares) adjacent to the white pawn?
    if (Game.opponent_who_are_you == constants.COMPUTER
        and Game.computer_pawn_2squares_advanced_file == to_file
        and Game.computer_pawn_2squares_advanced_rank == str(int(to_rank + 1))):
            print("YES/ OPP = COMPUTER EP")
            print("X", from_file)
            print("Y", from_rank) # todo
            print("PAWN/c", chess.piece_value(Game.computer_pawn_2squares_advanced_file, Game.computer_pawn_2squares_advanced_rank), constants.PAWN_VALUE * Game.who_are_you, Game.who_are_you, Game.opponent_who_are_you)
            the_rank = str(int(to_rank + 1))
            the_file = Game.computer_pawn_2squares_advanced_file
            print("DEST FILE", the_file)
            print("DEST RANK", the_file) # todo
            save_rank = Game.computer_pawn_2squares_advanced_rank
            save_file = Game.computer_pawn_2squares_advanced_file

# Computer is Black
# Is there a white pawn (which advanced 2 squares) adjacent to the black pawn?
    elif (Game.opponent_who_are_you == constants.PLAYER
         and Game.player_pawn_2squares_advanced_file == to_file
         and Game.player_pawn_2squares_advanced_rank == str(int(to_rank - 1))):
            print("YES/OPP = PLAYER EP")
            print("X", from_file)
            print("Y", from_rank)
            print("PAWN/p", chess.piece_value(Game.player_pawn_2squares_advanced_file, Game.player_pawn_2squares_advanced_rank), constants.PAWN_VALUE * Game.who_are_you, Game.who_are_you, Game.opponent_who_are_you)
            the_rank = str(int(to_rank - 1))
            the_file = Game.player_pawn_2squares_advanced_file
            print("DEST FILE", the_file)
            print("DEST RANK", to_rank)
            save_rank = Game.player_pawn_2squares_advanced_rank
            save_col = Game.player_pawn_2squares_advanced_file

    else:
        # Destination Square does not match the opponent's 2-square pawn advanced coordinates - Therefore, definitely not an en passant move
        return False

    # Is the 'From' Rank known? That is, is the Rank of this piece known?
    if from_rank == constants.NOVALUE:
        # No! Therefore, the rank would be the same as the potential captured pawn's rank
        from_rank = save_rank

    # Is the attacking piece, a pawn?
    if chess.piece_letter(from_file, from_rank) != constants.PAWN_LETTER:
    # No! - Therefore, definitely not an en passant move
        return False

    # Redisplay the Board
    chess.display(output_attacking_move(chess, Game.who_are_you, from_file, from_rank, to_file, to_rank))

    # Defensive Programming
    # Add a failsafe just to double-check that
    # 1) The attacking piece is a pawn of the right colour
    if chess.piece_value(from_file, from_rank) != constants.PAWN_VALUE * Game.who_are_you:
        # Redisplay the Board
        output_error_message = "INTERNAL ERROR: Expected the Attacking Piece to be a Pawn\n"
        output_error_message += "of the right colour for the en passant move;\n"
        output_error_message += f"Instead, Value: {chess.piece_value(from_file, from_rank)}"
        if Game.reading_game_file:
            input_status_message(output_error_message)
        else:
            print(output_error_message)
            print()

        Game.en_passant_status = constants.INVALID
        Game.message_printed = True
        return False

    # 2) The captured piece is a pawn of the right colour
    # That is, is the 'attacked piece' an actual opponent pawn of the right colour?
    if chess.piece_value(save_col, save_rank) != constants.PAWN_VALUE * Game.opponent_who_are_you:
        # Redisplay the Board
        showboard()
        output_error_message = "INTERNAL ERROR: Expected the Captured Piece to be a Pawn\n"
        output_error_message += "of the right colour for the en passant move;\n"
        output_error_message += f"Instead, Value: {chess.piece_value(from_file, from_rank)}"
        if Game.reading_game_file:
            input_status_message(output_error_message)
        else:
            print(output_error_message)
            print()

        Game.en_passant_status = constants.INVALID
        Game.message_printed = True
        return False
 
# Otherwise perform the en passant
    return perform_en_passant(chess, from_file, from_rank, to_file, to_rank)

def handle_evaluated_castling_move(chess, computer_move_finalised):
    """
    If the 'evaluate' function generated a Castling Move then perform it
    """
    test = (Game.evaluate_castle_move != "" 
            and not Game.reading_game_file
            and not computer_move_finalised)
    if not test:
        return computer_move_finalised

    # The Evaluate Function generated a Castle Move! Perform it
    # Set up variables for Castling
    Game.move_type = constants.CASTLING_MOVE
    Game.general_string.result = do_castle_move
    Game.evaluate_castle_move = ""  # reset

    just_performed_castling = perform_castling(chess, constants.COMPUTER)
    if not just_performed_castling:
        # The Castling that was generated by 'The Evaluate Function' was invalid!
        # At this stage, this should not happen!
        # 'perform_castling() redisplays the Board and displays the appropriate error messaging
        # Therefore, End the Program
        print("INTERNAL ERROR OCCURRED - VALID CASTLE MOVE EXPECTED", Game.general_string.result)
        print(from_file, from_rank, to_file, to_rank)
        print()
        handle_internal_error()
        # *** END PROGRAM ***

    # Otherwise
    # The Castling that was generated by 'The Evaluate Function' was valid! 
    # As expected seeing that checks were done beforehand.
    # Castling Validation has already been done to see whether Castling would put the Player in Check
    # 'indicate_castling.done()' displays the appropriate messaging regarding the Castling

    # Since this chess move is not a pawn that has advanced two squares
    # Ensure that previous values for 'Computer' have been reset

    e.reset_2squares_pawn_positions(constants.COMPUTER)
    finalise_computer_move(chess)
    computer_move_finalised = True
    return computer_move_finalised

def handle_en_passant_from_inputfile(chess, from_file, from_rank, to_file, to_rank,
                                     print_string, attacking_piece_letter, taken):
    """
    For testing purposes I read Chess moves from an input file
    Therefore, if this option is ON
    Check whether an en passant has been done or attempted
    """

    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"
    # En Passant move attempted - turned out to be invalid
    if Game.en_passant_status == constants.INVALID:
        Game.en_passant_status = constants.NOVALUE  # reset flag
        Game.message_printed = False  # reset flag
        do_next = "continue"
        return do_next

    if Game.en_passant_status == constants.VALID:
        Game.en_passant_status = constants.NOVALUE  # reset flag
        Game.message_printed = False  # reset flag

        """
        The En Passant move that was read from the input file was valid!
        At this stage we know that no king nor rook has been moved;
        neither has any pawns been advanced two squares
        Nor can there be any promotions from this en passant move
        Convert the en passant move in order to output it
        Add a 'from_file' to the output chess move if a piece was taken
        Then output the piece to the output file
        """

        setup_output_chess_move_add_promotion(constants.PAWN_LETTER, 
                                              from_file, from_rank, to_file, to_rank,
                                              constants.PAWN_VALUE)
        finalise_player_move(from_file, from_rank, to_file, to_rank, just_performed_castling, attacking_piece, taken)
        do_next = "return"
        return do_next

    # Otherwise 'pass'
    return do_next

