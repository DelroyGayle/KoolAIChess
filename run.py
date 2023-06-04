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


class Game:
    """
    A class that represents the status of the Chess Game
    This is the main workspace of the program
    It keeps track of the flags, properties and variables related
    to the state of play of the Game
    """

# Class Variables

    # the number of valid moves found for chosen piece
    num_moves = -1 # todo
    # recursion level for evaluate()
    level = 0 # todo
    # worth of play
    score = 0
    check_flag = False  # Therefore, True means that one is currently in check # todo
    player_first_move = True

    output_stream = ""
    output_chess_move = "" 
    error_message = ""
    message_printed = False

    whose_move = constants.PLAYER  # WHITE goes first
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

        In the Chess World,
        A chess board is depicted as eight ranks (rows) numbered
        from the bottom of the board 1 to 8
        Files are columns that are labelled left to right with numbers
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

        Therefore I chose to use a dictionary to reflect the above scheme
        The keys being a string e.g. 'h8' for the square h8
        Then each value would be a Piece Class instance variable
        of the form (PIECE VALUE, LETTER, SIGN)
        Therefore the Dictionary would look like this
        {a8:value, b8:value, ... a1:value, ... h1:value}
        Blank squares will have the value None

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


    def board_sign(self, index, rank=""):
        """
        Determine the sign of the value of the piece on the square
        Blank squares have a 'sign' of 0
        """
        if rank:
            index += rank
            
        return getattr(self.board[index], 'sign', 0)


    def board_piece(self, index, rank=""):
        """
        Determine the letter of the piece on the square
        Blank squares are depicted as None
        """
        if rank:
            index += rank

        # space = " " todo
        return getattr(self.board[index], 'piece', None)


    def board_value(self, index, rank=""):
        """
        Determine the numerical value of the piece on the square
        Blank squares are depicted as None
        """
        if rank:
            index += rank

        # space = " " todo
        return getattr(self.board[index], 'value', None)


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
                thesign = self.board_sign(letter, number)
                if thesign == constants.BLANK:
                    output_string += portion1 + space + portion2
                elif thesign == constants.COMPUTER:
                    output_string += (portion1
                                      + self.board_piece(letter, number)
                                      + portion2)
                else:
                    output_string += (portion1
                                      + self.board_piece(letter, number)
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


def handle_internal_error():
    """
    Hopefully this is not necessary
    Added this just in case I have some kind of logic error that causes
    a chess logic problem e..g a king piece being taken!
    If such a thing happens then abort this program with an error message
    """

    print("Computer resigns due to an internal error")
    print("Please investigate")
    # output_all_chess_moves(constants.PLAYER_WON) todo
    goodbye()
    # Internal Error
    # *** END ***


def show_taken(to_file, to_rank, piece_sign):
    """
    Print a message showing which user took which piece
    Return the positive value of the piece taken
    In addition I add a test to check that the attacking/taking logic is correctly working
    If a 'King' is about to be taken raise an error as such a move is illegal in Chess
    # Note the Kings' values are: Computer's King (-7500) and Player's King (5000)
    """

    values_dict = {
        constants.QUEEN_VALUE:  "Queen",
        constants.ROOK_VALUE:   "Rook",
        constants.BISHOP_VALUE: "Bishop",
        constants.KNIGHT_VALUE: "Knight",
        constants.PAWN_VALUE:   "Pawn"
    }

    piece_taken = chess.board_value(to_file, to_rank)

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
        raise Exception("Internal Error: King piece about to be taken:" + str(piece_taken))

    # Convert to a positive number
    piece_taken = abs(piece_taken)

    if piece_sign < 0:
        print("Computer took your ", end = "")
    else:
        print("Player took my ", end = "")
    print(values_dict[piece_taken])
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
    return newrank if '1' <= rank <= '8' else None


def advance_horizontal(file, steps):
    """
    Calculate the new file
    by adding 'steps' to the current 'file'
    ('a' to the far left, 'h' to the far right)
    If the sum is not within the range a - h 
    then return None
    """
    newfile = chr(ord(file) + steps)
    return newfile if 'a' <= file <= 'h' else None


def generate_moves_for_pawn(who_are_you, file, rank, moves_list, piece_sign):
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
    if newfile and chess.board_sign(newfile, rank_plus1) == -piece_sign:
        moves_list.append(newfile + rank_plus1)

    # Capture right?
    newfile = advance_horizontal(file, 1)
        # Is there an opponent piece present?
    if newfile and chess.board_sign(newfile, rank_plus1) == -piece_sign:
        moves_list.append(newfile + rank_plus1)

    # one step forward?
    # Is this square blank?
    if chess.board_sign(file, rank_plus1) == constants.BLANK:
        moves_list.append(file + rank_plus1) 

    # two steps forward?
    rank_plus2 = (advance_vertical(rank, 2) if who_are_you == constants.Player
                                            else advance_vertical(rank, -2))
    if rank_plus2:
    # Is this square blank?
        if chess.board_sign(file, rank_plus2) == constants.BLANK:
            moves_list.append(file + rank_plus2) 

    return moves_list


def determine_generate_move_method(piece_letter):
    """
    Use a dictionary to determine which method to call
    """
    methods_dictionary = {  
        PAWN_LETTER: generate_moves_for_pawn,
    }
    themethod = methods_dictionary.get(piece_letter, "Unknown letter " + piece_letter)

    if isinstance(themethod, str):
        raise Exception("Internal Error: " + themethod)

    return themethod


def generate_moves(self, piece_sign):
    """
    Generate a list of valid moves for a particular piece
    """
    ...
    # todo    

def movelist(from_file, from_rank, piece_sign, evaluating= False):
    """
    get a list of valid moves for a particular piece
    """
    who_are_you = piece_sign
    piece = board_piece(chess.board[from_file + from_rank])
    if not piece:
        return []  # blank square

    generate_moves_method = determine_generate_move_method(piece)
    all_the_moves = generate_moves_method(who_are_you, from_file, from_rank,
                                          [],board_sign(chess.board[from_file + from_rank]))
    num_moves = - 1 # todo
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

# To quote Rod Bird:
# this function checks all squares to see if any opposition piece has the king in check

def in_check(user_sign):
    opponent_sign = 0 - user_sign

    # Go through each square on the board
    for letter in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            if chess.board_sign(letter + number) == opponent_sign:
                all_the_moves = movelist(letter, number, opponent_sign, False)
                # Start scanning each move
                for m in range(len(all_legal_moves)):
                    if chess.board_piece(letter + number) == constants.KING_LETTER:
                        # Opponent King is in check!
                        return True

    # Indicate that the Opponent King is currently not in check at all
                    return False


def is_player_move_legal(from_file, from_rank, to_file, to_rank):

    """
    validate that the PLAYER'S move is legal
    That is: it does not put the PLAYER in check
    """

    piece_sign = constants.PLAYER  # white piece
    all_legal_moves = movelist(from_file, from_rank, piece_sign, False)
    to_square = to_file + to_rank
    from_square = from_file + from_rank
    # Start scanning each move
    for m in range(len(all_legal_moves)):
        if all_legal_moves[m] == to_square:
            # Found the move that matches the Piece, the From square and the To square
            # Print a Message if a piece is about to be taken
            # At the same time, Check whether the Computer's King is about to be literally taken
            # This indicates an Internal Logic Error
            taken = show_taken(to_file, to_rank, piece_sign)
            # No error raised - so the above test passed

            from_square = from_file + from_rank
            to_square = to_file + to_rank

            # store mover and target data so that it may be restored
            save_from_square = chess.board[from_square]
            save_to_square = chess.board[to_square]
            make_move_to_square(from_square, to_square)

            # Does this PLAYER's move place the PLAYER in check?
            # If so, illegal move!
            if in_check(constants.PLAYER):
            # reset play and restore board pieces
                print("You are in check")
                chess.board[from_square] = save_from_square
                chess.board[to_square] = save_to_square
                # Indicate in Check
                return (True, taken)

            # Indicate not in check
            return (False, taken)

    
    # Indicate that no legal move had been found
    return (False, None)


def output_attacking_move(who_are_you, from_file, from_rank, to_file, to_rank):

    print_string = from_file + from_file + "-" + to_file + to_rank + " Piece: " + board_piece(from_file, from_rank)

    if who_are_you == constants.PLAYER:
          return "Checking Player move for " + print_string
    else:
          return "Computer moves " + print_string


def convert_played_piece(piece, from_file, from_rank, to_file, to_rank):
    """
    Convert the piece into output format
    e.g. e2e4 for a pawn move
         Ng1f3 for a knight move
    """

    chess.output_chess_move = piece if piece != constants.PAWN_LETTER else ""
    chess.output_chess_move += from_file + from_rank + to_file + to_rank


def add_capture_promotion(taken):

    """
    If a piece had been taken indicate this 
    by adding 'x' before the last two characters e.g. e5d5 ==> e5xd4
    If a Pawn had been promoted to for example, a Queen; indicate this
    by adding =Q at the end of the Chess move e.g. f1xg1=Q
    """
    if taken:
# add 'x' before the last two characters e.g. e5d5 ==> e5xd4
        length = len(output_chess_move)
        suffix = output_chess_move[-2:]
        chess.output_chess_move = coutput_chess_move[0:length - 2] + "x" + suffix


    if chess.promoted_piece:
# EG Add =Q at the end if a Pawn was promoted to a Queen e.g. fxg1=Q
          chess.output_chess_move += "=" + chess.promoted_piece


def setup_output_chess_move_add_promotion(piece, from_file, from_rank, to_file, to_rank, taken):

# Convert the chess move in order to output it
    convert_played_piece(piece, from_file, from_rank, to_file, to_rank)

# Add a 'x' to the output chess move if a piece was taken
# Add the promoted piece if a promotion took place - this is denoted as =Q e.g. f1xg1=Q
    add_capture_promotion(taken)

def finalise_player_move(from_file, from_rank, to_file, to_rank, taken):
    # TODO just_performed_castling, attacking_piece

# TODO
# Increment Move Number
#        if not g_move_count_incremented:
#            g_move_count+=1

#        g_move_count_incremented = False  # keep this flag unset from now on; so that the move count is incremented

# Output the Move Number
#        append_to_output(lstrip(str(g_move_count)) + "." + constants.SPACE)


# Convert the chess move in order to output it
# Add a 'x' to the output chess move if a piece was taken
# Add the promoted piece if a promotion took place
# Then output the piece to the output file
    setup_output_chess_move_add_promotion(attacking_piece, from_file, from_rank, to_file, to_rank, taken)


# Now that the opponent has played, see if the computer is in check
    check_flag = in_check(constants.COMPUTER)
    if check_flag:
        print("I am in Check")
        add_check_to_output()
        check_flag = isit_Checkmate(constants.COMPUTER)
        if check_flag:
            output_chess_move = add_checkmate_to_output(output_chess_move)
            print("Checkmate!! You Win!")
#            append_to_output(output_chess_move + constants.SPACE)
#            output_all_chess_moves(constants.PLAYER_WON)
# todo
            print()
            goodbye()
            # *** END ***

# Output the chess move
#   append_to_output(output_chess_move + constants.SPACE)
# todo
    print()


def player_move_validation_loop(from_file, from_rank ,to_file, to_rank, just_performed_castling, attacking_piece, taken):
    """
    Input Validation of the Player's Move
    Main Validation Loop
    """

    while True:
        
        print()

        # fetch the next move from the player from keyboard
        input_string = trim(input("YOUR MOVE (e.g. e2e4): "))

        if input_string == "R":
            print("Player Resigned")
            # output_all_chess_moves(chess.COMPUTER_WON) todo
            goodbye()  # Player Resigned
            # *** END ***
            

        """
        *** CASTLING ***
        This is denoted by using capital 'O
        that is O-O and O-O-O
        It is not PGN notation to use ZEROS - However will cater for 0-0 and 0-0-0
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
            or not constants.chess_move_pattern.match(lower_string)):  # ([a-h][1-8]){2}
            os.system("clear")
            chess.showboard()
            print()
            print("I do not understand this input ", input_string)
            print("Format of chess moves ought to be 4 characters e.g. e2e4")
            print("Files should be a letter from a to h")
            print("Ranks should be a number from 1 to 8")
            continue
            
        # Determine the file and rank of each board name e.g. e2 ==> file 'e', rank '2'
        from_file = lower_string[0]
        from_rank = lower_string[1]
        to_file = lower_string[2]
        to_rank = lower_string[3]

        attacking_piece = chess.board_piece(from_file, from_rank)

        print_string = output_attacking_move(chess.PLAYER, from_file, from_rank, to_file, to_rank)
        # print() todo
        print(print_string)

        piece_value = chess.board_piece(from_file,from_rank)

        if piece_value < 0: # negative numbers are the Computer's Pieces
             print("This is not your piece to move")
             ...
             continue
        
        if  piece_value == constants.BLANK: # BLANK SQUARE
             print("There is no piece to be played, instead a Blank Square")
             ...
             continue
        
        (illegal, taken) = is_player_move_legal(from_file, from_rank, to_file, to_rank)
        if illegal:
            print("Illegal move")
            ...
            continue

        # Has the king been moved?
        # Has a rook been moved
        # TODO record_if_king_or_rook_have_moved(constants.PLAYER, from_file, from_rank, to_file, to_rank)

        # As the opponent advanced a pawn two squares? if yes, record the pawn's position
        # TODO record_pawn_that_advanced_by2(constants.PLAYER, from_file, from_rank, to_file, to_rank)

        # Increment the move count
        # Convert player's chess move for output
        # Output the chess move
        finalise_player_move(from_file, from_rank, to_file, to_rank, taken)
        # TODO just_performed_castling, attacking_piece, taken)


def player_move(from_file, from_rank, to_file, to_rank):
    """
    Firstly show the result of the computer move
    Then get and validate the player's move
    """

    if chess.player_first_move:
        # Player goes first so on the first iteration there is no processing of Computer Moves 
        chess.player_first_move = False
        return

    # From this point onwards, process computer moves
    (just_performed_castling, attacking_piece, taken) = (None, None, None)  # todo
    process_computer_move(from_file, from_rank, to_file, to_rank)
    #                               just_performed_castling, attacking_piece, taken)
    
    player_move_validation_loop(from_file, from_rank, to_file, to_rank, 
                                just_performed_castling,
                                attacking_piece,
                                taken)



def main_part2():
    """
    The main functionality of the Chess Program begins here
    """

    """
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
    result = None
    # Game Loop
    while True:
        player_move(from_file, from_rank, to_file, to_rank)
        chess.showboard()
        break

def main():
    try:
        main_part2()
    except Exception as error:
        print(error)
        handle_internal_error()
        quit()

if __name__ == "__main__":
    main()
