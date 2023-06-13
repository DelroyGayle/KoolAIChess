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


def append_to_output_stream(astring):
    """
    append string to Game.output_stream
    """
    Game.output_stream += astring

    # debugging TODO
    print("OS",Game.output_stream)


"""
************ CASTLING ************
There are two types:
King-side castling - where the White king goes two spaces to his right,
and on the other side of the board the Black king can go two spaces to his left.
Queen-side castling - similar in that the king moves two spaces but this time
the White king goes left and the Black king goes right.
https://www.chessable.com/blog/how-to-castle-in-chess/
"""

def is_piece_a_king(chess, row, column):
    """
    Is the piece on this square a King?
    Regardless of colour
"""
    return chess.piece_letter(from_file, from_rank) == constants.KING_LETTER


def record_if_king_or_rook_have_moved(chess, who_are_you, file, rank):
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

def handle_castling(who_are_you):
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

def record_pawn_that_advanced_by2(who_are_you, previous_file, previous_rank, current_file, current_rank):
    """
    Record a pawn if it has made its first initial two-square move
    """
    # TODO
    print("CAME IN RP> " + previous_file + " PFR " + previous_rank + " CFR " + current_file + " CC " + current_rank)
    print("WHO ", who_are_you, chess.value(previous_rank, previous_rank), chess.value(current_rank, current_rank))  # todo
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
        save_captured_pawn = chess.piece_value(Game.computer_pawn_2squares_advanced_file, Game.computer_pawn_2squares_advanced_rank)
        chess[save_captured_file + save_captured_rank] = None
    else:
        save_captured_rank = Game.player_pawn_2squares_advanced_rank
        save_captured_file = Game.player_pawn_2squares_advanced_file
        save_captured_pawn = chess.piece_value(Game.player_pawn_2squares_advanced_file, Game.player_pawn_2squares_advanced_rank)
        chess[save_captured_file + save_captured_rank] = None

    # fill square with pawn

    chess[to_file + to_rank] = piece.Pawn(constants.PAWN_VALUE, Game.who_are_you)

    # Erase square of 'from' pawn now vacated
    save_current_pawn = chess[from_file + from_rank]
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


    print("EPFIRST ? R> " + from_rank + "C" + from_file + "TO R " + to_row + "C " + to_column)
    print("COMP CR>", Game.computer_pawn_2squares_advanced_col, Game.computer_pawn_2squares_advanced_row)
    print("PLAY CR>", Game.player_pawn_2squares_advanced_col, Game.player_pawn_2squares_advanced_row)
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
            print("DEST ROW", the_rank)
            print("DEST COL", to_file) # todo
            save_rank = Game.computer_pawn_2squares_advanced_rank
            save_file = Game.computer_pawn_2squares_advanced_file

# Computer is Black
# Is there a white pawn (which advanced 2 squares) adjacent to the black pawn?
    elif (Game.opponent_who_are_you == constants.PLAYER
         and Game.player_pawn_2squares_advanced_file == to_column
         and Game.player_pawn_2squares_advanced_rank == str(int(to_rank - 1))):
            print("YES/OPP = PLAYER EP")
            print("X", from_file)
            print("Y", from_rank)
            print("PAWN/p", chess.piece_value(Game.player_pawn_2squares_advanced_file, Game.player_pawn_2squares_advanced_rank), constants.PAWN_VALUE * Game.who_are_you, Game.who_are_you, Game.opponent_who_are_you)
            the_rank = str(int(to_rank - 1))
            the_file = Game.player_pawn_2squares_advanced_file
            print("DEST ROW", the_row)
            print("DEST COL", to_column)
            save_row = Game.player_pawn_2squares_advanced_rank
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
    chess.display(output_attacking_move(chess, Game.who_are_you, from_file, from_rank, to_column, to_row))

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
    if chess.piece_value(save_col, save_row) != constants.PAWN_VALUE * Game.opponent_who_are_you:
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
