"""
fileio.py
For testing purposes I decided to read Chess moves from an input file
So this file contains all the routines related to reading chess moves from a file
and their validation.
"""

import constants
from game import Game
from extra import append_to_output_stream, output_attacking_move
from time import sleep


def output_message(message):
    """
    Output a message after first removing any superfluous blank lines
    """
    lines = message.splitlines()
    # Based on 
    # https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
    stripped = [line.strip() for line in lines if line.strip()]

    if not stripped:
        # Print a blank line
        print()
        return

    for m in stripped:
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
    Display a general message if an erroneous chess move came from the input file
    """
    if Game.reading_game_file:
        input_status_message("Since This Illegal Move came from the input file\n"
                             "moves will hereafter come from your input via the keyboard")


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
    regexp = r"[\x00-\x08\x0B-\x1F\x7F-\xFF]"
    work_string = re.sub(regexp, "", work_string)

# Replace any horizontal tabs with spaces
    work_string = work_string.replace(constants.TAB, constants.SPACE)

# Trim and ensure there is an extra \n at the end, if not null
    work_string = work_string.strip(work_string, " \n")
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
    if not position:
        astring = "Found " + open_char + " however cannot determine where " + close_char + " ends"
        input_status_message(astring)
        return False

    Game.input_stream = Game.input_stream[position + 1:]
    return True


def ignore_rav():
    """
    Remove everything between the parentheses
    Including the parentheses
    Note: the parentheses can be nested
    """
    
    count = 1  # Found the first parenthesis
    position = 1  # So start the search to the right of it
    while True:
        # r"[()]"
        matched = constants.parens_pattern.search(Game.input_stream, position)
        if not matched:
            break

        elif matched.group(0)== LPAREN:
            count += 1
            position += 1
            continue

        else:  # must be the right parenthesis
            count -= 1
            if count == 0:
            # Found the matching RAV ( ... ) - remove it
                Game.input_stream = Game.input_stream[matched.end(0) + 1:]
                return True

            position += 1
            continue

    # No closing parenthesis found
    return False


def open_input_file():
    """
    The file 'input.pgn' will be used to hold 
    Chess 'Movetext in PGN format' for testing purposes
    Open this file and read its contents
    If this is an IOError e.g. the file does not exist; 
    or the file is empty,
    Set file_contents and input_stream to ""
    """
    LPAREN = "("
    RPAREN = ")"
    LBRACKET = "["
    RBRACKET = "]"
    OA_BRACKET = "<"  # open angled bracket
    CA_BRACKET = ">"  # close angled bracket

    Game.input_stream = ""

    try:
        with open(constants.INPUT_PGN_NAME) as pgn_input_file:
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
        input_status_message(f"Input file too big - larger than {constants.FILE_SIZE_LIMIT} characters")
        return

    Game.input_stream = cleanup_input_stream(file_contents)
    if len(Game.input_stream) == 0:
        # Null string i.e. Empty file contents
        Game.reading_game_file = False
        # Game.input_stream already set to ""


def regexp_loop():
    """
    Parse the input stream
    Remove any comments and annotations which are part of the PGN file notation
    This will loop until a potential chess move string is found 
    or end of string
    """

    while True:

# Remove any spaces
        Game.input_stream = Game.input_stream.lstrip()
        if len(Game.input_stream) == 0:
            input_status_message(f"No further input available from '{constants.INPUT_PGN_NAME}'")
            return True

        # % Escape mechanism - This mechanism is triggered
        # by a percent sign character ("%") appearing in the first column of a line;
        # the data on the rest of the line is ignored up to the next \n

        # r"(\A%)|(\n%)"
        matched = constants.percent_pattern.match(Game.input_stream)
        if matched:
            # The length is either 1 or 2 - the correct starting position for the 'find'
            position = Game.input_stream.find("\n",length(matched.group(0)))
            if position < 0:  # No \n found - therefore remove entire contents
                Game.input_stream = ""
                continue

# Remove everything up to and including the \n
            Game.input_stream = Game.input_stream[position + 1:]
            continue

# Remove any leading whitespace i.e. including \n
        Game.input_stream = Game.input_stream.lstrip(" \n\t")
        if len(Game.input_stream) == 0:
            input_status_message(f"No further input available from '{constants.INPUT_PGN_NAME}'")
            return True

        # Just in case any found - remove an 'en passant' annotation, that is 'e.p.'
        # r"\Ae\.p\.[ \n]*"
        Game.input_stream = constants.en_passant_pattern.sub("", Game.input_stream, count=1)

        firstchar = Game.input_stream[0:1]

# Comment text may appear in PGN data. There are two kinds of comments.
# The first kind is the "rest of line" comment; this comment type starts with a
# semicolon character and continues to the end of the line.  The second kind
# starts with a left brace character and continues to the next right brace
# character.

        if firstchar == ";":
            # Ignore up to the end of the line
            position = Game.input_stream.find("\n")
            if position < 0:  # No \n found - therefore remove entire contents
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
        # Ignore up to and including the following right close angled bracket
            position = ignore_group_comment(OA_BRACKET, CA_BRACKET)
            if not position:
                return False
            else:
                continue

        elif firstchar == constants.LPAREN:  # I.E. LEFT PARENTHESIS
        # An RAV (Recursive Annotation Variation) is a sequence of movetext containing
        # one or more moves enclosed in parentheses.
        # Because the RAV is a recursive construct, it may be nested.
        # Ignore up to and including the corresponding right nested parenthesis

            position = ignore_rav()
            if not position:
                return False
            else:
                continue

        elif firstchar == "$":  # I.E. $nnn
        # An NAG (Numeric Annotation Glyph) is a movetext element that is used to
        # indicate a simple annotation in a language independent manner.  An NAG is
        # formed from a dollar sign ("$") with a non-negative decimal integer suffix

            # r"\A\$[0-9]+"
            matched = constants.percent_pattern.match(Game.input_stream)
            if matched:
                # Ignore $nnn
                Game.input_stream = Game.input_stream[len(matched.group(0)):]
                continue

            input_status_message("Cannot determine this NAG: " + Game.input_stream[0:6])
            return False

        else:
# Either Move Number, a Chess Move or no more data
            return True


def handle_move_suffix(matched):

    """
    Skip over the 'matched' string
    Remove any trailing symbol continuation characters.
    These continuation characters are letter characters ("A-Za-z"), digit characters ("0-9"),
    the plus sign ("+"), the octothorpe sign ("#"),
    the equal sign ("="), the colon (":"),  and the hyphen ("-").
    Therefore ignore suffix text such as =Q+
    """

    Game.input_stream = Game.input_stream[len(matched.group(0)):]
    # r"\A[A-Za-z0-9+#=:\-]*"
    Game.input_stream = constants.chess_move_suffix_pattern.sub("", Game.input_stream, count=1)


def triple_tuple(matched):
    """
    For example: 
    (the piece, the source square, the destination square)
    Fetch the matched string and create the tuple
    """

    Game.general_string_result = matched.group(0)
    #                             PIECE             FROM              TO
    Game.chess_move_tuple = tuple(matched.group(1), matched.group(2), matched.group(3))
    handle_move_suffix(matched)


def double_tuple(matched):
    """
    For example: 
    (the piece, the destination square)
    Fetch the matched string and create the tuple
    Add a null item to make the tuple a length of 3
    """

    Game.general_string_result = matched.group(0)
    #                             PIECE            FROM TO
    Game.chess_move_tuple = tuple(matched.group(1), "", matched.group(2))
    handle_move_suffix(matched)


def parse_chess_move():
    """
    Parse the chess move into a tuple
    Place the tuple into Game.chess_move_tuple
    Place the string result into Game.general_string_result
    Note: the order of these regular expression patterns is significant
    """

    print(">" + Game.input_stream[0:20])  # todo

    inputstream_previous_contents = Game.input_stream[0:20]

    # EIGHT REGEXPS

    """
    7)
    A)
    print("NO7>> " + Game.input_stream)  # todo

    *** NON-AMBIGUOUS LONG NOTATION SHOWING PIECE & COORDINATES OF BOTH PIECES ***
    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED BY BOTH two character square coordinates ***
    EG Ng1f3 e2e4
    An En Passant move could be of this format
    tuple format: (the piece, the source square, the destination square)
    """

    # r"\A([KQRBN]?)([a-h][1-8])([a-h][1-8])
    matched = constants.long_notation_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the source square, the destination square
        Game.move_type = constants.LONG_NOTATION
        triple_tuple(matched)
        return True  # Indicate success

    """
    6)
    B)

    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED BY BOTH two character square coordinates ***
    EG Nd2xe4  e4xd5
    An En Passant move could be of this format
    tuple format: (the piece, the source square, the destination square)
    """

    # r"\A([KQRBN]?)([a-h][1-8])x([a-h][1-8])"
    matched = constants.capture_2squares_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the source square, the destination square
        Game.move_type = constants.PIECE_BOTH_SQUARES
        triple_tuple(matched)
        return True  # Indicate success

    """
    1)
    C)

    *** HANDLE e4 Ng2 ***
    Note: This program does NOT support En Passant captures of the form EG d6
    En Passant captures must contain a 'from_file' EG exd6
    tuple format: (the piece optional , the destination square)
    """

    # r"\A([KQRBN]?)([a-h][1-8])"
    matched = constants.one_square_pattern.match(Game.input_stream)
    if matched:
        # That is, just piece and the destination square only
        Game.move_type = constants.DESTINATION_SQUARE_ONLY
        double_tuple(matched)
        return True  # Indicate success

    """
    2)
    D)

    *** HANDLE PAWN CAPTURES USING 'file' EG exd4 ***
    EG exd4
    An En Passant move could be of this format
    tuple format: (the file , the destination square)
    """

    # r"\A([a-h])x?([a-h][1-8])"
    matched = constants.pawn_capture_pattern.match(Game.input_stream)
    if matched:
        # That is, just the file and the destination square only
        Game.move_type = constants.PAWN_CAPTURE_FILE
        double_tuple(matched)
        return True  # Indicate success

    """
    3)
    E)

    *** HANDLE CAPTURES REGARDING OTHER PIECES EG Qxd4 ***
    No possibility of an En Passant move in this format
    tuple format: (the piece, the destination square)
    """

    # r"\A([KQRBN])x([a-h][1-8])"
    matched = constants.nonpawn_capture_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece and the destination square
        # EG Qxe1 Kxf7 Rxe1+
        Game.move_type = constants.PIECE_DESTINATION_SQUARE
        double_tuple(matched)
        return True  # Indicate success

    """
    4)
    F)

    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED BY THEIR 'file' ***
    EG Nge2  - THE FILE BEING 'g'
    EG Nfxe4 - THE FILE BEING 'f'

    This pattern does not apply to Pawns
    Therefore, no possibility of an En Passant move in this format
    tuple format: (the piece, the file, the destination square)
    """

    # r"\A([KQRBN])([a-h])x?([a-h][1-8])
    matched = constants.file_pattern.match(Game.input_stream)
    if matched:
        # That is, the piece, the file and the destination square
        Game.move_type = constants.PIECE_FILE_MOVE
        triple_tuple(matched)
        return True  # Indicate success

    """
    5)
    G)

    *** HANDLE MOVES/CAPTURES REGARDING PIECES DETERMINED BY THEIR 'rank' ***
    EG N2d4  - THE RANK BEING '2'
    EG N6xe4 - THE FILE BEING 'G'

    This pattern does not apply to Pawns
    Therefore, no possibility of an En Passant move in this format
    tuple format: (the piece, the rank, the destination square)
    """

    # r"\A([KQRBN])([1-8])x?([a-h][1-8])
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

    # r"\A((O-O-O)|(O-O)|(0-0-0)|(0-0))"
    matched = constants.castling_inputfile_pattern(Game.input_stream)
    if matched:
        Game.move_type = constants.CASTLING_MOVE
        Game.general_string_result = matched.group(0)
        handle_move_suffix(matched)
        print("OO>", Game.general_string_result, position, length)  # todo
        return True  # Indicate success

# Unknown Chess Move
    input_status_message(constants.BAD_CHESS_MOVE_FROM_FILE 
                         + Game.input_stream[0:20])
    return False # Indicate failure


def check_game_termination_marker_found():
    """
    Determine if the parsed string is
    # is it "1-0" (White wins), "0-1" (Black wins), "1/2-1/2" (drawn game), OR "*"
    """

    result = False
    # r"\A((1-0)|(0-1)|(1/2-1/2)|[*])"'
    matched = constants.move_number_pattern.match(Game.input_stream)
    if matched:
    # Reached the Indicator regarding the Result and the End of the Game
        input_status_message("Result of the Game has been read from the input file: "
                             + matched.group(0))
        result = True

# Remove it from the input stream
        Game.input_stream = Game.input_stream[len(matched.group(0)):]

    return result


def expected_move_number_not_found():
    """
    Report that an expected move number could not be determined
    """

    input_status_message("Expected Move Number " + str(Game.move_count)
                         + ". Instead: " + Game.input_stream[0:10])


def parse_move_text():
    """
    Parse the text into a tuple of the following form:
    (the piece optional, the destination square)
    The result is placed in Game.general_string_result
    TODO
    """

    if Game.whose_move == constants.COMPUTER:
        Game.global_piece_sign = constants.COMPUTER
        # For parsing a Computer's move, check that it is not a string of periods e.g. ...
        # r"\A[.]+"
        matched = constants.periods_pattern.match(Game.input_stream)
        if matched:
            input_status_message("Expected the Player's Chess Move not Periods: "
                                 + Game.input_stream[0:10])
            return False
            
        # Otherwise    
        return parse_chess_move()

    # Therefore Game.whose_move is == constants.PLAYER
    # Increment the Move Counter
    global_piece_sign = constants.PLAYER
    Game.move_count += 1
    Game.move_count_incremented = True

    # Output the Move Number
    append_to_output_stream(str(Game.move_count) + "." + constants.SPACE)

    # Move Number expected EG '4.' I will allow periods to be optional
    matched = constants.move_number_pattern.match(Game.input_stream)
    if not matched:
        expected_move_number_not_found()
        return False

    # Determine the move number that was read by conversion

    try:
        move_number = int(matched(0))
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
    
    # r"\A[.][ \n]*"
    Game.input_stream = constants.move_number_suffix_pattern.sub("", Game.input_stream, count=1)

    # Handle any comments
    # If empty don't continue
    if Game.input_stream == "" or not regexp_loop():
        return False

    # is it "1-0" (White wins), "0-1" (Black wins), "1/2-1/2" (drawn game), OR "*"
    if check_game_termination_marker_found():
        return False

    # Otherwise
    return parse_chess_move()


def check_for_en_passant_first(chess, source, target):
    """
    Whilst trying to identify the chess move
    that was read from an input file
    Firstly, check whether it is an en passant move?
    """

    target_file = target[0]  # EG 'E' for 'E6' ' TODO need a dest
    target_rank = target[1]  # EG '6' for 'E6'
    source_file = source[0]

    is_it_an_en_passant_move = validate_and_perform_en_passant(chess, source_file, constants.NOVALUE, target_file, target_rank)
    if is_it_an_en_passant_move:
    # Valid en passant move has been performed
        return True  # Successful en passant move

    if Game.en_passant_status == constants.INVALID:
    # Illegal En Passant Move has been determined
        if g_message_printed:
            # Hopefully Doubtful!
            pass
        else:
            input_status_message(constants.BAD_EN_PASSANT_FROM_FILE + inputstream_previous_contents)
            g_message_printed = True

        return

    # This chess move is not an en passa
    return


def determine_the_move(chess, piece, to_square):
    """
    Using 'piece' and 'to_square' to determine what the 'from' square is
    """

    to_file = to_square[0]
    to_rank = to_square[1]

    # Filter all the squares where both the colour and the piece match
    same_colour_pieces_list = [index for index in constants.PRESET_CHESSBOARD
                               if chess.piece_sign(index) == Game.global_piece_sign
                                  and chess.piece_letter(index) == piece]

    # Go through each filtered square, 
    # generated all the moves for the matching piece 
    # and find the move with the matching 'target' destination
    for index in same_colour_pieces_list:
        from_file = index[0]
        from_rank = index[1]
        all_the_moves = movelist(chess, from_file, from_rank,
                                 Game.global_piece_sign, False)

        found_target = None

        for m in all_the_moves:
            target_file = all_the_moves[m][0]
            target_rank = all_the_moves[m][1]
            if target_file == to_file and target_rank == to_rank:
                found_target = all_the_moves[m]
                # todo
                print("MATCH", from_file, from_rank, to_file, to_rank)
                break

        if found_target:
           break

    if not found_target:
        """
        This ought not to happen! 
        It means: An illegal move or invalid move has been read in from the input file    
        The erroneous text/input is in Game.general_string_result
        """
        input_status_message(constants.BAD_CHESS_MOVE_FROM_FILE + inputstream_previous_contents)
        return # Failure

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

    # todo
    print("ANSWER1",Game.new_from_file, Game.new_from_rank, Game.new_to_file, Game.new_to_rank, Game.output_chess_move)

    return # Success


def determine_the_capture_by_file(chess, piece, from_file, to_square):
    """
    Using 'piece', 'from_file' and 'to_square'
    to determine what the 'from' square is
    """

    # Filter all the squares where
    # The file, the colour and the piece all match
    all_matches_list = [index for index in constants.PRESET_CHESSBOARD
                               if index[0] == from_file
                                  and chess.piece_sign(index) == Game.global_piece_sign
                                  and chess.piece_letter(index) == piece]

    found = False

        FOR target_y = 7 TO 0 STEP - 1
# BOTH THE COLOUR AND THE PIECE MUST MATCH!
            if bsign(file_x, target_y) == global_piece_sign and bpiece(file_x, target_y) == ascii_piece:
                movelist(file_x, target_y, global_piece_sign, False)
                FOR m = 0 TO num_moves
# FIRST ENTRY ONLY SO USE THE NUMBER 1 AS OPPOSED TO THE VARIABLE level
                    if destination_x == movex(m, 1) and destination_y == movey(m, 1):

# debugging
# PRINT "MATCH2", file_x, target_y, destination_x, destination_y

                            found = True
                            break


                if found:
                    break


# THIS MUST BE DONE
    level = 0

    if not found:
#        PRINT "INTERNAL ERROR 4: NO MATCH FOUND"
#        PRINT piece, file, destination, file_x, target_y, destination_x, destination_y, global_piece_sign
#        console_input = WAITKEY$
#        END

# The erroneous text/input is in Game.general_string_result

         input_status_message(constants.BAD_CHESS_MOVE_FROM_FILE + inputstream_previous_contents)
         return


# REFACTOR

    Game.new_from_file = file_x
    Game.new_from_rank = target_y
    Game.new_to_file = destination_x
    Game.new_to_rank = destination_y
    g_en_passant_status = constants.NOVALUE

    if piece == "P":
        output_chess_move = ""
    else:
        output_chess_move = piece


    output_chess_move = output_chess_move + convert_indices_to_file_rank(Game.new_from_file, Game.new_from_rank, Game.new_to_file, Game.new_to_rank)

# debugging
# PRINT "ANSWER2",Game.new_from_file, Game.new_from_rank, Game.new_to_file, Game.new_to_rank, output_chess_move

# PRINT "OS2>",output_stream

# THIS MUST BE DONE
# level = 0 - SEE ABOVE

    determine_the_capture_by_file = True  # Success


def determine_move_both_file_rank(chess):
    """
    Since SAN is shortened i.e. short algebraic notation
    https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
    Determine the full chess move, both file and rank
    For example, change 'e4' to 'e2e4'; change 'Nf3' to 'g1f3'
    This is needed in order for this program to play the move

    Game.chess_move_tuple consists of (piece, source, target)
    """

    (piece, source, target) = Game.chess_move_tuple

    # Depending on the 'move_type' check whether 
    # an en passant move is possible
    # And if so, perform it
    if (Game.move_type == constants.PAWN_CAPTURE_FILE)
        result = check_for_en_passant_first(chess, source, target)
        
        """
        There are three possible outcomes

        1) If 'result' is True then an en passant move has been performed

        2) Otherwise check Game.en_passant_status
        If it is equal to constants.INVALID then an attempted en passant took place
        which turned out to be illegal

        3) Otherwise the move was not an en passant move at all
        Proceed with determining the full move
        # TODO
        """

        if (result)
            return # Successful en passant move
    
        if g_en_passant_status == constants.INVALID:
            return 

        # Therefore not an en passant move - Continue

    if piece == "":  # PAWN
        piece = "P"


    if (Game.move_type == constants.DESTINATION_SQUARE_ONLY
       or constants.PIECE_DESTINATION_SQUARE)
       # DESTINATION_SQUARE_ONLY EG e4 OR Ne2
       # PIECE_DESTINATION_SQUARE EG Qxe1
        return determine_the_move(chess, piece, target)

    if Game.move_type == constants.PAWN_CAPTURE_FILE
        # EG exd4
        return determine_the_capture_by_file(chess, piece, source, target)


def handle_move_text(chess):
    """
    At this pointing looking at either 
    a Move Number or a Chess Piece EG 1. OR e2e4
    Parse accordingly
    If the Parsing operation was successful
    Game.general_string_result would be set to 
    the value of the matched 'chess move string'
    Determine the full chess move, both file and rank
    """

    result = parse_move_text()
    # Alternate the players for the next time; that is, negate the sign
    Game.whose_move = -Game.whose_move

    # Was the parsing successful?
    if not result:
    # No!       
        return

    # Yes! 
    print("BEFORE1", Game.reading_game_file)
    # TODO
    result = determine_move_both_file_rank(chess)
    print("test result", Game.reading_game_file, result)  # todo
    # todo RESULT NOT NEEDED TODO SUB NOT FUNCTION


def fetch_chess_move_from_file(chess):
    """
    Read a chess move from the input file stream and parse it
    """
    if Game.input_stream == "" or not regexp_loop():
        # Empty or Erroneous input
        return

    # Must be the movetext section.
    # The movetext section is composed of chess moves, move number indications, comments,
    # optional annotations, and a single concluding game termination marker.

    # is it "1-0" (White wins), "0-1" (Black wins), "1/2-1/2" (drawn game), OR "*"
    if check_game_termination_marker_found():
        return

    # Could be either a Move Number or a Chess Piece

    handle_move_text(chess)
