# Testing

## Introduction

I am a novice chess player. I simply do not know enough chess to ensure that my program works correctly in its playing of Chess.<br>**My Solution:**<br>There are thousands of recorded chess games on the internet, all recorded in *PGN notation*.<br>Therefore,
* if I could get the program to *actually play the chess moves as read from a pgn file*;
* then exactly the same chessboard configuration should appear after *playing the read rules*;
* without any differences in the outcomes;
* nor any error messages or conflicts coming from the program.
* If any error messages or discrepancies in the outcomes occur
* then I know that there is a bug in the program that needs to be resolved.
* This is the rationale behind my method of testing.

Therefore, if there is a **input.pgn** in the KOOLAICHESS directory: 
* the program will first open this file,
* parse it contents, 
* and then **play the Chess moves as found in this file 
* *as if** both a human user and the computer were playing both *White and Black* moves.**

Therefore, essentially *Chess-Playing Automation!*<br> 

* I would copy and paste the chess moves from a PGN file into *input.pgn*,
* run the program, and watch it play each move, displaying the chessboard accordingly.
* If the chosen game, ends in Check, I expected the outcome of the program to be the same.
* If the chosen game, ends in Checkmate, I expected the outcome of the program to be the same.
* Any pieces taken, the progarm ought to take the same pieces.
* All moves, including *Castling and En Passant*; should be followed in identical fashion. 

The program will read as many chess moves it can find in *input.pgn*.
When it reaches the end of the file, it will display a suitable message to inform the user that *any further player moves will now come from the user*; likewise, computer moves would be indeed evaluated by the computer according to its algorithm.

## Remove pgn file when deploying
If there is *no input.pgn file* the program will simply expect keyboard input from the user.<br>
Therefore, they ought to be *no file I/O* in the deployed version of this project.<br>
That is, before deployment, remove *input.pgn* from the project.

## PGN Notation
Portable Game Notation (PGN) is a standard plain text format for recording chess games (both the moves and related data), which can be read by humans and is also supported by most chess software.

## **Testing input.pgn** 
1. **Test - Empty File** - Empty file should be ignored. Instead prompt user for input.
    * *Method Used*
        
        I modified *open_input_file()* to make it think it had an empty file e.g.<br>
         if len(file_contents) == 0 *or True*:<br>
        **# The above IF will always be True**
    * *Result*
        
        The Chessboard is then displayed with the prompt:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test - Large File** - I set a limit of 10,000 characters for the size of the input file
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
I performed the testing of ad hoc input of comments and annotations in the following manner.
1. **Test - Comments using ; i.e. semicolon** - Comments should always be ignored when parsing input.<br>So the following entries ought to be all interpreted as empty input.
    * *Method Used*
    
    I set *input.pgn* with just one of the following lines as its file contents<br>
        1. ;ABCDEF;\n<br>
        2. ;ABC\n;DEF<br>
        3. ;ABC\n;DEF\n<br>
    * *The Output*
        
        In each of the above 3 cases the Chessboard is displayed with the message:<br>
        **Finished reading all the moves from the input file<br>
        There will be no further input from 'input.pgn'**<p>
        Then the user is prompted:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test - Empty File:** - Empty file should be ignored. Instead prompt user for input.
    * *Method Used*
        
        I modified *open_input_file()* to make it think it had an empty file e.g.<br>
         if len(file_contents) == 0 *or True*:<br>
        **# The above if will always be True**
    * *The Output*
        
        Chessboard displayed with the prompt:<br>
        *YOUR MOVE (e.g. e2e4):*    
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

1. **Test** - 
    * *Method Used*
        * .
    * *The Output*
        * .
    * *Issues Found*
    * *Solution Found:*
        * .
1. **Test** - 
    * *Method Used*
        * .
    * *The Output*
        * .
    * *Issues Found*
    * *Solution Found*
        * .
        * 
