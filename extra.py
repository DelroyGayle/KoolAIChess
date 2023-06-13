"""
extra.py
This module contains the routines related to
# Castling and En Passant

Also all other extra and miscellaneous routines relating to 
the formatting, displaying and output of chess moves are placed here
"""

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

# Note: This test does not regard the colour of the piece
def is_piece_a_king(chess, row, column)
"""
Is the piece on this square a King?
Ignore the colour
"""
    return chess.piece_letter(from_file, from_rank) == constants.KING_LETTER


def record_if_king_or_rook_have_moved(chess, who_are_you, file, rank)
    """
    Record whether either a king or rook piece has been moved
    Once such a piece has been move, the Castling move is no longer an option
    # Note: the rooks are set up as follows:
        Designate the kingside rooks
        self.board["h8"].kingside = True
        self.board["h1"].kingside = True

        Designate the queenside rooks
        self.board["a8"].queenside = True
        self.board["a1"].queenside = True
    """

    # Note: 'is_piece_a_king' does not regard the colour of the piece
    print("REC IF", Game.player_king_moved, is_piece_a_king(file, rank)) # todo

    index = file + rank
    if who_are_you == constants.PLAYER:
        # The Player

        # Only check that the king has been moved if the flag has has not been set prior
        # Has the player's king been moved?
        # Note: 'is_piece_a_king' does not regard the colour of the piece
        Game.player_king_moved = (not Game.player_king_moved
                                  and is_piece_a_king(file, rank))

        """
        Has a rook been moved?
        Only check if the relevant flag has has not been set prior
        """
        Game.player_queen_rook_moved = (not Game.player_queen_rook_moved
                                       and hasattr(chess.board[index], "queenside"))
        Game.player_king_rook_moved = (not Game.player_king_rook_moved
                                       and hasattr(chess.board[index], "kingside"))

        print("PLAYER", Game.player_king_moved,
                    Game.player_queen_rook_moved, Game.player_king_rook_moved) # TODO
        return

    # the Computer

    # Only check that the king has been moved if the flag has has not been set prior
    # Has the computer's king been moved?
    # Note: 'is_piece_a_king' does not regard the colour of the piece
    Game.computer_king_moved = (not Game.computer_king_moved
                             and is_piece_a_king(current_row, current_column))

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


# Use a tuple # todo
#   DIM which_castle_side AS INTEGER, who_are_you AS INTEGER, just_performed_castling AS BYTE
#   DIM output_castling_move AS STRING, castling_message AS STRING

def handle_castling(who_are_you)
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
             output_castling_move = CASTLING_QUEENSIDE
             castling_message = ("Player Attempted Castling Queenside O-O-O"
                                if who_are_you == constants.PLAYER
                                else "Computer Attempted Castling Queenside O-O-O")

    result = check_if_castling_move_is_valid(who_are_you, which_castle_side, False)

    print("IS CASTLING VALID", result, castling_message, g_error_message)  # TODO

    if not result:
        # This Castling move is invalid!
        # Redisplay the Board
        # Display the reason why the Castling Move is Invalid
        chess.display(castling_message)
        print("Illegal Castling Move")
        print(Game.error_message)
        Game.general_string_result = output_castling_move  # Need this
        time.sleep(constants.SLEEP_VALUE)  # Pause the Computer
        return False

    # This Castling move is valid! - Indicate this
    indicate_castling_done(which_castle_side, who_are_you)
    # Castling Move will be written to the output file
    Game.output_chess_move = output_castling_move
    return True


"""
************ EN PASSANT ************

En Passant Rule:
The attacking pawn must be one square into your opponent's half of the board.
So, if you are White, your pawn must be on the 5th rank,
and if you are Black, then your pawn must be on the 4th rank
https://www.chessable.com/blog/the-en-passant-rule-in-chess/

Note: the ranks are always ordered from White's perspective, so it is labelled White's fourth rank
Likewise for the fifth rank
"""

def record_pawn_that_advanced_by2(who_are_you, previous_file, previous_rank, current_file, current_rank)
    """
    Record a pawn if it has made its first initial two-square move
    """
    # TODO
    print("CAME IN RP> " + previous_file + " PFR " + previous_rank + " CFR " + current_file + " CC " + current_rank)
    print("WHO ", who_are_you, chess.value(previous_rank, previous_rank), chess.value(current_rank, current_rank))  # todo
    if (who_are_you == constants.PLAYER
       and previous_rank == constants.PLAYER_PAWNS_RANK and current_rank == constants.FOURTH_RANK):
        print("YES/player")
           player_pawn_2squares_advanced_file = current_file
           player_pawn_2squares_advanced_rank = current_rank

    elif (who_are_you == constants.COMPUTER
          and previous_rank == constants.COMPUTER_PAWNS_RANK and current_rank == constants.FIFTH_RANK):
            print("YES/computer")
            computer_pawn_2squares_advanced_file = current_file
            computer_pawn_2squares_advanced_rank = current_rank
    
    else:
# Since this chess move is not a pawn that has advanced two squares
# Ensure that previous values for this colour have been reset
           reset_2squares_pawn_positions(who_are_you)


def validate_player_en_passant_move(from_file, from_rank, to_file, to_rank)
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
