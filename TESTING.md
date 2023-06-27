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
When it reaches the end of the file, it will display a suitable message to inform the user that *any further player moves will now come from the user*; likewise, the computer moves would hereafter be evaluated by the computer according to its algorithm.

## Remove pgn file when deploying
If there is *no input.pgn file* present the program will simply expect keyboard input from the user.<br>
Therefore, there ought to be *no file I/O* in the deployed version of this project.<br>
That is, before deployment, remove *input.pgn* from the project. This ensures that the program's logic expects all input to be from the user.

-----
   
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
   * a) It reads a item of text that it cannot parse whereby it will display a message. Then it will proceed to handle chess moves from the Player via the keyboard
   * b) The end of the file is reached whereby, in like manner,  it will display a suitable message. Then it will proceed to handle chess moves from the Player via the keyboard
   * c) A Game Termination Marker is detected: That is, either one of the following strings:
      + **1-0** which means (White wins)
      + **0-1** which means (Black wins)
      + **1/2-1/2** which means (drawn game)
      + **\*** which means (game in progress, result unknown, or game abandoned)
   * d) If the program detects any of the above four strings it will perform the EOF action as described in **b)**.  
   
   
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
   
   > A PGN game is composed of two sections. The first is the tag pair section and the second is the Movetext section. The tag pair section provides information that identifies the game by defining the values associated with a set of standard parameters. The Movetext section gives the usually enumerated and possibly annotated moves of the game along with the concluding game termination marker. The chess moves themselves are represented using **SAN (Standard Algebraic Notation)**.<br>
   See [this article](https://www.chessprogramming.org/Algebraic_Chess_Notation#Standard_Algebraic_Notation_.28SAN.29) for an explanation of **SAN**.<p>
   
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
   * A chess move in **SAN (Standard Algebraic Notation)** - please refer to [this link](https://www.chessprogramming.org/Algebraic_Chess_Notation#Standard_Algebraic_Notation_.28SAN.29) for an explanation.
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
   
## The Output of the Game

   One of the features of this program is that at the end of a game,
   the program will produce **all the moves of the game in <br>Long algebraic notation (LAN)** and write them both out to the screen and the ***output.pgn* file**<p>
   To quote [Wikipedia](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)), 
   > **In long algebraic notation (LAN), also known as full/fully expanded algebraic notation,<br> 
   both the starting and ending squares are specified**,<br>
   for example: e2e4. Sometimes these are separated by a hyphen, e.g. Nb1-c3, while captures are indicated by an "x", e.g. Rd3xd7.<br>
   Long algebraic notation takes more space and is no longer commonly used in print; however, it has the advantage of clarity. 

   <p>Therefore, this program produces the output of all moves in LAN <em>without hyphens</em> so that an user such as I,<br> can read the moves clearly without too much difficulty;<br>that is,
   <em>what moves were made from what square to which square, and what piece was moved.</em><p>
   Please note: this is LAN as opposed to strict SAN as expected in the PGN Standard.<br>Nevertheless, PGN files can indeed contain LAN and Chess-playing software should understand LAN.
	   
## Limitations
* When it comes to File Input of moves and Pawn Promotion, *Kool AI* solely promotes Pawns to Queens.
* Therefore, when parsing *input.pgn* the program will ignore the annotation *=N* in a move such as **a8=N**.
* Instead it would automatically promote the pawn in a8 to a Queen.
-----
   
## Testing
### **Testing the file-handling of input.pgn** 
1. **Test: Empty File** - An empty file should be ignored. Simply proceed with the prompt for user's input.
    * *Method Used*
        
        I modified *open_input_file()* to make it think it had an empty file e.g.<br>
         if len(file_contents) == 0 *or True*:<br>
        **# The above IF will always be True**
    * *Result*
        
        The Chessboard is displayed with the prompt:<br>
        *YOUR MOVE (e.g. e2e4):*    
1. **Test: Large File** - I set a limit of 10,000 characters for the size of the input file.
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

-----
   
### **Testing PGN Input - Non-Chess Moves** 
I performed the following testing of ad hoc input of PGN comments and annotations in the following manner.<br>
Comments should always be ignored when parsing input.
1. **Test: Comments that begin with ; i.e. semicolon** - <br>With the **;** type comment all input is ignored to the end of the line.<br>
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
1. **Test: % i.e. percent escape mechanism** -  a percent sign character ("%") appearing in the first column<br>of a line means ignore the rest of the line<br>So, the following entries ought to be all interpreted as empty input.
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
1. **Test: Comments using {} and <> i.e. braces and angled brackets** -<br>
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
      
1. **Test: RAVs using () i.e. parentheses** - All text within the parentheses and including the parentheses should be ignored.<br>**Note: the parentheses (unlike braces/brackets) can be nested**<br>
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
1. **Test: NAGs $nnn** - Dollar followed by a nonnegative integer.<br>This annotation ought to be ignored.<br>(I ignore the numeric value, that is, regardless whether it is greater than 255.)<br>
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
	
1. **Test: Ignore e.p.** - Although not allowed according to the *PGN standard*,<br> sometimes the en passant move
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

-----
       
### **Testing SAN Input - Chess Moves** 
1. **Test Move Numbers** - The PGN file should have consecutive numbered pairs of chess moves **starting with Number 1**.<p>
    * *Method Used*
        
        I set *input.pgn* contents to have various annotations:<br>
        * "e.p. e.p.**2.**{Testing Various Annotations} ((ABC)) e.p."<p>
    
    * *The Output* - the following error message
        
        Expected Move Number 1. **Instead: 2.**{Testing<br>
        There will be no further input from 'input.pgn'

    * *Solution*

        The PGN file must start with *White's move numbered 1.* 
    
1. **Test One Move: Move Number, Comment and Chess Move** - Test one line of movetext with all three elements.<p>
    Move numbers should be an integer followed by (optionally) a period. Then there should be a **chess move** and optionally, annotations as well. 
    All annotations are to be ignored except for **Game Termination Markers**
    * *Method Used*
        
        I set *input.pgn* contents to have all three elements as follows:<br>
        * "1. {One Chess move} e4"<p>
    
    * *The Output*<p>
![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/f53e0879-03b4-47d1-812f-15f0c2f4e270)
         
    ```    
    I am evaluating my next move...
    Finished reading all the moves from the input file
    There will be no further input from 'input.pgn'
    ```
    * Then a 3 second delay, in addition to the general *2 second delay, hence a total delay of 5 seconds*
    * This gives the user,  plenty of time to see that *there is no longer any futher PGN file input*
    * The Computer then displays the updated chessboard with its own move of 
    * **Computer moves e7-e6 Piece: Pawn**

      ![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/38eb7d4c-c313-4f71-8090-d5564a394484)
       

       
    * *Summary*

        1. The Computer successfully parsed all three elements: *the number 1, a comment, the move e4*
        2. It converted e4 to *e2e4* then played it as White's move
        3. Updated the chessboard and displayed it with White's move
        4. Then proceeded to fetch the next move from the input file
        5. No further input therefore the Computer evaluated its own move - in this case *e7e6*
        6. Then played Black's move of *e7e6*
        7. Updated the chessboard and displayed it with Black's move
        8. Then prompted the Player for the next move; expecting all further moves to be from the keyboard<p>

1. **Test Two Moves: Move Number, Comments and Move** - Test that it can play two moves from the input file<p>
    The format is *move number, White's move, Black's move*<br>
    All annotations are to be ignored except for **Game Termination Markers**
    * *Method Used*
        
        I set *input.pgn* contents to have two Chess moves with comments as follows:<br>
        * "1. {First move} e4 (2nd move) h5"<p>
    
    * *The Output*
           
      ![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/f53e0879-03b4-47d1-812f-15f0c2f4e270)
           
 The Computer then reads *h5*. Converts *h5* to *h7h5* and plays it as Black's move

 * *The Output*
           
   ![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/c38b95e9-9753-4fbd-9ce1-7c7e045be873)

    ```    
    Finished reading all the moves from the input file
    There will be no further input from 'input.pgn'
    ```
    * Then a 5 second delay, as described above
    * Then the Computer prompts the Player for the next move; expecting all further moves to be from the keyboard<p>           

           
    * *Summary*

        1. The Computer successfully parsed all both Chess moves
        2. It converted e4 to *e2e4* then played it as White's move
        3. Updated the chessboard and displayed it with White's move
        4. Then proceeded to fetch the next move from the input file
        5. In this case *h5*. It converted h5 to *h7h5* then played it as Black's move
        6. Updated the chessboard and displayed it with Black's move
        4. Then proceeded to fetch the next move from the input file
        5. No further input therefore the Computer prompts the Player for the next move;<br>expecting all further moves to be from the keyboard<p>
           

-----

### **Testing any number of moves**
           
1. **Test the removal of SAN move suffix annotations** - That is, "!", "?", "!!", "!?", "?!" and "??"
           
    * *Method Used*
    <p>The Movetext used can be found in testdata/file01.pgn
       
    ```
    1. e4 c6 2. d4? d5 3. e5? Bf5! 4. Nf3 !? e6 5. !? Be2 Nh6!!
    ```
           
    * Various annotations and comments have been added which ought to be ignored by the program
    * Run the program:
    
    * *The Output*
           
      ![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/3abb6084-11e0-4601-8de6-c2190eb00230)

           
    * All moves were played successfully without any issues.           

-----
         
2. **Castling** - Test that user can *Castle Kingside*
           
    * *Method Used*
    <p>The Movetext used can be found in testdata/file02.pgn
    <p>This is the original Movetext that I based this test on
       
    ```
    1. e4 c6 2. d4 d5 3. e5 Bf5 4. Nf3 e6 5. Be2 Nh6 6. O-O Bg6
    ```
           
    * **Note the moves numbered 6. Number 6's White Move is Castling O-O**
    * So, I solely populate input.pgn with 1. e4 c6 2. d4 d5 3. e5 Bf5 4. Nf3 e6 5. Be2 Nh6
    * That is, *without Number 6 moves.* 
    * Run the program:
    
    * *The Output*
           
	![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/3abb6084-11e0-4601-8de6-c2190eb00230)
           
 * All moves were played successfully without any issues. In fact, identical to **Test 1.**
 * As you can see, White's position of pieces are indeed **set up for (Kingside) Castling**
 * So, I entered **O-O**

 * *The Output*
           
   ![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/ac308bee-3ed5-435b-b2f9-1202dac400e2)

           
* Success! Incidentally, the Computer responded with:
           
	![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/1284bad3-255e-4c0c-9667-e52a3dec4055)

-----
                     
3. **Test the detection of Game Termination Markers** - That is, "1-0", "0-1", "1/2-1/2" and "*"
           
    * *Method Used*
    <p>The Movetext used can be found in testdata/file03.pgn
       
    ```
    1. e4 c6 2. d4 d5 3. e5 Bf5 4. Nf3 e6 5. Be2 Nh6 6. O-O Bg6 7. c3 Be7 8. Bxh6
    gxh6 9. Qc1 h5 10. c4 dxc4 11. Bxc4 Nd7 12. Nc3 Qc7 13. Qf4 Nb6 14. Bb3 O-O-O
    15. Rac1 Kb8 16. Rfd1 Qd7 17. Nh4 Rhf8 18. Nxg6 hxg6 19. Ne4 Qc7 20. Qf3 Nd5 21.
    Nc3 Qb6 22. h3 Qb4 23. Ne4 Nc7 24. Rc4 Qb6 25. Rd3 Nd5 26. Rd1 Rd7 27. Rc2 Qa5 
    28. a3 Nc7 29. Bc4 Nb5 30. Rcd2 a6 31. Rd3 Qd8 32. Nc5 Bxc5 33. dxc5 Rxd3 34. 
    Rxd3 1/2-1/2
    ```
    * That is, 34 moves ending with White's Rook move then the *Game Termination Marker 1/2-1/2*<br>
    Because of Black's Castling move in **No. 14. Bb3 O-O-O**; this game will also test that *Kool AI can Castle correctly!*
    * Run the program:
    
    * *The Output*
           
      	![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/67bbfffe-dca3-4971-b07e-d763f4c10db4)

           
 * All 34 sets of moves were played successfully without any issues.
 * Incidentally, the Computer responded with:

	![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/d01f5fcf-326b-4573-b7bb-837c68edc683)

-----
     
4. **Can program play its own output?** - That is, can it play using Long algebraic notation?
           
   One of the features of this program is that at the end of a game,
   the program will produce <br>**all the moves of the game in Long algebraic notation (LAN)** and write them both out to the screen and the ***output.pgn* file**<p>

   The main purpose of this test is that:
   1. Game moves recorded in SAN are converted to LAN when played by this program.
   2. Regardless of notation, **the game-play ought to be identical!**
   3. Therefore, if the program reads and plays **the same game** using LAN notation, the outcome ought to be identical!<p>
      
    * *Method Used*
    <p>The Movetext used can be found in testdata/file04.pgn<br>
    This is the output of the moves in testdata/file03.pgn after they were used in <strong>Test 3.</strong> So, all the moves have been converted from SAN to LAN.<br>
    The pgn file, testdata/file04.pgn, has <em>no newlines</em> in order to test that lack of newlines is not an issue for the program.
    
    testdata/file05.pgn has the same data with newlines as shown here:
    ```
	1. e2e4 c7c6 2. d2d4 d7d5 3. e4e5 Bc8f5 4. Ng1f3 e7e6 5. Bf1e2 Ng8h6 6. O-O Bf5g6 7. c2c3 Bf8e7 8. Bc1xh6 g7xh6
    9. Qd1c1 h6h5 10. c3c4 d5xc4 11. Be2xc4 Nb8d7 12. Nb1c3 Qd8c7 13. Qc1f4 Nd7b6 14. Bc4b3 O-O-O 15. Ra1c1 Kc8b8
    16. Rf1d1 Qc7d7 17. Nf3h4 Rh8f8 18. Nh4xg6 h7xg6 19. Nc3e4 Qd7c7 20. Qf4f3 Nb6d5 21. Ne4c3 Qc7b6
    22. h2h3 Qb6b4 23. Nc3e4 Nd5c7 24. Rc1c4 Qb4b6 25. Rd1d3 Nc7d5 26. Rd3d1 Rd8d7 27. Rc4c2 Qb6a5
    28. a2a3 Nd5c7 29. Bb3c4 Nc7b5 30. Rc2d2 a7a6 31. Rd2d3 Qa5d8 32. Ne4c5 Be7xc5 33. d4xc5 Rd7xd3 
	34. Rd1xd3
    ```
    * That is, the same 34 moves as in **Test 3** in LAN.
    * Run the program:
    
    * *The Output*
           
      	![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/d70d82d1-26b9-42dc-973b-0aa14a97f99e)

           
 * All moves were played successfully without any issues.
 * With the Computer responded identically with **Nb5d4**
 * When I compared the contents of testdata\file04.pgn with the outputted moves of this game *without the computer-generated move Nb5d4 and without newlines* using [Diffchecker](https://www.diffchecker.com/text-compare/), the result was<p>
   	![image](https://github.com/DelroyGayle/KoolAIChess/assets/91061592/d229c5a4-a792-49e4-8f4c-37d5c0d3ad0b)


-----

5. **Castling** - Test that user can *Castle Queenside*
   * *Method Used*
     <p>The Movetext used can be found in testdata/file06.pgn<br>
	The Chess moves are taken from the [Opera Game](https://en.wikipedia.org/wiki/Opera_Game)
  
    ```
    1. e2e4 e7e5 2. Ng1f3 d7d6 3. d2d4 Bc8g4 4. d4xe5 Bg4xf3 5. Qd1xf3 d6xe5
    6. Bf1c4 Ng8f6 7. Qf3b3 Qd8e7 8. Nb1c3 c7c6 9. Bc1g5 b7b5 10. Nc3xb5
    c6xb5 11. Bc4xb5+ Nb8d7 12. O-O-O Ra8d8 13. Rd1xd7 Rd8xd7 14. Rh1d1
    Qe7e6 15. Bb5xd7+ Nf6xd7 16. Qb3b8+ 1-0
    ```
           
    * **Note the moves numbered 12. Number 12's White Move is Castling O-O-O**
    * Run the program:
    * All moves were played successfully without any issues.
    
    * *The Output*

    ```
    Checking Player move for b3-b8 Piece: Queen
    I am in Check
    Kool AI resigns!
    The moves of this Chess Game are as follows:

    1. e2e4 e7e5 2. Ng1f3 d7d6 3. d2d4 Bc8g4 4. d4xe5 Bg4xf3 5. Qd1xf3 d6xe5
    6. Bf1c4 Ng8f6 7. Qf3b3 Qd8e7 8. Nb1c3 c7c6 9. Bc1g5 b7b5 10. Nc3xb5
    c6xb5 11. Bc4xb5+ Nb8d7 12. O-O-O Ra8d8 13. Rd1xd7 Rd8xd7 14. Rh1d1
    Qe7e6 15. Bb5xd7+ Nf6xd7 16. Qb3b8+ 1-0

    These moves have also been written to /workspace/KoolAIChess/output.pgn

    ```           
           
Note:
1. The difference is that KoolAI resigned at **Move 16** forseeing that it could not win this game.
2. When you compare the contents of file06.pgn with the above output you will see that<br>
*All the captures shown by **x** and all the checks shown by **+** correspond!*
3. Afterwards, I pasted the outputted moves into input.pgn just to ensure that the moves played and the output were identical.
Therefore, confirming that  *captures **x** and checks **+*** do not interfere with parsing.

-----

6. **Ignore Annotations** - Test that user can *Castle Queenside*

* Another test to ensure that comments and annotations do not interfere with the parsing of a pgn file
* I made up the annotations (++ # =Q ) for these moves. They do not actually correspond to any of these moves.
* That is, there are no checks, checkmates or promotions in this game.
* I added these simply to check that they are all being ignored during parsing.
* *Method Used*
     <p>The Movetext used can be found in testdata/file07.pgn<br>
    
* Run the program:
* All moves were played successfully without any issues.
* *The Output*
```
Computer moves a5-b4 Piece: Pawn
Computer took your Pawn
```


-----

7. **Illegal Moves** - To test the response when an *illegal move* is read from an input file

* *Method Used*
     <p>The Movetext used can be found in testdata/file08.pgn<br>
* **h8h7** in this game is an illegal move since there would be a piece occupying **h7**
    
* Run the program:
* *The Output*
```
Legal Chess Move Expected From Input File. Instead h8h7 6.
There will be no further input from 'input.pgn'
```
-----

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
* [Wikipedia - Algebraic notation (chess)](https://en.wikipedia.org/wiki/Algebraic_notation_(chess))
* [Algebraic Chess Notation](https://www.chessprogramming.org/Algebraic_Chess_Notation)
* [Diffchecker](https://www.diffchecker.com/text-compare/)
