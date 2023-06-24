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
from game import Game
import moves as m
import fileio as f
import extras as e
import os
import re
from time import sleep
from extras import CustomException, in_check, is_it_checkmate, finalise_computer_move
import copy

def handle_internal_error():
    """
    Hopefully this method is not necessary
    I added this method just in case there is some kind of logic error
    that causes a chess logic problem e.g. a King piece being taken!
    If such a thing happens then abort this program with an error message
    """

    print("Computer resigns due to an internal error")
    print("Please investigate")
    f.output_all_chess_moves()  # todo
    e.goodbye()
    # Internal Error
    # *** END PROGRAM ***


def is_piece_taken(chess, to_file, to_rank, piece_sign):
    """
    Set up a message showing which user took which piece
    Return the positive value of the piece taken

    In addition I added a test to check that the attacking/taking logic
    is correctly working
    If a 'King' is about to be taken, raise an error because such a move
    is illegal in Chess

    Note the Kings' values are:
        Computer's King (-7500) and Player's King (5000)
    """

    Game.show_taken_message = ""
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
        raise CustomException("Internal Error: King piece about to be taken: "
                              + str(piece_taken))

    # Check whether the same colour is about to be taken
    # Of course, this should never happen!
    if ((piece_sign < 0 and chess.piece_sign(to_file, to_rank) < 0)
       or
       (piece_sign > 0 and chess.piece_sign(to_file, to_rank) > 0)):
        """
        Some internal logic error has occurred
        """
        raise CustomException("Internal Error: "
                              "Piece of the same colour about to be taken: "
                              + str(piece_taken))

    # Convert to a positive number
    piece_taken = abs(piece_taken)

    if piece_sign < 0:
        message = "Computer took your "
    else:
        message = "Player took my "

    index = to_file + to_rank
    Game.show_taken_message = message + chess.board[index].print_string()
    return piece_taken


""" TODO
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


def is_player_move_illegal(chess, from_file, from_rank, to_file, to_rank):

    """
    Determine whether the PLAYER'S move is illegal
    For example:
    1) Does the PLAYER'S move put the PLAYER in Check?
    2) Can the chosen piece make that move?
    Note: returns 'taken'
    """

    piece_sign = constants.PLAYER  # white piece
    all_possible_moves = e.movelist(chess, from_file, from_rank,
                                    piece_sign, False)

    # print("G>>>",Game.reading_game_file)
    # print(all_possible_moves) # todo
    # if Game.move_count > 21:
    #     input() # todo
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

            taken = is_piece_taken(chess, to_file, to_rank, piece_sign)
            # No error raised - so the above test passed

            # print("from/to taken",from_square,to_square,taken) todo

            # store From and To data so that it may be restored
            save_from_square = chess.board[from_square]
            save_to_square = chess.board[to_square]
            # if Game.move_count > 21:
            #     input("BEFORE MOVE " + to_square) # todo

            # Make the Player's move
            e.make_move_to_square(chess,
                                  from_square, to_square, to_file, to_rank)

            # Does this PLAYER's move place the PLAYER in Check?
            # If so, illegal move!

            check_flag = in_check(chess, constants.PLAYER)
            if check_flag:
                # reset play and restore board pieces
                # check_flag todo
                # checkmate # todo
                print("You are in Check")
                chess.board[from_square] = save_from_square
                chess.board[to_square] = save_to_square
                # Indicate that the chosen move placed the Player in Check
                return (True, True, taken)

            # Indicate not in check
            # check_flag todo
            return (False, False, taken)

    # Indicate that no legal move has been found
    return (True, None, None)


def coords_formula(file, rank):
    """
    Need to convert chessboard squares coordinates
    from chess algebraic notation to
    computer array notation
    COLUMN FIRST that is Y then X

    EG
    a8 TOP LEFT to 0,0 TOP LEFT
    h1 BOTTOM RIGHT to 7,7 BOTTOM RIGHT

    a8 to 0,0
    a7 to 0,1
    a1 to 0,7
    b8 to 1,0
    h8 to 7,0
    h7 to 7,1
    h1 to 7,7
    etc
    """

    file_number = ord(file) - constants.ASCII_A  # 97
    rank_number = constants.ASCII_EIGHT - ord(rank)
    return (file_number, rank_number)


def do_evaluation(chess, level, piece_sign, prune_factor,
                  from_file, from_rank,
                  to_file, to_rank,
                  bestscore):
    """
    Perform the evaluation using
    minimax/negamax formula
    """

    from_square = from_file + from_rank
    to_square = to_file + to_rank

    # store From and To data so that it may be restored
    save_from_square = chess.board[from_square]
    save_to_square = chess.board[to_square]
    if (Game.xy and level == 1):
        print("B4", from_square, to_square, save_from_square, save_to_square)
    if (save_from_square == "c6" or save_to_square == "c6"):
        print(chess.board["c6"])
        input("c6")
    targetvalue = chess.piece_value(to_square)
    (to_file_number, to_rank_number) = coords_formula(to_file, to_rank)
    # Make the move so that it can be evaluated
    e.make_move_to_square(chess,
                          from_square, to_square, to_file, to_rank)

    # negamax formula
    if level < constants.MAXLEVEL:
        temp_calc = (bestscore - targetvalue + piece_sign
                     * (8 - abs(4 - to_file_number) - abs(4 - to_rank_number)))

        Game.score += evaluate(chess,
                               level,
                               -piece_sign,
                               temp_calc)

    """
    Rod Bird's comment:
    Unwind the recursion by coming back here
    until we finally return to the main program flow
    Work out the score adding a small amount
    to favour forwards and central play
    """

    temp_calc = (8 - abs(4 - to_file_number) - abs(4 - to_rank_number))
    Game.score += targetvalue - piece_sign * temp_calc

    """
    Rod Bird's comment:
    If it results in a better score than previously
    then store it as the best
    """

    if ((piece_sign < 0 and Game.score > bestscore)
       or
       (piece_sign > 0 and Game.score < bestscore)):
        bestscore = Game.score
        if level == 1:
            # Record the best move found so far
            Game.best_from_file = from_file
            Game.best_from_rank = from_rank
            Game.best_to_file = to_file
            Game.best_to_rank = to_rank

        # Restore previous squares
        chess.board[from_square] = save_from_square
        chess.board[to_square] = save_to_square
        if (Game.xy and level == 1):
            print("AFT", from_square, to_square, chess.board[from_square], chess.board[to_square])
            if (save_from_square == "c6" or save_to_square == "c6"):
                print(chess.board["c6"])
                input("c6 restore")

        """
        Rod Bird's comment:
        If it is not as good as a previous piece move
        then cut the search short
        Exit the loop in 'evaluate'
        """

        if ((piece_sign < 0 and bestscore >= prune_factor)
           or
           (piece_sign > 0 and bestscore <= prune_factor)):
            exitloop = True

        else:
            # Continue the loop i.e. continue evaluating
            exitloop = False

        return (exitloop, bestscore)

    # Restore previous squares
    chess.board[from_square] = save_from_square
    chess.board[to_square] = save_to_square
    if (Game.xy and level == 1):
        print("AFT2", from_square, to_square, chess.board[from_square], chess.board[to_square])
        if (save_from_square == "c6" or save_to_square == "c6"):
            print(chess.board["c6"])
            input("c6 restore2")
    # Continue the loop i.e. continue evaluating
    exitloop = False
    return (exitloop, bestscore)


def evaluate(chess, level, piece_sign, prune_factor):
    """
    To quote Rod Bird:
    This function checks all squares for players
    to move then recursively test plays.
    It plays its own move then plays the opponent's best move,
    recursively over four moves.
    So getting the potential net worth of each moveable player on the board.
    The highest scored determines the computer's next move.
    It is a classic mini max evaluation shortened
    to its a negamax form with pruning
    i.e. it does not waste time on lower value plays.
    """

    # Update recursion level
    level += 1
    if level > constants.MAXLEVEL:
        raise CustomException("Internal Error: Level Number Overflow: "
              + str(level))

    bestscore = constants.EVALUATE_THRESHOLD_SCORE * piece_sign
    # Go through each square on the board

    """
    PRESET_CHESSBOARD is a list containing the entire chessboard coordinates
    ['a1', 'a2' ... 'h7', 'h8']
    In order to
    1) save time in regards to generating such a list from scratch
    2) the need for two nested for-loops in regards to generating the list
    3) Instead I filter PRESET_CHESSBOARD for all the pieces of
       the same colour of the current user using a List Comprehension
    """

    same_colour_pieces_list = [index for index in constants.PRESET_CHESSBOARD
                               if chess.piece_sign(index) == piece_sign]

    for index in same_colour_pieces_list:
        # Have a same coloured piece - evaluate its score
        from_file = index[0]
        from_rank = index[1]

        all_the_moves = e.movelist(chess, from_file, from_rank,
                                   piece_sign, level == 1)
        # TODO
        # if level == 1:  # Level 1 # todo refactor with level == 1 ==>
        #     all_the_moves = movelist(chess, from_file, from_rank,
        #                              piece_sign, True)
        # else:
        #     all_the_moves = movelist(chess, from_file, from_rank,
        #                              piece_sign, False)

        # Loop through each possible move
        for m in range(len(all_the_moves)):
            # todo
            # For level=1, add logic to handle castling

            (to_file, to_rank) = all_the_moves[m]
            oldscore = Game.score
            (exit_loop, bestscore) = do_evaluation(chess, level,
                                                   piece_sign,
                                                   prune_factor,
                                                   from_file, from_rank,
                                                   to_file, to_rank,
                                                   bestscore)

            # Restore 'score'
            Game.score = oldscore
            if exit_loop:
                return bestscore  # Done!

            # Otherwise continue evaluating
            continue

    return bestscore  # Done!


def execute_computer_move(chess, from_file, from_rank, to_file, to_rank):
    """
    Carry out the chess move that was produced
    by the 'evaluate' function
    Note: returns 'attacking_piece_letter, taken'
    """

    piece_sign = constants.COMPUTER  # black piece
    # display the move
    attacking_piece_letter = chess.piece_letter(from_file, from_rank)

    Game.computer_print_string = m.output_attacking_move(chess,
                                                         constants.COMPUTER,
                                                         from_file, from_rank,
                                                         to_file, to_rank)

    """
    Check whether a Player's piece is about to be taken
    Print a Message if this is true
    At the same time,
    Check whether the Player's King is about to be literally taken
    If so, this indicates an Internal Logic Error
    It would mean the COMPUTER's best move is an illegal move!
    'Kings' cannot actually be taken in Chess!
    """

    from_square = from_file + from_rank
    to_square = to_file + to_rank
    taken = is_piece_taken(chess, to_file, to_rank, piece_sign)
    # No error raised - so the above test passed

    # Make the Computer's move
    e.make_move_to_square(chess, from_square, to_square, to_file, to_rank)

    # If the COMPUTER cannot play out of check then resign
    check_flag = in_check(chess, constants.COMPUTER)
    if check_flag:
        e.computer_resigns()
        # *** END PROGRAM ***

    # Has the king been moved?
    # Has a rook been moved?
    m.record_if_king_or_rook_has_moved(chess, constants.COMPUTER,
                                       from_file, from_rank, to_file, to_rank)

    # As the opponent advanced a pawn two squares?
    # If yes, record the pawn's position
    m.record_pawn_that_advanced_by2(chess, constants.COMPUTER,
                                    from_file, from_rank, to_file, to_rank)

    # Convert the chess move in order to output it
    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # Then output the piece to the output file
    m.setup_output_chess_move_add_promotion(attacking_piece_letter,
                                            from_file, from_rank,
                                            to_file, to_rank, taken)


def process_computer_move(chess, from_file, from_rank, to_file, to_rank):
    """
    This routine handles the playing of the Computer's move
    Note: returns 'computer_move_finalised, just_performed_castling,
                   attacking_piece_letter, taken'
    """

    computer_move_finalised = False
    just_performed_castling = False
    attacking_piece_letter = ""
    taken = None

    if Game.player_first_move:
        # Player goes first so on the very first iteration
        # there is no processing of Computer Moves
        Game.player_first_move = False
        return

    # From this point onwards, process the Computer's move

    # king on king end game?
    # Stalemate?
    if Game.evaluation_result < constants.STALEMATE_THRESHOLD_SCORE:
        e.computer_resigns()
        # *** END PROGRAM ***

    # Are the Chess moves currently coming from an input file?
    # If so, fetch the next move from there
    if Game.reading_game_file:
        tuple = f.handle_computer_move_from_inputfile(chess,
                                                      from_file, from_rank,
                                                      to_file, to_rank)
        (computer_move_finalised,
         from_file, from_rank,
         to_file, to_rank) = tuple

    """
    At this stage, three possibilities
    # 1) 'evaluate' function generated a Castling Move
    # 2) No longer reading Chess Moves from an input file
    # 3) No Chess Move has been finalised
    """

    # Handle 1) Castling Move if one was generated by the 'evaluate' function
    # Keep linter happy - shorten name
    c = m.handle_evaluated_castling_move(chess, computer_move_finalised)

    computer_move_finalised = c

    # Handle 2 and 3
    # Validate, Execute then Finalise the Computer Chess Move
    # (if it was not a Castling Chess Move 
    #  or if it is not a 'finalised' computer move)
    if not computer_move_finalised:
        execute_computer_move(chess, from_file, from_rank, to_file, to_rank)
        finalise_computer_move(chess)

    return


def finalise_player_move(chess, it_is_a_castling_move,
                         from_file=None, from_rank=None,
                         to_file=None, to_rank=None,
                         print_string="", attacking_piece_letter="",
                         taken=None):
    """
    Now that the Player's move has been performed
    Increment the move count (if not reading from a file)
    Display the chess move to the Player
    Output the chess move to the output stream
    Determine whether the Computer is in Check
    If so, determine to see if the Player has won
    That is, is it Checkmate?
    """

    if not Game.reading_game_file:
        # Increment Move Number
        if not Game.move_count_incremented:
            Game.move_count += 1

        # keep this flag unset from now on; so that the move count is incremented
        Game.move_count_incremented = False

        # Output the Move Number
        e.append_to_output_stream(str(Game.move_count) + "." + constants.SPACE)

    if not it_is_a_castling_move:
    # Convert the chess move in order to output it
    # Add a 'x' to the output chess move if a piece was taken
    # Add the promoted piece if a promotion took place
    # (The above does not apply to the Castling move) 
        m.setup_output_chess_move_add_promotion(attacking_piece_letter,
                                                from_file, from_rank,
                                                to_file, to_rank, taken)

    # Then display the chess move to the Player
    if print_string:
        # Display the move
        chess.display(print_string)
        if (Game.show_taken_message):
            # Show what piece the Player took
            print(Game.show_taken_message)

            # input("PLAYER TAKEN/2") TODO
    # input("CHECK - SHOULD BE WHITE1> ") # TODO

    # If an en passant move has been performed, 
    # the Check test has already been done - no need to repeat it
    if Game.en_passant_status == constants.VALID:
        # Then output the chess move to the output stream
        e.append_to_output_stream(Game.output_chess_move + constants.SPACE)
        print("REPEAT")
        input(Game.output_chess_move)
        return

    # Now that the Player has played, see if the Computer is in Check
    if Game.move_count >= 7 and Game.who_are_you<0:
            Game.xy = True
    check_flag = in_check(chess, constants.COMPUTER)
    if check_flag:
        input("CF") # TODO
    # input("CF") todo
        print("I am in Check")
        m.add_check_to_output()
        check_flag = is_it_checkmate(chess, constants.COMPUTER)
        if check_flag:
            # Keep Linter happy - shorten name
            chess_move = Game.output_chess_move

            Game.output_chess_move = m.add_checkmate_to_output(chess_move)
            print("Checkmate!! You Win!")
            # Then output the chess move to the output file
            e.append_to_output_stream(Game.output_chess_move + constants.SPACE 
                                      + constants.PLAYER_WON)
            f.output_all_chess_moves()
            print()
            e.goodbye()
            # Checkmate!
            # *** END PROGRAM ***
        input("CF2") # todo
        # input("CF2")  TODO
    # Then output the chess move to the output stream
    e.append_to_output_stream(Game.output_chess_move + constants.SPACE)


def handle_castling_input(chess, input_string):
    """
    *** CASTLING ***
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
    m.castling_move_was_valid(chess)
    do_next = "return"
    return do_next


def player_move_validation_loop(chess, from_file, from_rank, to_file, to_rank):
    """
    Input Validation of the Player's Move
    Main Validation Loop
    """

    computer_move_finalised = False
    just_performed_castling = False
    attacking_piece_letter = ""
    print_string = ""
    taken = None

    while True:

        # print() TODO

        # Are the moves being read from the input game file?
        # If so, fetch the next move from there
        # Note: If the move that is read is an en passant move
        # Then it is performed at this stage
        # within the functionality of
        # 'handle_player_move_from_inputfile'

        # Game.en_passant_status is:
        #   set to 'constants.VALID' for a valid en passant move
        #   set to 'constants.INVALID' for an illegal en passant move
        #   set to 'constants.NOVALUE' for a non-en-passant move

        do_next = f.handle_player_move_from_inputfile(chess,
                                                      from_file, from_rank,
                                                      to_file, to_rank)
        if do_next == "return":
            return
        elif do_next == "continue":
            continue
        # else do_next is "pass"

        # *** EN PASSANT ***
        # At this point, a chess move has successfully been read and parsed
        # from the input game file
        # Was this chess move, an en passant move?

        # Keep linter happy - shorten name
        funcname = m.finalise_en_passant_move_from_inputfile

        do_next = funcname(chess,
                           constants.PAWN_LETTER,
                           constants.PAWN_VALUE)
        if do_next == "return":
            # The en passant move was valid and it has been performed
            return
        elif do_next == "continue":
            # The en passant move was invalid!
            continue
        # else do_next is "pass"
        # It was not an en passant move
        # Continue

        if not Game.reading_game_file:
            # fetch the next move from the player from the keyboard
            (do_next, lower_string) = e.handle_player_move_from_keyboard(chess)
            if do_next == "return":
                return
            elif do_next == "continue":
                continue
            # else do_next is "pass"

            # Determine the file and rank of each board name
            # e.g. e2 ==> file 'e', rank '2'
            from_file = lower_string[0]
            from_rank = lower_string[1]
            to_file = lower_string[2]
            to_rank = lower_string[3]
            print(lower_string)  # todo

        else:
            # If the move was read from the input file
            # populate the relevant values
            # Note: although it is fair to assume that ALL the Chess Moves
            # in the input file are legal
            # Nevertheless the input file's moves will be validated
            # as if the user has entered them
            from_file = Game.new_from_file
            from_rank = Game.new_from_rank
            to_file = Game.new_to_file
            to_rank = Game.new_to_rank

        attacking_piece_letter = chess.piece_letter(from_file, from_rank)

        print_string = m.output_attacking_move(chess, constants.PLAYER,
                                               from_file, from_rank,
                                               to_file, to_rank)
        # print() todo
        # print(print_string)

        piece_value = chess.piece_value(from_file, from_rank)

        # Loop until a valid move is played
        # If an erroneous move was read from the input file,
        # then there will be no further input from this file

        if piece_value == constants.BLANK:  # BLANK SQUARE
            chess.display(print_string)
            print("There is no piece to be played, instead a Blank Square")
            e.is_error_from_input_file()
            continue

        if piece_value < 0:  # negative numbers are the Computer's Pieces
            chess.display(print_string)
            print("This is not your piece to move")
            e.is_error_from_input_file()
            continue

        # Check whether the Player entered an en passant move
        # 'print_string' N/A since the en passant routines
        # will display their own messages using 
        # 'attacking_piece_letter' and 'taken'
        do_next = m.handle_en_passant_from_keyboard(chess, from_file, from_rank,
                                                    to_file, to_rank)
        if do_next == "return":
            # Inform Player that Kool AI is thinking!
            print("I am evaluating my next move...")
            return
        elif do_next == "continue":
            continue
        # else do_next is "pass"
        # It was not an en passant move

        # Check legality of Player's move
        # If legal, the move is played
        (illegal,
         illegal_because_in_check,
         taken) = is_player_move_illegal(chess,
                                         from_file, from_rank,
                                         to_file, to_rank)
        if illegal_because_in_check:
            if not Game.it_is_checkmate:
                chess.display(print_string)
                print("Illegal move because you are in check")
            else:
                chess.display(print_string)
                print("Illegal move because it is Checkmate!")
            continue

        elif illegal:
            chess.display(print_string)
            print("Illegal move")
            continue

        # Has the king been moved?
        # Has a rook been moved?
        m.record_if_king_or_rook_has_moved(chess, constants.PLAYER,
                                           from_file, from_rank,
                                           to_file, to_rank)

        # As the opponent advanced a pawn two squares?
        # If yes, record the pawn's position
        m.record_pawn_that_advanced_by2(chess, constants.PLAYER,
                                        from_file, from_rank,
                                        to_file, to_rank)

        # Increment the move count
        # Determine whether the Computer is in Check
        # Convert player's chess move for output
        # Output the chess move
        finalise_player_move(chess, False,
                             from_file, from_rank, to_file, to_rank,
                             print_string, attacking_piece_letter, taken)

        # Valid move has been played - show the updated board
        # Display the Player's Move
        
        #chess.display(print_string)
        #if (Game.show_taken_message):
            # Show what piece the Player took
        #    print(Game.show_taken_message)
        # CF3 TODO
        
        # Pause so that the Player
        # can see the description of the move that the Player chose
        # Inform Player that Kool AI is thinking!
        if not Game.reading_game_file:
            print("I am evaluating my next move...")

        sleep(constants.SLEEP_VALUE)
        return


def play_2_moves(chess, from_file, from_rank, to_file, to_rank, result):
    """
    1) Play and show the result of the Computer move
    2) Then get, validate and play the Player's move
    """

    process_computer_move(chess, from_file, from_rank, to_file, to_rank)
    # if (Game.move_count > 15): # todo
    input("GO")

    player_move_validation_loop(chess, from_file, from_rank, to_file, to_rank)
    # if (Game.move_count > 15): # todo
    x = input("GO/2")
    if x == "Y" or x == "y":
        Game.xy = True # todo
#  TODO             just_performed_castling, attacking_piece_letter, taken)


def main_part2():
    """
    The main functionality of the Chess Program begins here

    Initialise the Game
    Display the Board
    Start the Main Loop
    """

    chess = Game()
    Game.xy = False # TODO

    f.open_input_file()

    chess.fillboard()
    os.system("clear")
    chess.showboard()

    # remove todo
    from_file = None
    from_rank = None
    to_file = None
    to_rank = None

    # Game Loop
    while True:
        play_2_moves(chess,
                     Game.best_from_file,
                     Game.best_from_rank,
                     Game.best_to_file,
                     Game.best_to_rank,
                     Game.evaluation_result)

        # todo - REMOVE
        #  os.system("clear")
        #  chess.showboard()
        if (Game.xy or Game.move_count >= 7): # todo
            print(chess.board["c6"], Game.promoted_piece, Game.output_stream)
            input("EVAL ENTER " + Game.promoted_piece + Game.output_stream)
         
        board_copy = copy.deepcopy(chess)
        Game.evaluation_result = evaluate(chess, 0,
                                          constants.COMPUTER,
                                          constants.EVALUATE_THRESHOLD_SCORE)
        chess = board_copy
        if (Game.xy or Game.move_count >= 7): # todo
            print(chess.board["c6"], Game.promoted_piece, Game.output_stream)
            input("FINISHED EVAL " + Game.promoted_piece + Game.output_stream)
            chess.display("C6 a8 h1")
            print(chess.board["c6"], chess.board["a8"], chess.board["h1"],
                        Game.promoted_piece, Game.output_stream)
            input() # todo
        # remove todo
        # from_file = Game.best_from_file
        # from_rank = Game.best_from_rank


def main():
    """
    Main Routine
    Begin Here
    Report any errors
    """

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
