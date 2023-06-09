"""
fileio.py
For testing purposes Chess moves are read from an input file
So this file contains all the routines related to reading chess moves
from a file and their validation.
"""

import constants
from game import Game
import extras as e
import moves as m
from time import sleep
import re
import os
from extras import CustomException, finalise_computer_move


def cleanup_input_stream(in_string):
    """
    Sanitise the input
    That is remove any superfluous CARRIAGE RETURNS
    or any nonprintable characters
    """

# Convert any \r\n to \n - Remove superfluous CARRIAGE RETURNS \r i.e. \x0D
    regexp = r"\r+\n"
    work_string = re.sub(regexp, "\n", in_string)

# Remove nonprintables
# Remove any possibility of SAN move suffix annotations
# i.e. remove ! and ? characters
    regexp = r"[!?\x00-\x08\x0B-\x1F\x7F-\xFF]"
    work_string = re.sub(regexp, "", work_string)

# Replace any horizontal tabs with spaces
    work_string = work_string.replace(constants.TAB, constants.SPACE)

# Trim the string of whitespace
# ensure there is an extra \n at the end, if not null
    work_string = work_string.strip()
    if work_string:
        return work_string + "\n"

    return ""


def ignore_group_comment(open_char, close_char):
    """
    Remove everything between the delimiters
    'open_char' and 'close_char'
    Including the delimiters
    """

    position = Game.input_stream.find(close_char)
    if position < 0:
        astring = ("Found " + open_char + " however cannot determine where "
                   + close_char + " ends")
        e.input_status_message(astring)
        return False

    Game.input_stream = Game.input_stream[position + 1:]
    return True


def ignore_rav():
    """
    Remove everything between the parentheses
    Including the parentheses
    Note: the parentheses can be nested
    """

    LPAREN = "("
    count = 1  # Already found the first parenthesis
    position = 1  # So start the search to the right of it
    while True:
        #                   r"[()]"
        matched = constants.parens_pattern.search(Game.input_stream, position)
        if not matched:
            break

        elif matched.group(0) == LPAREN:
            count += 1
            position = matched.end(0)
            continue

        else:  # must be the right parenthesis
            count -= 1
            if count == 0:
                # Found the matching RAV ( ... ) - remove it
                Game.input_stream = Game.input_stream[matched.end(0):]
                return True

            position = matched.end(0)
            continue

    # No closing parenthesis found
    e.input_status_message("Cannot determine where this RAV closes: "
                           + Game.input_stream[0:20])
    return False


def remove_the_suffix(text, suffix):
    """
    A Function To Remove a Suffix in Python
    Taken from https://datagy.io/python-remove-prefix-suffix/
    """
    if text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text


def open_input_file():
    """
    The file 'input.pgn' will be used to hold
    Chess 'Movetext in PGN format' for testing purposes
    Open this file and read its contents
    If this is an IOError e.g. the file does not exist;
    or the file is empty,
    Set file_contents and input_stream to ""
    """

    Game.input_stream = ""

    try:
        with open(constants.INPUT_PGN_NAME) as pgn_input_file:
            Game.directory_of_open_inputfile = (
                    remove_the_suffix(os.path.realpath(pgn_input_file.name),
                                      constants.INPUT_PGN_NAME))
            file_contents = pgn_input_file.read()
            if len(file_contents) != 0:
                Game.input_stream = file_contents
                Game.reading_game_file = True

    except IOError:
        file_contents = ""

    if len(file_contents) == 0:
        # Empty file
        Game.reading_game_file = False
        # Game.input_stream already set to ""
        return

    if len(file_contents) > constants.FILE_SIZE_LIMIT:
        e.input_status_message(("Input file too big - larger than "
                               "{} characters")
                               .format(constants.FILE_SIZE_LIMIT))
        sleep(5)
        return

    Game.input_stream = cleanup_input_stream(file_contents)
    if len(Game.input_stream) == 0:
        # Null string i.e. Empty file contents
        Game.reading_game_file = False
        # Game.input_stream already set to ""


def output_to_screen(outtable, output_ok, output_filename=""):
    """
    Print outtable's contents to the screen
    """
    print("The moves of this Chess Game are as follows:")
    print()
    for i in range(len(outtable)):
        print(outtable[i])
    print()
    if output_ok:
        print(f"These moves have also been written to {output_filename}")
        print()


def output_all_chess_moves():

    """
    Divide the string up into a list
    EG 1. e2e4 c7c6 2. d2d4 d7d5
    INTO 'thelist'
    ["1.", "e2e4", "c7c6", "2.", "d2d4", "d7d5"]
    Add items from 'thelist' to the output string 'line' up to
    the length of constants.LINESIZE (currently 73)
    Once this length as been exceeded, print 'line'
    and then set 'line' to the current item
    and repeat the process until the entire list has been processed

    Then
    1) Print outtable's contents to the output file 'output.pgn'
    in input.pgn's directory or the current working directory
    2) Print outtable's contents to the screen
    """

    thelist = Game.output_stream.split()
    if not thelist:  # empty?
        return

    outtable = []
    line = ""
    surplus = ""
    while thelist:
        # Remove the first item of the list
        surplus = thelist.pop(0) + " "
        if len(line) + len(surplus) <= constants.LINESIZE:
            line += surplus
        else:
            outtable.append(line.rstrip())
            line = surplus

    # Last item
    outtable.append(line.rstrip())

    output_ok = False
    if not Game.directory_of_open_inputfile:
        # Output to the screen only
        output_to_screen(outtable, output_ok)
        return

    try:
        output_filename = (Game.directory_of_open_inputfile
                           + constants.OUTPUT_PGN_NAME)

        with open(output_filename, "w") as pgn_output_file:
            for i in range(len(outtable)):
                pgn_output_file.write(outtable[i] + "\n")
        output_ok = True
    except IOError:
        # Ignore any output errors - rather, write to the screen instead
        pass

    output_to_screen(outtable, output_ok, output_filename)


def regexp_loop():
    """
    Parse the input stream
    Remove any comments and annotations which are part of the PGN file notation
    This will loop until a potential chess move string is found
    or end of string
    """

    LPAREN = "("
    LBRACE = "{"
    RBRACE = "}"
    OA_BRACKET = "<"  # open angled bracket
    CA_BRACKET = ">"  # close angled bracket

    while True:

        # Remove any leading whitespace
        Game.input_stream = Game.input_stream.lstrip()
        if len(Game.input_stream) == 0:
            e.input_status_message("Finished reading "
                                   "all the moves from the input file")
            return True

        # % Escape mechanism - This mechanism is triggered
        # by a percent sign character ("%") appearing
        # in the first column of a line;
        # the data on the rest of the line is ignored up to the next \n

        #                   r"(\A%)|(\n%)"
        matched = constants.percent_pattern.match(Game.input_stream)
        if matched:
            # The length is either 1 or 2 -
            # the correct starting position for the 'find'
            position = Game.input_stream.find("\n", len(matched.group(0)))
            if position < 0:  # No \n found - therefore, remove entire contents
                Game.input_stream = ""
                continue

        # Remove everything up to and including the \n
            Game.input_stream = Game.input_stream[position + 1:]
            continue

        # Remove any leading whitespace i.e. including \n
        Game.input_stream = Game.input_stream.lstrip(" \n\t")

        # Just in case any found - remove an 'En Passant' annotation,
        # that is 'e.p.'
        #                             r"\A(e\.p\.[ \n]*)+"
        Game.input_stream = constants.en_passant_pattern.sub("",
                                                             Game.input_stream,
                                                             count=1)

        if len(Game.input_stream) == 0:
            e.input_status_message("Finished reading "
                                   "all the moves from the input file")
            return True

        firstchar = Game.input_stream[0:1]

# Comment text may appear in PGN data. There are two kinds of comments.
# The first kind is the "rest of line" comment; this comment type starts with a
# semicolon character and continues to the end of the line.  The second kind
# starts with a left brace character and continues to the next right brace
# character.

        if firstchar == ";":
            # Ignore up to the end of the line
            position = Game.input_stream.find("\n")
            if position < 0:  # No \n found - therefore, remove entire contents
                Game.input_stream = ""
                continue

            # Remove everything up to and including the \n
            Game.input_stream = Game.input_stream[position + 1:]
            continue

        elif firstchar == LBRACE:
            # Ignore up to and including the following right brace
            position = ignore_group_comment(LBRACE, RBRACE)
            if not position:
                return False
            else:
                continue

        elif firstchar == OA_BRACKET:
            # Ignore up to and including
            # the following right close angled bracket
            position = ignore_group_comment(OA_BRACKET, CA_BRACKET)
            if not position:
                return False
            else:
                continue

        elif firstchar == LPAREN:  # I.E. LEFT PARENTHESIS
            # An RAV (Recursive Annotation Variation)
            # is a sequence of movetext containing
            # one or more moves enclosed in parentheses.
            # Because the RAV is a recursive construct, it may be nested.
            # Ignore up to and including
            # the corresponding right nested parenthesis

            position = ignore_rav()
            if not position:
                return False
            else:
                continue

        elif firstchar == "$":  # I.E. $nnn
            # An NAG (Numeric Annotation Glyph) is a movetext element
            # that is used to indicate a simple annotation
            # in a language independent manner.
            # An NAG is formed from a dollar sign ("$")
            # with a non-negative decimal integer suffix

            #                   r"\A\$[0-9]+"
            matched = constants.nag_pattern.match(Game.input_stream)
            if matched:
                # Ignore $nnn
                Game.input_stream = Game.input_stream[matched.end(0):]
                continue

            e.input_status_message("Cannot determine this NAG: "
                                   + Game.input_stream[0:6])
            return False

        else:
            # Either Move Number, a Chess Move or no more data
            return True


def handle_move_suffix(matched):

    """
    Skip over the 'matched' string
    Remove any trailing symbol continuation characters.
    These continuation characters are letter characters ("A-Za-z"),
    digit characters ("0-9"),
    the plus sign ("+"), the octothorpe sign ("#"),
    the equal sign ("="), the colon (":"),  and the hyphen ("-").
    Therefore, ignore suffix text such as =Q+
    """

    Game.input_stream = Game.input_stream[matched.end(0):]
    #                             r"\A[A-Za-z0-9+#=:\-]*"
    Game.input_stream = constants.chess_move_suffix_pattern.sub(
                                                            "",
                                                            Game.input_stream,
                                                            count=1)


def triple_tuple(matched):
    """
    For example:
    (the piece, the source square, the destination square)
    Fetch the matched string and create the tuple
    """

    Game.general_string_result = matched.group(0)

    #                                PIECE
    Game.chess_move_tuple = (matched.group(1),
                             #  FROM
                             matched.group(2),
                             #  TO
                             matched.group(3))
    handle_move_suffix(matched)


def double_tuple_with_piece(matched):
    """
    For example: Bxh6
    Piece: B for Bishop
    Destination: h6
    No Source Square!
    (the piece, the destination square)
    Fetch the matched string and create the tuple
    Add a null item to make the tuple a length of 3
    """

    Game.general_string_result = matched.group(0)
    #                        PIECE                 DESTINATION
    Game.chess_move_tuple = (matched.group(1), "", matched.group(2))
    handle_move_suffix(matched)


def double_tuple_with_source(matched):
    """
    For example: Chess move: gxh6
    Source: g
    Destination: h6
    No Piece!
    (the source square, the destination square)
    Fetch the matched string and create the tuple
    Add a null item to make the tuple a length of 3
    """

    Game.general_string_result = matched.group(0)
    #                            SOURCE            DESTINATION
    Game.chess_move_tuple = ("", matched.group(1), matched.group(2))
    handle_move_suffix(matched)


def parse_chess_move(chess):
    """
    Parse the chess move into a tuple
    Place the tuple into 'Game.chess_move_tuple'
    Place the matched string result into 'Game.general_string_result'
    Note: the order of these regular expression patterns is significant
    """

    Game.input_stream_previous_contents = Game.input_stream[0:20]

    # EIGHT REGEXPS

    """
    1)

    *** NON-AMBIGUOUS LONG NOTATION SHOWING PIECE
    & COORDINATES OF BOTH PIECES ***
    *** HANDLE MOVES/CAPTURES REGARDING PIECES
    DETERMINED BY BOTH two character square coordinates ***
    EG Ng1f3 e2e4
    An En Passant move could be of this format
    tuple format: (the piece, the source square, the destination square)
    """

    #                   r"\A([KQRBN]?)([a-h][1-8])([a-h][1-8])
    matched = constants.long_notation_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the source square, the destination square
        Game.move_type = constants.LONG_NOTATION
        triple_tuple(matched)
        return True  # Indicate success

    """
    2)

    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED
    BY BOTH two character square coordinates ***
    EG Nd2xe4  e4xd5
    An En Passant move could be of this format
    tuple format: (the piece, the source square, the destination square)
    """

    #                   r"\A([KQRBN]?)([a-h][1-8])x([a-h][1-8])"
    matched = constants.capture_2squares_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the source square, the destination square
        Game.move_type = constants.PIECE_BOTH_SQUARES
        triple_tuple(matched)
        return True  # Indicate success

    """
    3)

    *** HANDLE e4 Ng2 ***
    Note: This program does NOT support En Passant captures of the form EG d6
    En Passant captures must contain a 'x' EG exd6
    tuple format: (the piece optional , the destination square)
    """

    #                   r"\A([KQRBN]?)([a-h][1-8])"
    matched = constants.one_square_pattern.match(Game.input_stream)
    if matched:
        # That is, just piece and the destination square only
        Game.move_type = constants.DESTINATION_SQUARE_ONLY
        double_tuple_with_piece(matched)
        return True  # Indicate success

    """
    4)

    *** HANDLE PAWN CAPTURES USING 'file' EG exd4 ***
    EG exd4
    An En Passant move could be of this format
    tuple format: (the file , the destination square)
    """

    #                   r"\A([a-h])x([a-h][1-8])"
    matched = constants.pawn_capture_pattern.match(Game.input_stream)
    if matched:
        # That is, just the file and the destination square only
        Game.move_type = constants.PAWN_CAPTURE_FILE
        double_tuple_with_source(matched)
        return True  # Indicate success

    """
    5)

    *** HANDLE CAPTURES REGARDING OTHER PIECES EG Qxd4 ***
    No possibility of an En Passant move in this format
    tuple format: (the piece, the destination square)
    """

    #                   r"\A([KQRBN])x([a-h][1-8])"
    matched = constants.nonpawn_capture_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece and the destination square
        # EG Qxe1 Kxf7 Rxe1+
        Game.move_type = constants.PIECE_DESTINATION_SQUARE
        double_tuple_with_piece(matched)
        return True  # Indicate success

    """
    6)

    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED BY THEIR 'file' ***
    EG Nge2  - THE FILE BEING 'g'
    EG Nfxe4 - THE FILE BEING 'f'

    This pattern does not apply to Pawns
    Therefore, no possibility of an En Passant move in this format
    tuple format: (the piece, the file, the destination square)
    """

    #                   r"\A([KQRBN])([a-h])x?([a-h][1-8])
    matched = constants.file_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the file and the destination square
        Game.move_type = constants.PIECE_FILE_MOVE
        triple_tuple(matched)
        return True  # Indicate success

    """
    7)

    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED BY THEIR 'rank' ***
    EG N2d4  - THE RANK BEING '2'
    EG N6xe4 - THE FILE BEING 'G'

    This pattern does not apply to Pawns
    Therefore, no possibility of an En Passant move in this format
    tuple format: (the piece, the rank, the destination square)
    """

    #                   r"\A([KQRBN])([1-8])x?([a-h][1-8])
    matched = constants.rank_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the rank and the destination square
        Game.move_type = constants.PIECE_RANK_MOVE
        triple_tuple(matched)
        return True  # Indicate success

    """
    *** CASTLING ***
    This is denoted by using capital 'O' that is O-O and O-O-O
    It is not PGN notation to use ZEROS - However will cater for 0-0 and 0-0-0
    No tuple used for this chess move
    Place the matched string in 'Game.general_string_result'
    in order to later convert 0-0-0 to O-O-O or 0-0 to O-O
    """

    #                   r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))"
    matched = constants.castling_inputfile_pattern.match(Game.input_stream)
    if matched:
        Game.move_type = constants.CASTLING_MOVE
        Game.general_string_result = matched.group(0)
        handle_move_suffix(matched)
        return True  # Indicate success

# Unknown Chess Move
    chess.display("Cannot match chess move")
    e.input_status_message(constants.BAD_CHESS_MOVE_FROMFILE
                           + Game.input_stream[0:20])
    return False  # Indicate failure


def check_game_termination_marker_found():
    """
    Determine if the parsed string is either
    #       "1-0" (White wins), "0-1" (Black wins),
    #       "1/2-1/2" (drawn game), OR "*"
    """

    result = False
    #                   r"\A((1-0)|(0-1)|(1/2-1/2)|[*])"'
    matched = constants.game_termination_pattern.match(Game.input_stream)
    if matched:
        # Reached the Indicator regarding the Result and the End of the Game
        e.input_status_message(
                     "Result of the Game has been read from the input file: "
                     + matched.group(0))
        result = True

# Remove it from the input stream
        Game.input_stream = Game.input_stream[len(matched.group(0)):]

    return result


def expected_move_number_not_found():
    """
    Report that an expected move number could not be determined
    """

    e.input_status_message("Expected Move Number " + str(Game.move_count)
                           + ". Instead: " + Game.input_stream[0:10])


def parse_move_text(chess):
    """
    1)
    If it is the Player's turn, then a Move Number is expected
    to be parsed first. The Move Number parsed must match
    the current Move Number Count.
    2)
    Then a Chess Move is expected, which will be parsed
    into a tuple of the following form:
    (the piece optional, the destination square)
    The parsed chess move string is placed in 'Game.general_string_result'
    3)
    During Parsing, all PGN comments and annotations are ignored
    """

    if Game.whose_move == constants.COMPUTER:
        Game.global_piece_sign = constants.COMPUTER
        # For parsing a Computer's move, check that
        # it is not a number nor a string of periods e.g. ...
        #                   r"\A([0-9]+|[.]+)"
        matched = constants.number_periods_pattern.match(Game.input_stream)
        if matched:
            chess.display("Expected the Computer's Chess Move")
            e.input_status_message("Not Numbers or Periods: "
                                   + Game.input_stream[0:10])
            return False

        # Otherwise
        return parse_chess_move(chess)

    # Therefore, Game.whose_move is == constants.PLAYER
    # Increment the Move Counter
    Game.global_piece_sign = constants.PLAYER
    Game.move_count += 1
    Game.move_count_incremented = True

    # Output the Move Number
    e.append_to_output_stream(str(Game.move_count) + "." + constants.SPACE)

    # Move Number expected EG '4.' I will allow periods to be optional
    #                   r"\A([0-9]+)[. ]*"
    matched = constants.move_number_pattern.match(Game.input_stream)
    if not matched:
        expected_move_number_not_found()
        return False

    # Determine the move number that was read by conversion
    try:
        move_number = int(matched.group(1))
    except ValueError:
        expected_move_number_not_found()
        return False

    # Expecting move number from file to match the count being kept.
    # Do the check. Do they match?
    if Game.move_count != move_number:
        expected_move_number_not_found()
        return False

    # Skip the move number and determine the Chess Move
    # That is, parse any periods and whitespace; then parse the Chess Move
    Game.input_stream = Game.input_stream[matched.end(0):]

    #                             r"\A[.][ \n]*"
    Game.input_stream = constants.move_number_suffix_pattern.sub(
                                                "",
                                                Game.input_stream,
                                                count=1)

    # Handle any comments
    # If empty don't continue
    # Note: the order of this 'or' expression is significant
    # Call regexp_loop first!
    if not regexp_loop() or Game.input_stream == "":
        return False

    # is it "1-0" (White wins), "0-1" (Black wins),
    #       "1/2-1/2" (drawn game), OR "*"
    if check_game_termination_marker_found():
        return False

    # Otherwise since not a move number,
    # Expecting to parse a chess move
    return parse_chess_move(chess)


def find_the_match(chess, all_matched_list,
                   to_file, to_rank, piece):
    """
    Go through each filtered square
    Regarding the piece on the square
    generate all the possible moves for this piece
    Find the move with the matching 'target' destination
    """

    found_target = None

    for index in all_matched_list:
        from_file = index[0]
        from_rank = index[1]
        all_the_moves = e.movelist(chess, from_file, from_rank,
                                   Game.global_piece_sign, False)

        for m in range(len(all_the_moves)):
            target_file = all_the_moves[m][0]
            target_rank = all_the_moves[m][1]
            if target_file == to_file and target_rank == to_rank:
                found_target = all_the_moves[m]
                break

        if found_target:
            break

    if not found_target:
        """
        This ought not to happen!
        It means: An invalid move
        has been read in from the input file
        """
        chess.display("Invalid Move")
        e.input_status_message(constants.BAD_CHESS_MOVE_FROMFILE
                               + Game.input_stream_previous_contents)
        return  # Failure

    # Match found
    # Retrieve the new values
    Game.new_from_file = from_file
    Game.new_from_rank = from_rank
    Game.new_to_file = to_file
    Game.new_to_rank = to_rank
    Game.en_passant_status = constants.NOVALUE

    if piece == "P":
        Game.output_chess_move = ""
    else:
        Game.output_chess_move = piece

    Game.output_chess_move += found_target
    return  # Success


def determine_the_move(chess, piece, to_square):
    """
    Use 'piece' and 'to_square' to determine what the 'from' square is
    """

    to_file = to_square[0]
    to_rank = to_square[1]

    # Filter all the squares where both the colour and the piece match
    all_matched_list = [index for index in constants.PRESET_CHESSBOARD
                        if chess.piece_sign(index) == Game.global_piece_sign
                        and chess.piece_letter(index) == piece]

    # Go through each filtered square,
    # generated all the moves for the piece on a filtered square
    # and find the move with the matching 'target' destination

    find_the_match(chess, all_matched_list,
                   to_file, to_rank, piece)


def determine_the_capture_by_file(chess, piece, from_file, to_square):
    """
    Use 'piece', 'from_file' and 'to_square'
    to determine what the 'from' rank is
    """

    to_file = to_square[0]
    to_rank = to_square[1]

    # Filter all the squares where
    # The file, the colour and the piece all match
    all_matched_list = [index for index in constants.PRESET_CHESSBOARD
                        if index[0] == from_file
                        and chess.piece_sign(index) == Game.global_piece_sign
                        and chess.piece_letter(index) == piece]

    # Go through each filtered square,
    # generated all the moves for the piece on a filtered square
    # and find the move with the matching 'target' destination

    find_the_match(chess, all_matched_list,
                   to_file, to_rank, piece)


def determine_the_capture_by_rank(chess, piece, from_rank, to_square):
    """
    Use 'piece', 'from_rank' and 'to_square'
    to determine what the 'from' file is
    """

    to_file = to_square[0]
    to_rank = to_square[1]

    # Filter all the squares where
    # The rank, the colour and the piece all match
    all_matched_list = [index for index in constants.PRESET_CHESSBOARD
                        if index[1] == from_rank
                        and chess.piece_sign(index) == Game.global_piece_sign
                        and chess.piece_letter(index) == piece]

    # Go through each filtered square,
    # generated all the moves for the piece on a filtered square
    # and find the move with the matching 'target' destination

    find_the_match(chess, all_matched_list,
                   to_file, to_rank, piece)


def determine_the_capture_by_both_squares(chess,
                                          piece, from_square, to_square):
    """
    Use 'piece', 'from_square' and 'to_square'
    Check that the move is possible for this piece
    """

    if not (chess.piece_sign(from_square) == Game.global_piece_sign
            and chess.piece_letter(from_square) == piece
            and from_square in constants.PRESET_CHESSBOARD
            and to_square in constants.PRESET_CHESSBOARD):
        """
        This ought not to happen!
        It means: An illegal move or invalid move
        has been read in from the input file
        """
        chess.display("Invalid Long Notation Move")
        e.input_status_message(constants.BAD_CHESS_MOVE_FROMFILE
                               + Game.input_stream_previous_contents)
        return  # Failure

    to_file = to_square[0]
    to_rank = to_square[1]

    # generated all the moves for the piece on 'from_square'
    # and find the move with the matching 'target' destination

    find_the_match(chess, [from_square],
                   to_file, to_rank, piece)


def determine_move_both_file_rank(chess):
    """
    Standard Algebraic Notation (SAN) suppresses redundant information
    concerning the from-square,
    while keeping the descriptive letter or symbol of pieces other than a pawn.
    In other words, it is a shortened algebraic notation of chess moves.

    https://www.chessprogramming.org/
    Algebraic_Chess_Notation#Standard_Algebraic_Notation_.28SAN.29

    https://en.wikipedia.org/wiki/Algebraic_notation_(chess)

    Therefore, conversion takes place. In order to convert SAN chess moves into
    Long Algebraic Notation (LAN) so that the origin and target coordinates
    can be used by this program to interpret the chess move.

    Therefore:
    Determine the full chess move, both file and rank
    For example, change 'e4' to 'e2e4'; change 'Nf3' to 'g1f3'; etc
    This is needed in order for this program to play the move.

    'Game.chess_move_tuple' consists of (piece, source, target)

    Note: If the resultant move that has been read
          from the input file is an En Passant move.
          Then this move is performed 'at this stage'
          within the functionality of 'determine_move_both_file_rank'
    """

    (piece, source, target) = Game.chess_move_tuple

    # Depending on the 'move_type' check whether
    # an En Passant move is possible
    # And if so, perform the move at this point
    if (Game.move_type == constants.PAWN_CAPTURE_FILE
       or Game.move_type == constants.LONG_NOTATION
       or Game.move_type == constants.PIECE_BOTH_SQUARES):
        # Game.en_passant_status is
        # set to either constants.VALID for a valid En Passant move
        #  or to 'constants.INVALID' for an illegal En Passant move
        result = m.check_if_inputfile_move_is_en_passant(chess, source, target)

        """
        There are three possible outcomes

        1) If 'result' is True then an En Passant move has been performed

        2) Otherwise check Game.en_passant_status
        If it is equal to constants.INVALID
        then an attempted En Passant took place
        which turned out to be illegal

        3) Otherwise the move was not an En Passant move at all
        Proceed with determining the full chess move, both file and rank
        """

        if result:
            return  # Successful En Passant move

        if Game.en_passant_status == constants.INVALID:
            return  # Unsuccessful En Passant move

        # Otherwise not an En Passant move - Continue

    if piece == "":  # PAWN
        piece = "P"

    if (Game.move_type == constants.DESTINATION_SQUARE_ONLY
       or Game.move_type == constants.PIECE_DESTINATION_SQUARE):
        # DESTINATION_SQUARE_ONLY  EG h3 OR Ne2
        # PIECE_DESTINATION_SQUARE EG Qxe1
        determine_the_move(chess, piece, target)
        return

    elif (Game.move_type == constants.PAWN_CAPTURE_FILE
          or Game.move_type == constants.PIECE_FILE_MOVE):
        # PAWN_CAPTURE_FILE EG exd4
        # PIECE_FILE_MOVE   EG Nfxe4, Rac1
        determine_the_capture_by_file(chess, piece, source, target)
        return

    elif Game.move_type == constants.PIECE_RANK_MOVE:
        # EG N6xe4
        determine_the_capture_by_rank(chess, piece, source, target)
        return

    elif (Game.move_type == constants.PIECE_BOTH_SQUARES
          or Game.move_type == constants.LONG_NOTATION):
        # PIECE_BOTH_SQUARES EG Nd2xe4 e5xf6
        # LONG_NOTATION EG Ng1f3
        determine_the_capture_by_both_squares(chess,
                                              piece, source, target)
        return

    else:
        # Defensive Programming
        raise CustomException(("Internal Error: Unknown Move Type {}")
                              .format(Game.move_type))


def handle_move_text(chess):
    """
    At this point, looking at either
    a Move Number or a Chess Move EG 1. OR e2e4
    Parse accordingly
    If it is a Chess Move and the Parsing operation was successful,
    'Game.general_string_result' would be set to
    the value of the matched 'chess move string'
    """

    result = parse_move_text(chess)
    # Alternate the players for the next time; that is, negate the sign
    Game.whose_move = -Game.whose_move

    # Was the parsing successful?
    if not result:
        # No!
        return

    # Yes!
    if Game.move_type == constants.CASTLING_MOVE:
        return

    # Determine the full chess move, both file and rank
    # Note: If the resultant move is an En Passant move
    #       Then this move is performed at this stage
    #       within the functionality of 'determine_move_both_file_rank'

    #       Game.en_passant_status would be:
    #           set to 'constants.VALID' for a valid En Passant move
    #           set to 'constants.INVALID' for an illegal En Passant move
    #           set to 'constants.NOVALUE' for a non-en-passant move

    determine_move_both_file_rank(chess)


def fetch_chess_move_from_file(chess):
    """
    Read a chess move from the input file stream and parse it
    Note: the order of this 'or' expression is significant
    Call regexp_loop first!
    """
    if not regexp_loop() or Game.input_stream == "":
        # Empty or Erroneous input
        return

    # Must be the movetext section.
    # The movetext section is composed of chess moves, move number indications,
    # comments, optional annotations
    # and a single concluding game termination marker.

    # is it "1-0" (White wins), "0-1" (Black wins),
    # "1/2-1/2" (drawn game), OR "*"
    if check_game_termination_marker_found():
        return

    # Could be either a Move Number or a Chess Piece
    handle_move_text(chess)


def handle_player_move_from_inputfile(chess,
                                      from_file, from_rank, to_file, to_rank):
    """
    For testing purposes Chess moves are read from an input file
    Therefore, if this option is ON
    Fetch the Player's next move from the input file's stream
    """

    # Default: 'pass' as in Python i.e. NOP
    do_next = "pass"
    if not Game.reading_game_file:
        # No File Handling. Fetch the chess move from the user
        # from the keyboard i.e. 'pass'
        return do_next

    # File Input ... Continue
    # Ensure that these are set correctly
    # PLAYER'S MOVE against COMPUTER
    Game.who_are_you = constants.PLAYER
    Game.opponent_who_are_you = constants.COMPUTER

    fetch_chess_move_from_file(chess)

    # Was there a file input issue?
    # If so, appropriate error messaging has been displayed
    # Pause the computer so that the Player can read it
    # From this point, fetch user's input from keyboard

    if not Game.reading_game_file:
        sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)
        return do_next  # 'pass'

    # Was a Castling move read from the file? If so, process it
    if Game.reading_game_file and Game.move_type == constants.CASTLING_MOVE:
        just_performed_castling = m.perform_castling(chess, constants.PLAYER)

        if not just_performed_castling:
            # The Castling that was read from the input file was invalid!
            # 'perform_castling() redisplays the Board
            # and displays the appropriate error messaging
            # Pause the computer so that the Player can read it
            # No further moves are read from the input file;
            # rather fetch moves from the user
            e.is_error_from_input_file()
            print()
            sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)
            do_next = "continue"
            return do_next

        # The Castling Move that was read from the input file was valid!
        m.castling_move_was_valid(chess)
        # Pause the computer so that the Player can read the move
        sleep(constants.CASTLING_EP_SLEEP_VALUE)
        do_next = "return"
        return do_next

    # Otherwise 'pass'
    return do_next


def pause_for_display():
    """
    Pause the computer so that the Player can read what has been displayed
    """
    if Game.it_is_checkmate:
        # Messaging already displayed and Paused
        return

    if Game.reading_game_file:
        sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)
    else:
        sleep(constants.CASTLING_EP_SLEEP_VALUE)


def handle_computer_move_from_inputfile(chess,
                                        from_file, from_rank,
                                        to_file, to_rank):
    """
    For testing purposes Chess moves are read from an input file
    Therefore, if this option is ON
    Fetch the Computer's next move from the input file's stream
    The Chess Move being read from the input file always has priority
    over the Chess Move generated from 'evaluate'
    """

    # Ensure that these are set correctly
    # COMPUTER'S MOVE against PLAYER
    Game.who_are_you = constants.COMPUTER
    Game.opponent_who_are_you = constants.PLAYER

    fetch_chess_move_from_file(chess)

    # Was there a file input issue?
    # If so, appropriate error messaging has been displayed
    # Pause the computer so that the Player can read it
    # Use the values that were previously generated by 'evaluate'
    # i.e. from_file, from_rank, to_file, to_rank

    if not Game.reading_game_file:
        sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)
        return (False, from_file, from_rank, to_file, to_rank)

    # No file input issue ... Continue
    # Was the move a Castling Move?
    if Game.move_type == constants.CASTLING_MOVE:
        # A Castling Move has been read from the file - process it
        just_performed_castling = m.perform_castling(chess, constants.COMPUTER)
        if not just_performed_castling:
            # The Castling that was read from the input file was invalid!
            # 'perform_castling() redisplays the Board
            # and displays the appropriate error messaging
            # Pause the computer so that the Player can read it
            # No further moves are read from the input file;
            # rather fetch moves from the user
            print("Computer from this point onwards "
                  "will now generate its own moves")
            e.is_error_from_input_file()
            print()
            sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)
            return (False, from_file, from_rank, to_file, to_rank)

        else:
            # The Castling that was read from the input file was valid!
            # Castling Validation has already been done
            # to see whether Castling would put the Player in Check
            # 'indicate_castling_done()' displayed the appropriate messaging
            # regarding the Castling move

            # Since this chess move is not a pawn that has advanced two squares
            # Ensure that previous values for 'Computer' have been reset

            m.reset_2squares_pawn_positions(constants.COMPUTER)
            finalise_computer_move(chess, True)
            pause_for_display()
            computer_move_finalised = True

            return (computer_move_finalised,
                    from_file, from_rank, to_file, to_rank)

    # Was the move a En Passant Move?
    # If so, was it valid?
    if Game.en_passant_status == constants.INVALID:
        # The En Passant that was read from the input file was invalid!
        # 'perform_en_passant() redisplays the Board
        # and displays the appropriate error messaging
        # Pause the computer so that the Player can read it
        print("Computer from this point onwards "
              "will now generate its own moves")
        print()
        sleep(constants.COMPUTER_FILEIO_SLEEP_VALUE)
        return (False, from_file, from_rank, to_file, to_rank)

    if Game.en_passant_status == constants.VALID:
        # The En Passant that was read from the input file was valid!
        # En Pasant Validation has already been done
        # to see whether this En Passant move would put the Player in Check
        # 'indicate_en_passant_done()' displays the appropriate messaging
        # regarding the En Pasant move
        # Previous values regarding 'Computer's pawn positions'
        # have already been reset

        # Convert the chess move in order to output it
        # Add a 'x' to the output chess move if a piece was taken
        # Add the promoted piece if a promotion took place
        # Then output the piece to the output file
        # Use the new En Passant coordinates Game.new_...
        m.setup_output_chess_move_add_promotion(constants.PAWN_LETTER,
                                                Game.new_from_file,
                                                Game.new_from_rank,
                                                Game.new_to_file,
                                                Game.new_to_rank,
                                                constants.PAWN_VALUE)

        finalise_computer_move(chess, False)
        pause_for_display()
        computer_move_finalised = True
        return (computer_move_finalised,
                None, None, None, None)

    # Not a Castling move therefore,
    # Fetch new values for 'from_file,from_rank,to_file,to_rank'
    # from what was read in the input game file
    Game.en_passant_status = constants.NOVALUE
    return (False,
            Game.new_from_file, Game.new_from_rank,
            Game.new_to_file, Game.new_to_rank)
