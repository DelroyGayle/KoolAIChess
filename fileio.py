"""
For testing purposes I decided to read Chess moves from an input file
So this file contains all the routines related to reading chess moves from a file
and their validation.
"""

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
            input_status_message(f"No further data available from '{constants.INPUT_PGN_NAME}'")
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
            input_status_message(f"No further data available from '{constants.INPUT_PGN_NAME}'")
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


def parse_move_text():

    parse_move_text = False

    if Game.whose_move == constants.PLAYER:

# Increment the Move Counter
        global_piece_sign = constants.PLAYER
        g_move_count+=1
        g_move_count_incremented = True

# Output the Move Number
        append_to_output(lstrip(str(g_move_count)) + "." + constants.SPACE)

# Move Number expected EG 40. I will allow periods to be optional
        regexp = "^[0-9]+[. ]+"
        REGEXPR regexp IN Game.input_stream TO position, length
# Cater for how PBasic handles ^
        if position != 1:
            input_status_message("Expected Move Number" + str(g_move_count) + ". Instead: " + Game.input_stream[0:10])
            return


# Expecting matching move number

# Determine the move number
# PRINT VAL("10."), VAL("10..") ==>  10 10

        move_number = VAL(Game.input_stream[0:length])

        if g_move_count != move_number:
            input_status_message("Expected Move Number" + str(g_move_count) + ". Instead: " + Game.input_stream[0:10])
            return


# Skip the move number and determine the Chess Move
# That is, parse any periods and whitespace
        Game.input_stream = Game.input_stream[length + 1 - 1:]

# Cater for how PBasic handles ^
# Replace
# regexp = "^[. \n]*"
# with
        regexp = "^[.][ \n]*"

        REGEXPR regexp IN Game.input_stream TO position, length
        if position == 1:
            Game.input_stream = Game.input_stream[length + 1 - 1:]


# Handle any comments
# If empty don't continue
        if not regexp_loop() or Game.input_stream == "":
            return


# is it "1-0" (White wins), "0-1" (Black wins), "1/2-1/2" (drawn game), OR "*"
        if check_game_termination_marker_found():
           return


    else:

        global_piece_sign = constants.COMPUTER
# For the Computer check that it is not ...
        regexp = "^[.]+"
        REGEXPR regexp IN Game.input_stream TO position, length
# Cater for how PBasic handles ^
        if position == 1:
            input_status_message("Expected the Player's Chess Move not Periods: " + Game.input_stream[position - 1:29])
            return


    parse_move_text = handle_chess_move()


def fetch_chess_move_from_file():
    """
    Handle a chess move recently parsed from an input file
    """
    if not regexp_loop() or Game.input_stream == "":
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

    handle_move_text()
