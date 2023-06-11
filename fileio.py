"""
For testing purposes I decided to read Chess moves from an input file
So this file contains all the routines related to reading chess moves from a file
and their validation.
"""

def regexp_loop()
    DIM position, length, firstchar, regexp
    DIM work_string

    DO

# Remove any spaces
        input_stream = lstrip(input_stream)
        if len(input_stream) == 0:
            input_status_message("No further data available from 'input.pgn'")
            return True
            return


# % Escape mechanism - This mechanism is triggered
# by a percent sign character ("%") appearing in the first column of a line;
# the data on the rest of the line is ignored up to the next \n

        regexp = "(^%)|(\n%)"
        REGEXPR regexp IN input_stream TO position, length

# Ensure anchored i.e. POSITION = 1
# length is either 1 or 2 - the correct position for the following INSTR
        if position == 1:
            position = INSTR(length, input_stream, constants.LF)
            if POSITION == 0:  # No \n found - therefore remove entire contents
                    input_stream = ""
                    continue


# Remove everything up to and including the \n
            input_stream = input_stream[position + 1 - 1:]
            continue


# Remove any leading whitespace i.e. including \n
        input_stream = lstrip(input_stream, ANY constants.CRLF + constants.SPACE)
        if len(input_stream) == 0:
            input_status_message("No further data available from 'input.pgn'")
            return True
            return


# Just in case any found - remove an 'en passant' annotation, that is 'e.p.'
        regexp = "^e\.p\.[ \n]*"
        position = 1
# Cater for how PBasic handles ^ hence POSITION = 1 AND work_string

        REGREPL regexp IN input_stream WITH "" AT position TO position, work_string
# Cater for how PBasic handles ^ hence POSITION = 1
        if position == 1:
            input_stream = work_string
            continue


        firstchar = input_stream[0:1]

        if firstchar

# Comment text may appear in PGN data.  There are two kinds of comments.  The
# first kind is the "rest of line" comment; this comment type starts with a
# semicolon character and continues to the end of the line.  The second kind
# starts with a left brace character and continues to the next right brace
# character.

            elif == ";"
# Ignore up to the end of the line
                position = INSTR(input_stream, constants.LF)
                if POSITION == 0:  # No \n found - remove entire contents
                    input_stream = ""
                    continue


# Remove everything up to and including the \n
                input_stream = input_stream[position + 1 - 1:]
                continue

            elif == "{"
# Ignore up to and including the following right brace }
                position = ignore_group_comment("{", "}")
                if not position:
                    return False
                    return
                else:
                    continue


            elif == "<"
# Ignore up to and including the following right brace }
                position = ignore_group_comment("<", ">")
                if not position:
                    return False
                    return
                else:
                    continue


            elif == constants.LPAREN  # I.E. LEFT PARENTHESIS
# An RAV (Recursive Annotation Variation) is a sequence of movetext containing
# one or more moves enclosed in parentheses.
# Because the RAV is a recursive construct, it may be nested.
# Ignore up to and including the corresponding right nested parenthesis

                position = ignore_rav()
                if not position:
                    return False
                    return
                else:
                    continue


            elif == "$"  # I.E. $nnn
# An NAG (Numeric Annotation Glyph) is a movetext element that is used to
# indicate a simple annotation in a language independent manner.  An NAG is
# formed from a dollar sign ("$") with a non-negative decimal integer suffix

                regexp = "^\$[0-9]+"
                REGEXPR regexp IN input_stream TO position, length
                if position == 1:
# Ignore $nnn
                    input_stream = input_stream[position + length - 1:]
                    continue

                input_status_message("Cannot determine this NAG: " + input_stream[0:6])
                return False
                return

            elif == constants.LBRACKET  # I.E. [ ... ] tag pair
# Tag Pairs  [ ... ] ' todo
# Seven Mandatory

                 position = handle_tag_pair()
                 if not position:
                    return False
                    return
                else:
                    continue


            elif == else:
# Either Move Number, a Chess Move or no more data
                 return True
                 return


    LOOP


def parse_move_text()
    DIM regexp, move_number
    DIM position, length, piece_sign
    DIM i, c

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
        REGEXPR regexp IN input_stream TO position, length
# Cater for how PBasic handles ^
        if position != 1:
            input_status_message("Expected Move Number" + str(g_move_count) + ". Instead: " + input_stream[0:10])
            return


# Expecting matching move number

# Determine the move number
# PRINT VAL("10."), VAL("10..") ==>  10 10

        move_number = VAL(input_stream[0:length])

        if g_move_count != move_number:
            input_status_message("Expected Move Number" + str(g_move_count) + ". Instead: " + input_stream[0:10])
            return


# Skip the move number and determine the Chess Move
# That is, parse any periods and whitespace
        input_stream = input_stream[length + 1 - 1:]

# Cater for how PBasic handles ^
# Replace
# regexp = "^[. \n]*"
# with
        regexp = "^[.][ \n]*"

        REGEXPR regexp IN input_stream TO position, length
        if position == 1:
            input_stream = input_stream[length + 1 - 1:]


# Handle any comments
# If empty don't continue
        if not regexp_loop() or input_stream == "":
            return


# is it "1-0" (White wins), "0-1" (Black wins), "1/2-1/2" (drawn game), OR "*"
        if check_game_termination_marker_found():
           return


    else:

        global_piece_sign = constants.COMPUTER
# For the Computer check that it is not ...
        regexp = "^[.]+"
        REGEXPR regexp IN input_stream TO position, length
# Cater for how PBasic handles ^
        if position == 1:
            input_status_message("Expected the Player's Chess Move not Periods: " + input_stream[position - 1:29])
            return


    parse_move_text = handle_chess_move()


def fetch_chess_move_from_file():
    """
    Handle a chess move recently parsed from an input file
    """
    if not regexp_loop() or Game.input_stream == "":
        # Erroneous or Empty input
        return

    # Must be the movetext section.
    # The movetext section is composed of chess moves, move number indications, comments,
    # optional annotations, and a single concluding game termination marker.

    # is it "1-0" (White wins), "0-1" (Black wins), "1/2-1/2" (drawn game), OR "*"
    if check_game_termination_marker_found():
        return

    # Could be either a Move Number or a Chess Piece

    handle_move_text()
