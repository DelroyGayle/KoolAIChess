# Testing

## Introduction

I am a novice chess player. I simply do not know enough chess to ensure that my program works correctly in its playing of Chess.<p>
**My Solution:**<br>There are thousands of recorded chess games on the internet, all recorded in *PGN/SAN notation*.<br>Therefore,
* if I could get the program to *actually play the chess moves as read from a pgn file*;
* then exactly the same chessboard configuration should appear after *playing the read moves*;
* without any differences in the outcomes;
* neither should there be any error messages or conflicts coming from the program.
* If any error messages or discrepancies in the outcomes occur
* then I know that there is a bug in the program that needs to be resolved.
* This is the rationale behind my method of testing.

Therefore, if there is a **input.pgn** present in the KOOLAICHESS directory:<p> 
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/72976999-049a-4e01-9c85-f6fad53403ea)
   
1. the program will first open this file, read its contents and close the file
2. parse the contents, 
3. then **play the Chess moves that was found in this file<br>*as if* both a human player and the computer were playing both *White's and Black's* moves.**

Therefore, essentially ***Chess-Playing Automation!***<br> 

* I would copy and paste the chess moves from a PGN file into *input.pgn*;
* run the program, and watch it play each move, displaying the chessboard accordingly.
* If the chosen game, ends in Check, I expect the outcome of the program to be the same.
* If the chosen game, ends in Checkmate, I expect the outcome of the program to be the same.
* Any pieces taken, the program ought to take the same pieces.
* All moves, including *Castling and En Passant*; should be followed in identical fashion. 

The program will read as many chess moves as present in *input.pgn*.
When it reaches the end of the file, it will display a suitable message to inform the user that *any further player moves will now come from the user*; likewise, the computer moves would be hereafter evaluated by the computer according to its algorithm.

## Remove pgn file when deploying
If there is *no input.pgn file* present the program will simply expect keyboard input from the user.<br>
Therefore, there ought to be *no file I/O* in the deployed version of this project.<br>
That is, before deployment, remove *input.pgn* from the project. This ensures that the program's logic expects all input to be from the user.

## **Portable Game Notation (PGN) Notation**
To quote [Wikipedia](https://en.wikipedia.org/wiki/Portable_Game_Notation)
>Portable Game Notation (PGN) is a standard plain text format for recording chess games (both the moves and related data), which can be read by humans and is also supported by most chess software.<br>
PGN was devised around 1993, by **Steven J. Edwards**, and was first popularized and specified via the Usenet newsgroup rec.games.chess.<p>
PGN is structured *"for easy reading and writing by human users and for easy parsing and generation by computer programs."* The chess moves themselves are given in algebraic chess notation using English initials for the pieces. The filename extension is .pgn.

See [this Wikipedia article](https://en.wikipedia.org/wiki/Portable_Game_Notation) for further details.<p>
The program would need to read a pgn file which has a specific format. Here are two links, [one](https://ia802908.us.archive.org/26/items/pgn-standard-1994-03-12/PGN_standard_1994-03-12.txt) and [two](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm), regarding <br>**the Standard: Portable Game Notation Specification and Implementation Guide**; which explains the actual PGN File Format Specification.

The major part that this program is interested in, is *the Movetext*.

Originally, I envisioned that the user could browse and select a pgn file from their computer and play the game. However, I quickly realised that, that is far beyond the scope of this project and my expertise. :)
<br>Instead, 
   * copy solely the Movetext from a pgn file 
   * place it into the input.pgn file
   * then the program will parse this file and run the parsed chess moves.

In short,
   * The program reads the entire contents of input.pgn
   * Removes leading/trailing whitespace
   * Removes unprintable characters (ASCII **\x00-\x08\x0B-\x1F\x7F-\xFF**)
   * Replaces Tab characters with spaces
   * Removes **carriage returns \r** leaving solely **linefeed characters \n**
   * Then parses each component that makes up a chess move; that is
   *  * Move Number
   *  * White's Chess move
   *  * Black's Chess move
   * It will play each move without human intervention until either
   * 1. It reads a item of text that it cannot parse whereby it will display a message then proceed to handle chess moves from the Player
   * 2. The end of the file is reached whereby, in like manner,  it will display a suitable message then proceed to handle chess moves from the Player
   * 3. A Game Termination Marker is detected: That is, either one of the following strings:
      + **1-0** which means (White wins)
      + **0-1** which means (Black wins)
      + **1/2-1/2** which means (drawn game)
      + **\*** which means (game in progress, result unknown, or game abandoned)
   * 4. If the program detects any of the above four strings it will perform the EOF action as described in 2.  
   
   
Now I will describe the relevant parts of the PGN file format citing the above Standard.
   
## A sample PGN game

A sample PGN game follows; it has most of the important features of a PGN file

```   
[Event "F/S Return Match"] 
[Site "Belgrade, Serbia JUG"] 
[Date "1992.11.04"] 
[Round "29"] 
[White "Fischer, Robert J."]
[Black "Spassky, Boris V."] 
[Result "1/2-1/2"] 

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3
O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15.
Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21.
Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7
27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33.
f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5
40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1/2-1/2
```

## PGN Game format
   
   > A PGN game is composed of two sections. The first is the tag pair section and the second is the Movetext section. The tag pair section provides information that identifies the game by defining the values associated with a set of standard parameters. The Movetext section gives the usually enumerated and possibly annotated moves of the game along with the concluding game termination marker. The chess moves themselves are represented using **SAN (Standard Algebraic Notation)**, also described later.
   
Essentially, a PGN file is divided up into eight *mandatory* parts - a *Seven Tag Roster* followed by the *Movetext*
   
   1. *Event* - the name of the tournament or match event
   2. *Site* - the location of the event
   3. *Date* - the starting date of the game
   4. *Round* - the playing round ordinal of the game
   5. *White* - the player of the white pieces
   6. *Black* - the player of the black pieces
   7. *Result* - the result of the game
   8. *Movetext* - The Movetext section is composed of chess moves, move number indications, optional annotations, and a single concluding game termination marker.

## Movetext

   The program expects the *input.pgn* to contain solely the *Movetext portion* of a PGN Game file.<br>
   It will parse the following:
   * Movetext move number indications - A move number indication is composed of one or more adjacent digits (an integer token) followed by *zero or more periods*. 
   * * **Note: This program expects that the Movetext begins with a move number of 1. Moreover, that the first move is White's move.**
   * A chess move in **SAN (Standard Algebraic Notation)** - please refer to the above specification links for an explanation.
   * * Essentially, this notation uses English language single character abbreviations for chess pieces,<br>that is: pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q", and king = "K".
   * The letter code for a pawn is not used for SAN moves in PGN export format movetext.
   * * **In other words, a move would consist of the letter code (blank for Pawns) followed by the Square Identification.**
   * Square identification: SAN identifies each of the sixty four squares on the chessboard with a unique two character name. The first character of a square identifier is the file of the square; a file is a column of eight squares designated by a single lower case letter from "a" (leftmost or queenside) up to and including "h" (rightmost or kingside). The second character of a square identifier is the rank of the square; a rank is a row of eight squares designated by a single digit from "1" (bottom side [White's first rank]) up to and including "8" (top side [Black's first rank]). The initial squares of some pieces are: white queen rook at a1, white king at e1, black queen knight pawn at b7, and black king rook at h8.
   
   The above essentially describes what a Chess move would look like in SAN notation:<br><em>
   * Move number
   * then White's move
   * then optionally, Black's move</em><br>

   
   However, a PGN file can also contain comments and annotations in addition to the Movetext. These are as follows:
   * The first kind of comment is the "rest of line" comment; this comment type starts with *a semicolon character and continues to the end of the line.*
   * ("{" and "}") - The second kind starts with *a left brace character and continues to the next right brace character.* Brace comments do not nest.
   * Escape mechanism - This mechanism is triggered by *a percent sign character ("%")* appearing in the first column of a line; the data on the rest of the line is ignored.
   * The left and right angle bracket characters ("<" and ">"). They are ignored in the same manner as braces ("{" and "}").
   * SAN move suffix annotations - There are exactly six such annotations available: "!", "?", "!!", "!?", "?!", and "??".
   * Movetext NAG (Numeric Annotation Glyph) -  An NAG is formed from a dollar sign ("$") with a non-negative decimal integer suffix. The non-negative integer must be from zero to 255 in value.
   * * **Note: This program ignores whether the value is greater than 255.**
   * Movetext RAV (Recursive Annotation Variation) - An RAV (Recursive Annotation Variation) is a sequence of movetext containing one or more moves enclosed in parentheses. Because the RAV is a recursive construct, **[the parentheses] may be nested.<br>The contents of the RAV as well as the parentheses are ignored.**
   * Game Termination Markers - <strong>1-0, 0-1, 1/2-1/2,*</strong>
   
   Any other kind of text would be flagged by this program as erroneous including brackets ("[" and "]").<br>Hence, the input.pgn file must solely contain *Movetext* data.
   

## Testing
### **Testing the file-handling of input.pgn** 
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
    
## **Testing SAN Input - Chess Moves** 
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

## References
* [Wikipedia - Portable Game Notation](https://en.wikipedia.org/wiki/Portable_Game_Notation)
* [Standard: Portable Game Notation Specification and Implementation Guide - Revised: 1994.03.12](https://ia802908.us.archive.org/26/items/pgn-standard-1994-03-12/PGN_standard_1994-03-12.txt)
* [HTML version](http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm)
