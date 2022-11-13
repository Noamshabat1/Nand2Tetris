// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// This program illustrates low-level handling of the screen and keyboard
// devices, as follows.
//
// The program runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
// 
// Assumptions:
// Your program may blacken and clear the screen's pixels in any spatial/visual
// Order, as long as pressing a key continuously for long enough results in a
// fully blackened screen, and not pressing any key for long enough results in a
// fully cleared screen.
//
// Test Scripts:
// For completeness of testing, test the Fill program both interactively and
// automatically.
// 
// The supplied FillAutomatic.tst script, along with the supplied compare file
// FillAutomatic.cmp, are designed to test the Fill program automatically, as 
// described by the test script documentation.
//
// The supplied Fill.tst script, which comes with no compare file, is designed
// to do two things:
// - Load the Fill.hack program
// - Remind you to select 'no animation', and then test the program
//   interactively by pressing and releasing some keyboard keys

(KEYBOARD)

// fill = 0000.0000 0000.0000
    @fill
    M=0

// if KBD !=0 goto PAINT
    @KBD
    D=M
    @PAINT
    D;JEQ

// fill = 1111.1111 1111.1111
    @fill
    M=-1

(PAINT)

// address == SCREEN
    @SCREEN
    D=A
    @address
    M=D

(LOOP)
// if address == 24576 goto KEYBOARD
// SCREEN + SCREENSIZE = 24576
    @address
    D=M
    @24576
    D=D-A
    @KEYBOARD
    D;JEQ

// @address == fill
    @fill
    D=M
    @address
    A=M
    M=D

// address == address + 1
    @address
    M=M+1

// goto LOOP
    @LOOP
    0;JMP

// Program Ends.
//(END)
//    @END
//    0;JMP