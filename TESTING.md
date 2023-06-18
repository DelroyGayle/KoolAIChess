# Testing

## Introduction

I am a novice chess player. I simply do not know enough chess to ensure that my program works correctly in its playing of Chess.<br>**My Solution:**<br>There are thousands of recorded chess games on the internet, all recorded in *PGN notation*.<br>Therefore,
* if I could get the program to *actually play the chess moves as read from a pgn file*;
* then exactly the same chessboard configuration should appear after *playing the read moves*;
* without any differences in the outcomes;
* neither should there be any error messages or conflicts coming from the program.
* If any error messages or discrepancies in the outcomes occur
* then I know that there is a bug in the program that needs to be resolved.
* This is the rationale behind my method of testing.

Therefore, if there is a **input.pgn** present in the KOOLAICHESS directory: 
1. the program will first open this file, read its contents and close the file
2. parse the contents, 
3. and then **play the Chess moves that was found in this file<br>*as if* both a human player and the computer were playing both *White's and Black's* moves.**

Therefore, essentially ***Chess-Playing Automation!***<br> 

* I would copy and paste the chess moves from a PGN file into *input.pgn*;
* run the program, and watch it play each move, displaying the chessboard accordingly.
* If the chosen game, ends in Check, I expected the outcome of the program to be the same.
* If the chosen game, ends in Checkmate, I expected the outcome of the program to be the same.
* Any pieces taken, the progarm ought to take the same pieces.
* All moves, including *Castling and En Passant*; should be followed in identical fashion. 

The program will read as many chess moves as present in *input.pgn*.
When it reaches the end of the file, it will display a suitable message to inform the user that<br>*any further player moves will now come from the user*; likewise, the computer moves would be hereafter evaluated by the computer according to its algorithm.

## Remove pgn file when deploying
If there is *no input.pgn file* present the program will simply expect keyboard input from the user.<br>
Therefore, there ought to be *no file I/O* in the deployed version of this project.<br>
That is, before deployment, remove *input.pgn* from the project. This ensures that the program's logic expects all input to be from the user keyboard.

## **Portable Game Notation (PGN) Notation**
Portable Game Notation (PGN) is a standard plain text format for recording chess games (both the moves and related data), which can be read by humans and is also supported by most chess software.

## **Testing input.pgn** 
1. **Test - Empty File** - Empty file should be ignored. Should simply proceed with the prompt for user's input.
    * *Method Used*
        
        I modified *open_input_file()* to make it think it had an empty file e.g.<br>
         if len(file_contents) == 0 *or True*:<br>
        **# The above IF will always be True**
    * *Result*
        
        The Chessboard is displayed with the prompt:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test - Large File** - I set a limit of 10,000 characters for the size of the input file.
    * *Method Used*
        
        I modified *open_input_file()* to make it think it had a large file e.g.<br>
         if len(file_contents) > constants.FILE_SIZE_LIMIT or *True:*<br>
        **# The above IF will always be True**
    * *Result*

        The following message was displayed for 5 seconds:<br>
        **Input file too big - larger than 10000 characters<br>
        There will be no further input from 'input.pgn'**<br>
        
        Then the Chessboard is displayed and the User is prompted for input of Chess moves<br>
        *YOUR MOVE (e.g. e2e4):*    
## **Testing SAN Input - Non-Chess Moves** 
I performed the following testing of ad hoc input of PGN comments and annotations in the following manner.<br>
Comments should always be ignored when parsing input.
1. **Test - Comments using ; i.e. semicolon** - <br>With the **;** type comment all input is ignored to the end of the line.<br>
    So, the following entries ought to be all interpreted as empty input.
    * *Method Used*
    
        I set *input.pgn* contents with just one of the following lines as its file contents<br>
        1. ;ABCDEF\n;\n<br>
        2. ;ABC\n;DEF<br>
        3. ;ABC\n;DEF\n<p>
    * *The Output*
        
        In each of the above three cases the Chessboard is displayed with the message:<br>
        **Finished reading all the moves from the input file<br>
        There will be no further input from 'input.pgn'**<p>
        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test % i.e. percent escape mechanism** -  a percent sign character ("%") appearing in the first column<br>of a line means ignore the rest of the line<br>So, the following entries ought to be all interpreted as empty input.
    * *Method Used*
    
        I set *input.pgn* contents with just one of the following lines as its file contents<br>
        1. %testing123<br>
        2. ;ABC\n%testing123\n<p>
        
    * *The Output*
        
        In each of the above two cases the Chessboard is displayed with the message:<br>
        **Finished reading all the moves from the input file<br>
        There will be no further input from 'input.pgn'**<p>
        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test - Comments using {} and <> i.e. braces and angled brackets** -<br>
    All text within the braces and including the braces should be ignored.<br>
    All text within the angled brackets and including the angled brackets should be ignored.<br>
    So, the following entries ought to be all interpreted as empty input.
    * *Method Used*
    
        I set *input.pgn* contents with just one of the following lines as its file contents<br>
        1. ;ABC;DEF;\n{comments}<br>
        2. ;ABC\n%testing123\n\<comments\><p>
    
    * *The Output*
        
        In each of the above two cases the Chessboard is displayed with the message:<br>
        **Finished reading all the moves from the input file<br>
        There will be no further input from 'input.pgn'**<p>
        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
    
    **How about unmatched braces/brackets?**
    * *Method Used*
    
        I set *input.pgn* contents with just one of the following lines as its file contents<br>
        1. ;ABC;DEF;\n\{comments<br>
        2. ;ABC\n%testing123\n\<comments<p>
    
    * *The Output*
        
        The Chessboard is displayed followed by:<p>
        *For number 1.*
        ```
        Found { however cannot determine where } ends
        There will be no further input from 'input.pgn'
        ```
        
        *For number 2.* 
        ```
        Found < however cannot determine where > ends
        There will be no further input from 'input.pgn'
        ```

        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test - RAVs using () i.e. parentheses** - All text within the parentheses and including the parentheses should be ignored.<br>**Note: the parentheses (unlike braces/brackets) can be nested**<br>
    * *Method Used*
    
        I set *input.pgn* contents to<br>
        * ;ABC;DEF;\n{comments}((RAV COMMENT)TESTING)<p>
    
    * *The Output*
        
        The Chessboard is displayed with the message:<br>
        **Finished reading all the moves from the input file<br>
        There will be no further input from 'input.pgn'**<p>
        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
    
    **How about unmatched parentheses?**
    * *Method Used*
    
        I set *input.pgn* contents to<br>
        * \(RAV COMMENT<p>
    
    * *The Output*
        
        The Chessboard is displayed followed by:<p>
        ```
        Cannot determine where this RAV closes: (RAV COMMENT
        There will be no further input from 'input.pgn'
        ```

        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test - NAGs $nnn** - Dollar followed by a nonnegative integer.<br>This annotation ought to be ignored.<br>(I ignore the numeric value, that is, regardless whether it is greater than 255.)<br>
    * *Method Used*
        
        I set *input.pgn* contents with just one of the following lines as its file contents<br>
        1. {Testing NAGs} $123<br>
        2. {Testing NAGs} $0<br>
        3. {Testing NAGs} $-123<br>
        4. {Testing NAGs} ${OK?}<p>
    
    * *The Output*
        
        The Chessboard is displayed followed by:<p>
        *For numbers 1. and 2.*
        ```
        Finished reading all the moves from the input file
        ```
        
        *For number 3.* 
        ```
        Cannot determine this NAG: $-123{
        ```
        
        *For number 4.* 
        ```
        Cannot determine this NAG: ${OK?}{
        ```

        Each of the above are then followed by the message:<br>
        *There will be no further input from 'input.pgn'*<br>
        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    

        **Please Note: To save repetition**, in all the tests following:
        1. The chessboard is always displayed
        2. Followed by a relevant message regarding the failure of parsing a file input
        3. Then the message: *There will be no further input from 'input.pgn'*
        4. Followed by the user prompt, *YOUR MOVE (e.g. e2e4):*<p>
1. **Test - Ignore e.p.** - Although not allowed according to the *PGN standard*,<br> sometimes the en passant move
annotation **e.p.** appears in PGN files. Therefore, if found, it ought to be ignored.<br>
    * *Method Used*
        
        I set *input.pgn* contents to have various annotations:<br>
        * "e.p. e.p.1{Testing Various Annotations} ((ABC)) e.p."<p>

    * *The Output*
        
        The Chessboard is displayed followed by:<p>
        ```
        Finished reading all the moves from the input file
        ```
        etc.

        So, all that is parsed is the move number **1** followed by a comment i.e. null input, which in turn, is ignored. 
    
1. **Test Move Numbers** - The PGN file should have consecutive numbered pairs of chess moves **starting with Number 1**.<p>
    * *Method Used*
        
        I set *input.pgn* contents to have various annotations:<br>
        * "e.p. e.p.**2.**{Testing Various Annotations} ((ABC)) e.p."<p>
    
    * *The Output*
        
        Expected Move Number 1. **Instead: 2.**{Testing
        There will be no further input from 'input.pgn'

    * *Solution*

        The PGN file must start with *White's move numbered 1.* 
    
1. **Test One Move: Move Number, Comment and Move** - Test one line of movetext with all three elements.<p>
    Move numbers should be an integer followed by (optionally) a period. Then there should be a **chess move** and optionally, annotations as well. All annotations are to be ignored except for **Game Termination Markers**
    * *Method Used*
        
        I set *input.pgn* contents to have all three elements as follows:<br>
        * "1. {One Chess move} e4"<p>
    
    * *The Output*
    ```    
    I am evaluating my next move...
    Finished reading all the moves from the input file
    There will be no further input from 'input.pgn'
    ```
    * Then a 3 second delay, in addition to the general *2 second delay, hence a total delay of 5 seconds*
    * This gives the user,  plenty of time to see that *there is no longer any futher PGN file input*
    * The Computer then displays the updated chessboard with its own move of 
    * **Computer moves e7-e6 Piece: Pawn**

    * *Summary*

        1. The Computer successfully parsed all three elements: *the number 1, a comment, the move e4*
        2. It converted e4 to *e2e4* then played White's move of *e2e4*
        3. Updated the chessboard and displayed it with White's move
        4. Then proceeded to fetch the next move from the input file.
        5. No further input therefore the Computer evaluated its own move - in this case *e7e5*
        6. Then played Black's move of *e7e5*
        7. Updated the chessboard and displayed it with Black's move
        8. Then prompted the Player for the next move; expecting all further moves to be from the keyboard<p>

1. **Test Two Moves: Move Number, Comments and Move** - Test that it can play two moves from the input file<p>
    The format is *move number, White's move, Black's move*
    All annotations are to be ignored except for **Game Termination Markers**
    * *Method Used*
        
        I set *input.pgn* contents to have all three elements as follows:<br>
        * "1. {First move} e4 (2nd move) h5"<p>
    
    * *The Output*
    ```    
    I am evaluating my next move...
    Finished reading all the moves from the input file
    There will be no further input from 'input.pgn'
    ```
    * Then a 3 second delay, in addition to the general *2 second delay, hence a total delay of 5 seconds*
    * This gives the user,  plenty of time to see that *there is no longer any futher PGN file input*
    * The Computer then displays the updated chessboard with its own move of 
    * **Computer moves e7-e6 Piece: Pawn**

    * *Summary*

        1. The Computer successfully parsed all three elements: *the number 1, a comment, the move e4*
        2. It converted e4 to *e2e4* then played White's move of *e2e4*
        3. Updated the chessboard and displayed it with White's move
        4. Then proceeded to fetch the next move from the input file.
        5. No further input therefore the Computer evaluated its own move - in this case *e7e5*
        6. Then played Black's move of *e7e5*
        7. Updated the chessboard and displayed it with Black's move
        8. Then prompted the Player for the next move; expecting all further moves to be from the keyboard<p>

1. **Test** - Empty file should be ignored. Instead prompt user for input.
Used various strings that are interpreted as comments in SAN
    * *Method Used*
    * *The Output*
        * 
    * *Issues Found* 
        * 
    * *Solution Found*
        * 
1. **Test** - 
    * *Method Used*
        * .
    * *The Output* 
        * .
    * *Issues Found*
    *  *Solution Found:*
        *  .

