"""

This Python Program is Based on
'How To Write A Chess Program in QBASIC By Dean Menezes.'

To quote Rod Bird who also adopted Menezes' program :-
    "Qudos to Mr Menezes for such a stunningly short and powerful Chess AI."

Menezes' QBASIC program can be found at
 http://www.petesqbsite.com/sections/express/issue23/Tut_QB_Chess.txt

"""

import constants
import piece
import os
import re


class CustomException(Exception):
    """
    my custom exception class
    Just in case a Chess Logic Error that I had not anticipated happens!
    This defintion is based on
    https://www.pythontutorial.net/python-oop/python-custom-exception/
    """


class Game:
    """
    A class that represents the status of the Chess Game
    This is the main workspace of the program
    It keeps track of the flags, properties and variables related
    to the state of play of the Game
    """

# Class Variables

    # the number of valid moves found for chosen piece
    num_moves = -1  # todo
    # recursion level for evaluate()
    level = 0  # todo
    # worth of play
    score = 0
    # todo check_flag
    # True means that one is currently in Check
    check_flag = False
    # Player (White) goes first
    player_first_move = True
    # White goes first
    whose_move = constants.PLAYER

    # Output purposes
    output_stream = ""
    output_chess_move = ""
    error_message = ""
    message_printed = False

    promoted_piece = ""
    player_castled = False
    computer_castled = False
    player_king_moved = False
    player_king_rook_moved = False
    player_queen_rook_moved = False
    computer_king_moved = False
    computer_king_rook_moved = False
    computer_queen_rook_moved = False
    player_pawn_2squares_advanced_col = None
    player_pawn_2squares_advanced_row = None
    computer_pawn_2squares_advanced_col = None
    computer_pawn_2squares_advanced_row = None
    en_passant_status = None
    selected_piece = None

    reading_game_file = None
    writing_game_file = False
    input_stream_previous_contents = ""
    skipped_seven_tag_rosters = False
    tag_pair_count = 0
    move_count = 0
    move_count_incremented = False

    def __init__(self):
        self.board = None
        self.fillboard()

    def fillboard(self):
        """
        The Chess Board as designed by Dean Menezes had the following values:

        -500,"R",-270,"N",-300,"B",-900,"Q",-7500,"K",-300,"B",-270,"N",-500,"R"
        -100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P",-100,"P"
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        0," ",0," ",0," ",0," ",0," ",0," ",0," ",0," "
        100,"P",100,"P",100,"P",100,"P",100,"P",100,"P",100,"P",100,"P"
        500,"R",270,"N",300,"B",900,"Q",5000,"K",300,"B",270,"N",500,"R"

        Black at the top has negative values
        You have: The value of each piece followed by its letter
        Zero and Space show the empty squares
        Then White at the bottom has positive values

        I chose not to use a 8X8 array with numerical indices
        for the following reason.

        In the Chess World,
        a chessboard consists of eight files and eight ranks.
        Columns are known as files and are labelled left to right with letters,
        a to h.
        Rows are known as ranks and are numbered from the bottom of the board
        upwards, 1 to 8.

        So a chessboard is depicted as
        a8, b8, c8, d8, e8, f8, g8, h8
        a7, b7, c7, d7, e7, f7, g7, h7
                    ...
                    ...
                    ...
                    ...
                    ...
                    ...
        a2, b2, c2, d2, e2, f2, g2, h2
        a1, b1, c1, d1, e1, f1, g1, h1

        Therefore rather than a 8X8 array with numerical indices;
        instead I chose to use a Python dictionary to reflect the above scheme.
        The keys being a string e.g. "h8" for the square h8
        Then each value would be a Piece Class instance
        of the form Piece(VALUE, LETTER, SIGN)

        Therefore the Dictionary would look like this
        {a8:value, b8:value, ..., d1:None, ..., e1:None, a1:value, ...,
         h1:value}

        Blank squares have the value None

        """
        self.board = dict(
                 # Black Rooks
                 a8=piece.Rook(constants.ROOK_VALUE, constants.COMPUTER),
                 h8=piece.Rook(constants.ROOK_VALUE, constants.COMPUTER),
                 # Black Knights
                 b8=piece.Knight(constants.KNIGHT_VALUE, constants.COMPUTER),
                 g8=piece.Knight(constants.KNIGHT_VALUE, constants.COMPUTER),
                 # Black Bishops
                 c8=piece.Bishop(constants.BISHOP_VALUE, constants.COMPUTER),
                 f8=piece.Bishop(constants.BISHOP_VALUE, constants.COMPUTER),
                 # Black Queen and King
                 d8=piece.Queen(constants.QUEEN_VALUE, constants.COMPUTER),
                 e8=piece.King(constants.KING_VALUE, constants.COMPUTER),
                 # White Rooks
                 a1=piece.Rook(constants.ROOK_VALUE, constants.PLAYER),
                 h1=piece.Rook(constants.ROOK_VALUE, constants.PLAYER),
                 # White Knights
                 b1=piece.Knight(constants.KNIGHT_VALUE, constants.PLAYER),
                 g1=piece.Knight(constants.KNIGHT_VALUE, constants.PLAYER),
                 # White Bishops
                 c1=piece.Bishop(constants.BISHOP_VALUE, constants.PLAYER),
                 f1=piece.Bishop(constants.BISHOP_VALUE, constants.PLAYER),
                 # White Queen and King
                 d1=piece.Queen(constants.QUEEN_VALUE, constants.PLAYER),
                 e1=piece.King(constants.KING_VALUE, constants.PLAYER))

        for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            # Black Pawns
            self.board[letter + "7"] = piece.Pawn(constants.PAWN_VALUE,
                                                  constants.COMPUTER)
            # White Pawns
            self.board[letter + "2"] = piece.Pawn(constants.PAWN_VALUE,
                                                  constants.PLAYER)
        # Blank Squares
        for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            for number in ["3", "4", "5", "6"]:
                self.board[letter + number] = None

        # Designate the kingside rooks
        self.board["h8"].kingside = True
        self.board["h1"].kingside = True

        # Designate the queenside rooks
        self.board["a8"].queenside = True
        self.board["a1"].queenside = True

    def piece_sign(self, index, rank=""):
        """
        Determine the sign of the value of the piece on the square
        Blank squares have a 'sign' of 0
        """

        if rank:
            index += rank

        return getattr(self.board[index], 'sign', constants.BLANK)

    def piece_value(self, index, rank=""):
        """
        Determine the numerical value of the piece on the square
        Blank squares are depicted as None
        """

        if rank:
            index += rank

        # space = " " todo
        return getattr(self.board[index], 'value', constants.BLANK)

    def piece_letter(self, index, rank=""):
        """
        Determine the letter of the piece on the square
        Blank squares are depicted as None
        """

        if rank:
            index += rank

        # space = " " todo
        return getattr(self.board[index], 'letter', None)

    def piece_output_string(self, index, rank=""):
        """
        Determine the letter of the piece on the square
        Blank squares are depicted as None
        """

        if rank:
            index += rank

        # space = " " todo
        print("Test")
        print(self.board[index].print_string())
        # return getattr(self.board[index], 'output_string', None)

    def showboard(self):
        """
        Display the Chessboard
        """

        space = " "
        left_bracket = " ["
        right_bracket = " ]"

        print()
        # 5 spaces THEN 2 spaces each
        print("{}A  B  C  D  E  F  G  H".format(space*5))

        # 3 spaces and 26 dashes "-"
        print("{}{}".format(space*3, "-"*26))

        for row in range(8, 0, -1):
            # SPACE NUMBER |
            output_string = "{}{} |".format(space, row)
            for column in range(8):
                position = (row + column) % 2
                portion1 = left_bracket[position]
                portion2 = right_bracket[position]
                letter = chr(97 + column)  # characters a to h
                number = row
                number = chr(48 + number)  # characters 1 to 8
                thesign = self.piece_sign(letter, number)
                if thesign == constants.BLANK:
                    output_string += portion1 + space + portion2
                elif thesign == constants.COMPUTER:
                    output_string += (portion1
                                      + self.piece_letter(letter, number)
                                      + portion2)
                else:
                    output_string += (portion1
                                      + self.piece_letter(letter, number)
                                      .lower()
                                      + portion2)

            print("{}|".format(output_string))

        # 3 spaces and 26 dashes "-"
        print("{}{}".format(space*3, "-"*26))
        # 5 spaces THEN 2 spaces each
        print("{}A  B  C  D  E  F  G  H".format(space*5))
        print()


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

    print("Kool A.I. resigns!")
    output_all_chess_moves(constants.PLAYER_WON)
    goodbye()
    # Computer Resigns
    # *** END PROGRAM ***


def handle_internal_error():
    """
    Hopefully this method is not necessary
    Added this just in case there is some kind of logic error that causes
    a chess logic problem e.g. a King piece being taken!
    If such a thing happens then abort this program with an error message
    """

    print("Computer resigns due to an internal error")
    print("Please investigate")
    # output_all_chess_moves(constants.PLAYER_WON) todo
    goodbye()
    # Internal Error
    # *** END PROGRAM ***


def show_taken(chess, to_file, to_rank, piece_sign):
    """
    Print a message showing which user took which piece
    Return the positive value of the piece taken
    In addition I added a test to check that the attacking/taking logic
    is correctly working
    If a 'King' is about to be taken, raise an error because such a move
    is illegal in Chess
    Note the Kings' values are:
        Computer's King (-7500) and Player's King (5000)
    """

    piece_taken = chess.piece_value(to_file, to_rank)

    # Return None for a Blank Square
    if not piece_taken:
        return None

    # Check whether a King is about to be actually taken!
    # Note the Kings' values: Computer's King (-7500) and Player's King (5000)
    if (piece_taken == constants.VALUE_OF_COMPUTER_KING or
            piece_taken == constants.VALUE_OF_PLAYER_KING):
        """
        This means the PLAYER/COMPUTER was allowed to make an illegal move
        i.e. KING cannot actually be taken
        One can attack a KING - Not take a King
        This should never happen!
        Some internal logic error has occurred
        """
        raise CustomException("Internal Error: King piece about to be taken:"
                              + str(piece_taken))

    # Convert to a positive number
    piece_taken = abs(piece_taken)

    if piece_sign < 0:
        print("Computer took your ", end="")
    else:
        print("Player took my ", end="")
    print(chess.print_string(to_file, to_rank))
    return piece_taken


def advance_vertical(rank, steps):
    """
    Calculate the new rank
    by adding 'steps' to the current 'rank'
    (8 at the top, 1 at the bottom)
    If the sum is not within the range 1 - 8
    then return None
    """

    newrank = chr(ord(rank) + steps)
    return newrank if '1' <= newrank <= '8' else None


def advance_horizontal(file, steps):
    """
    Calculate the new file
    by adding 'steps' to the current 'file'
    ('a' to the far left, 'h' to the far right)
    If the sum is not within the range a - h
    then return None
    """

    newfile = chr(ord(file) + steps)
    return newfile if 'a' <= newfile <= 'h' else None


def generate_moves_for_pawn(chess, who_are_you, file, rank, moves_list, piece_sign):
    """
    Generate all the legal moves of the pawn piece
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

    # one step forward?
    # Is this square blank?
    if chess.piece_sign(file, rank_plus1) == constants.BLANK:
        moves_list.append(file + rank_plus1)

    # two steps forward?
    rank_plus2 = (advance_vertical(rank, 2) if who_are_you == constants.PLAYER
                  else advance_vertical(rank, -2))

    if rank_plus2:
        # Is this square blank?
        if chess.piece_sign(file, rank_plus2) == constants.BLANK:
            moves_list.append(file + rank_plus2)

    return moves_list


def determine_generate_move_method(piece_letter):
    """
    Use a dictionary to determine which method to call
    """

    methods_dictionary = {
        constants.PAWN_LETTER: generate_moves_for_pawn,
    }
    themethod = methods_dictionary.get(piece_letter, "Unknown letter: "
                                       + piece_letter)

    if isinstance(themethod, str):
        raise CustomException("Internal Error: " + themethod)

    return themethod


def generate_moves(self, piece_sign):
    """
    Generate a list of valid moves for a particular piece
    """
    ...
    # todo


def movelist(chess, from_file, from_rank, piece_sign, evaluating=False):
    """
    get a list of possible moves for a particular piece
    """

    index = from_file + from_rank
    who_are_you = piece_sign
    letter = (chess.board[index]).letter
    if not letter:
        return []  # blank square

    generate_moves_method = determine_generate_move_method(letter)
    all_the_moves = generate_moves_method(chess, who_are_you, from_file, from_rank,
                                          [],
                                          chess.board[index].sign)
    num_moves = - 1  # todo
    return all_the_moves


"""
    if bpiece(x, y)
        elif == asc("P")
            pawn(x, y, piece_sign)
        elif == asc("N")
            knight(x, y, piece_sign)
        elif == asc("B")
            bishop(x, y, piece_sign)
        elif == asc("R")
            rook(x, y, piece_sign)
        elif == asc("Q")
            queen(x, y, piece_sign)
        elif == asc("K")
            king(x, y, piece_sign)
# Determine whether a Castling move is feasible
            if evaluating:
                  print("Castle", evaluating, level)  # todo
                  evaluate_castle(x, y, piece_sign)
todo
"""


def in_check(chess, user_sign):
    """
    To quote Rod Bird:
    this function scans all squares to see if any opposition piece
    has the King in Check
    """

    opponent_sign = 0 - user_sign

    # Go through each square on the board
    for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            index = letter + number
            if chess.piece_sign(index) == opponent_sign:
                all_the_moves = movelist(chess, letter, number, opponent_sign, False)
                # Start scanning each move
                for m in range(len(all_the_moves)):
                    if (chess.piece_letter(index) == constants.KING_LETTER):
                        # Opponent King is in Check!
                        return True

    # Indicate that the Opponent King is not in Check at all
                    return False


def is_player_move_legal(chess, from_file, from_rank, to_file, to_rank):

    """
    validate that the PLAYER'S move is legal
    That is: validate that the PLAYER'S move does not put the PLAYER in Check
    """

    piece_sign = constants.PLAYER  # white piece
    all_possible_moves = movelist(chess, from_file, from_rank, piece_sign, False)
    from_square = from_file + from_rank
    to_square = to_file + to_rank
    # Start scanning each move
    for m in range(len(all_possible_moves)):
        if all_possible_moves[m] == to_square:

            """
            Found the move that matches the Piece,
                  the From square and the To square

            Print a Message if a piece is about to be taken
            At the same time,
            Check whether the Computer's King is about to be literally taken
            If so, this indicates an Internal Logic Error
            """

            taken = show_taken(chess, to_file, to_rank, piece_sign)
            # No error raised - so the above test passed

            from_square = from_file + from_rank
            to_square = to_file + to_rank

            # store mover and target data so that it may be restored
            save_from_square = chess.board[from_square]
            save_to_square = chess.board[to_square]
            make_move_to_square(chess, from_square, to_square)

            # Does this PLAYER's move place the PLAYER in Check?
            # If so, illegal move!

            if in_check(chess, constants.PLAYER):
                # reset play and restore board pieces
                # check_flag todo
                print("You are in Check")
                chess.board[from_square] = save_from_square
                chess.board[to_square] = save_to_square
                # Indicate in Check
                return (True, taken)

            # Indicate not in check
            # check_flag todo
            return (False, taken)

    # Indicate that no legal move had been found
    return (False, None)


def output_attacking_move(chess, who_are_you, from_file, from_rank, to_file, to_rank):
    """
    Create a output message for the current chess move
    Showing who played what, the from square and the to square
    """
    print_strings_dict = {
        constants.KING_LETTER:   "King",
        constants.QUEEN_LETTER:  "Queen",
        constants.ROOK_LETTER:   "Rook",
        constants.BISHOP_LETTER: "Bishop",
        constants.KNIGHT_LETTER: "Knight",
        constants.PAWN_LETTER:   "Pawn"
    }
    print_string = (from_file + from_rank + "-" + to_file + to_rank
                    + " Piece: " + print_strings_dict[chess.piece_letter(from_file, from_rank)])

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
    If a piece had been taken indicate this
    by adding 'x' before the last two characters e.g. e5d5 ==> e5xd4
    If a Pawn had been promoted to, for example, a Queen; indicate this
    by adding =Q at the end of the Chess move e.g. f1xg1=Q
    """

    if taken:
        # add 'x' before the last two characters e.g. e5d5 ==> e5xd4
        length = len(output_chess_move)
        suffix = output_chess_move[-2:]
        Game.output_chess_move = (Game.output_chess_move[0:length - 2] + "x"
                                  + suffix)

    if Game.promoted_piece:
        # EG Add =Q at the end if a Pawn was promoted to a Queen e.g. fxg1=Q
        Game.output_chess_move += "=" + Game.promoted_piece


def setup_output_chess_move_add_promotion(letter, from_file, from_rank,
                                          to_file, to_rank, taken):
    """
    Convert the current chess move into an output format
    to show
    1) What piece has been played
    2) Does it do a capture
    3) Is it a promoted pawn?
    """

    # Convert the chess move in order to output it
    convert_played_piece(letter, from_file, from_rank, to_file, to_rank)

    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # this is denoted as =Q e.g. f1xg1=Q
    add_capture_promotion(taken)


def make_move_to_square(chess, from_square, to_square):
    """
    fill the square taken
    """
    
    chess.board[to_square] = chess.board[from_square]
    
# erase square vacated
    chess.board[from_square] = None
# promote pawn if it reaches board edge
    # any_promotion(x1, y1) todo


def execute_computer_move(chess, from_file, from_rank, to_file, to_rank):
    """
    Carry out the chess move that was produced
    by the 'evaluate' function
    """

    piece_sign = constants.COMPUTER  # black piece
    # display the move
    attacking_piece_letter = chess.piece_letter(from_file, from_rank)

    print_string = output_attacking_move(chess, constants.COMPUTER,
                                         from_file, from_rank,
                                         to_file, to_rank)

    # print() todo
    print(print_string)

    """
    Check whether a Player's piece is about to be taken
    Print a Message if this is true
    At the same time,
    Check whether the Player's King is about to be literally taken
    If so, this indicates an Internal Logic Error
    It would mean the COMPUTER's best move is an illegal move!
    'Kings' cannot actually be taken in Chess!
    """

    taken = None
    if piece_value(to_file, to_rank) > 0:
        taken = show_taken(chess, to_file, to_rank, piece_sign)
        # No error raised - so the above test passed

    from_square = from_file + from_rank
    to_square = to_file + to_rank
    make_move_to_square(chess, from_square, to_square)

# If the COMPUTER cannot play out of check then resign
    if in_check(chess, constants.COMPUTER):
        computer_resigns()

# todo
# Has the king been moved?
# Has a rook been moved
#       record_if_king_or_rook_have_moved(constants.COMPUTER, x, y, x1, y1)

# As the opponent advanced a pawn two squares?
#       If yes, record the pawn's position
#       record_pawn_that_advanced_by2(constants.COMPUTER, x, y, x1, y1)

# Convert the chess move in order to output it
# Add a 'x' to the output chess move if a piece was taken
# Add the promoted piece if a promotion took place
# Then output the piece to the output file
    setup_output_chess_move_add_promotion(attacking_piece_letter,
                                          from_file, from_rank,
                                          to_file, to_rank, taken)
    # return (attacking_piece, taken)  # todo


def finalise_computer_move(chess):
    """
    Now that the Computer's move has been performed
    Output the chess move to the output stream
    Determine whether the Player is in Check
    If so, determine to see if the Computer has won
    That is, is it Checkmate?
    """

    # check_flag todo

    check_flag = in_check(chess, constants.PLAYER)
    if check_flag:
        print("You are in check")
        add_check_to_output()
        check_flag = is_it_checkmate(constants.PLAYER)
        if check_flag:
            output_chess_move = add_checkmate_to_output(output_chess_move)
            print("Checkmate!! I Win!")
            print(output_chess_move)
            output_chess_move = add_checkmate_to_output(output_chess_move)

#            append_to_output(output_chess_move + constants.SPACE)
# keep this flag unset from now on; so that the move count is incremented
# g_move_count_incremented = False
# todo
            print()
            showboard()
            # todo Pause the Computer for 3 seconds


def process_computer_move(chess, from_file, from_rank, to_file, to_rank):
    """
    This routine handles the playing of the Computer's move
    """

    # todo
    # just_performed_castling = False
    computer_move_finalised = False

    if Game.player_first_move:
        # Player goes first so on the first iteration
        # there is no processing of Computer Moves
        Game.player_first_move = False
        return

    # From this point onwards, process the Computer's move

    # king on king end game?
    # Stalemate?
        if result < STALEMATE_THRESHOLD_SCORE:
            computer_resigns()

# Validate, Execute then Finalise the Computer Chess Move
# (if it was not a Castling Chess Move)
        if not computer_move_finalised:
            execute_computer_move(chess, from_file, from_rank, to_file, to_rank)
            # todo
            # finalise_computer_move
            # (check_flag, output_chess_move, g_move_count_incremented)
            finalise_computer_move(chess)


def finalise_player_move(chess, from_file, from_rank, to_file, to_rank,
                         attacking_piece_letter, taken):
    """
    Now that the Player's move has been performed
    Output the chess move to the output stream
    Determine whether the Computer is in Check
    If so, determine to see if the Player has won
    That is, is it Checkmate?
    """

    # TODO just_performed_castling, attacking_piece

    # TODO
    # Increment Move Number
    #        if not g_move_count_incremented:
    #            g_move_count+=1

    #        g_move_count_incremented = False
    # keep this flag unset from now on; so that the move count is incremented

    # Output the Move Number
    #     append_to_output(lstrip(str(g_move_count)) + "." + constants.SPACE)

    # Convert the chess move in order to output it
    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # Then output the piece to the output file
    setup_output_chess_move_add_promotion(attacking_piece_letter,
                                          from_file, from_rank,
                                          to_file, to_rank, taken)


# Now that the opponent has played, see if the computer is in Check
# check_flag todo

    check_flag = in_check(chess, constants.COMPUTER)
    if check_flag:
        print("I am in Check")
        add_check_to_output()
        check_flag = is_it_checkmate(constants.COMPUTER)
        if check_flag:
            output_chess_move = add_checkmate_to_output(output_chess_move)
            print("Checkmate!! You Win!")
#            append_to_output(output_chess_move + constants.SPACE)
#            output_all_chess_moves(constants.PLAYER_WON)
# todo
            print()
            goodbye()
            # Checkmate!
            # *** END PROGRAM ***

# Output the chess move
#   append_to_output(output_chess_move + constants.SPACE)
# todo

    print()


def player_move_validation_loop(chess, from_file, from_rank, to_file, to_rank):
    """
    Input Validation of the Player's Move
    Main Validation Loop
    """

    # todo                      (just_performed_castling,
    # todo                            attacking_piece_letter, taken)

    # print(just_performed_castling, attacking_piece_letter, taken) # todo
    while True:

        print()

        # fetch the next move from the player from keyboard
        input_string = input("YOUR MOVE (e.g. e2e4): ").strip()

        if input_string == "R" or input_string == "r":
            print("Player Resigned")
            # output_all_chess_moves(chess.COMPUTER_WON) todo
            goodbye()
            # Player Resigned
            # *** END PROGRAM ***

        """
        *** CASTLING ***
        This is denoted by using capital 'O
        that is O-O and O-O-O
        It is not PGN notation to use ZEROS
        However will cater for 0-0 and 0-0-0
        """

        if constants.castling_pattern.match(input_string):
            # \A((O-O-O)|(O-O)|(0-0-0)|(0-0))\Z"
            chess.general_string_result = input_string
            print("Castling Is Not Implemented")
            continue

        # General User Input Validation
        if input_string == "":
            print("Null Input! Enter 'R' to Resign")
            continue

        lower_string = input_string.lower()
        if (len(lower_string) != 4
            # Pattern: ([a-h][1-8]){2}
                or not constants.chess_move_pattern.match(lower_string)):
            os.system("clear")
            chess.showboard()
            print()
            print("I do not understand this input:", input_string)
            print("Format of Chess moves ought to be 4 characters e.g. e2e4")
            print("Files should be a letter from a to h")
            print("Ranks should be a number from 1 to 8")
            continue

        # Determine the file and rank of each board name
        # e.g. e2 ==> file 'e', rank '2'
        from_file = lower_string[0]
        from_rank = lower_string[1]
        to_file = lower_string[2]
        to_rank = lower_string[3]

        attacking_piece_letter = chess.piece_letter(from_file, from_rank)

        print_string = output_attacking_move(chess, constants.PLAYER,
                                             from_file, from_rank,
                                             to_file, to_rank)
        # print() todo
        print(print_string)

        piece_value = chess.piece_value(from_file, from_rank)

        if piece_value == constants.BLANK:  # BLANK SQUARE
            print("There is no piece to be played, instead a Blank Square")
            ...
            continue

        if piece_value < 0:  # negative numbers are the Computer's Pieces
            print("This is not your piece to move")
            ...
            continue

        (illegal, taken) = is_player_move_legal(chess,
                                                from_file, from_rank,
                                                to_file, to_rank)
        if illegal:
            print("Illegal move")
            ...
            continue

        # Has the king been moved?
        # Has a rook been moved
        # TODO record_if_king_or_rook_have_moved(constants.PLAYER,
        #       from_file, from_rank, to_file, to_rank)

        # As the opponent advanced a pawn two squares?
        # If yes, record the pawn's position
        # TODO record_pawn_that_advanced_by2(constants.PLAYER,
        #       from_file, from_rank, to_file, to_rank)

        # Increment the move count
        # Convert player's chess move for output
        # Output the chess move
        finalise_player_move(chess, from_file, from_rank, to_file, to_rank,
                             attacking_piece_letter, taken)
        # TODO just_performed_castling, attacking_piece_letter, taken)


def player_move(chess, from_file, from_rank, to_file, to_rank, result):
    """
    Firstly show the result of the Computer move
    Then get and validate the Player's move
    """

    # From this point onwards, process computer moves
    # todo
    (just_performed_castling, attacking_piece, taken) = (None, None, None)

    process_computer_move(chess, from_file, from_rank, to_file, to_rank)
    #  todo        just_performed_castling, attacking_piece_letter, taken)

    player_move_validation_loop(chess, from_file, from_rank, to_file, to_rank)

    """
    todo
                                just_performed_castling,
                                attacking_piece_letter,
                                taken
    """


def main_part2():
    """
    The main functionality of the Chess Program begins here

    Initialise the Game
    Display the Board
    """

    chess = Game()

    chess.fillboard()
    chess.showboard()

    from_file = None
    from_rank = None
    to_file = None
    to_rank = None
    result = 0  # TODO
    num = 0
    # Game Loop
    while True:
        player_move(chess, from_file, from_rank, to_file, to_rank, result)
        chess.showboard()
        num += 1  # todo testing
        if num > 3:
            break


def main():
    try:
        main_part2()
    except CustomException as error:
        print(error)
        handle_internal_error()
        quit()
    except Exception as error:
        raise error


if __name__ == "__main__":
    main()
