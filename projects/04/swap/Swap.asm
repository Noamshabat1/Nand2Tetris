// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in curr_ptr, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in curr_ptr is at least >= 2048
// - curr_ptr + R15 <= 16383
//
// Requirements:
// - Changing curr_ptr, R15 is not allowed.

// if R15 == 0 goto END
    @R15
    D=M
    @END // @69
    D;JEQ

// Setting curr_ptr to be a pointer to the last element in our array
// Then setting BIGGEST.ptr and SMALLEST.ptr to be pointers to the last element in the array
    @R14
    D=M
    @curr_ptr //@16
    M=D
    @R15
    D=M
    @curr_ptr //@16
    M=M+D
    M=M-1

    D=M
    @BIGGEST.ptr // @17
    M=D
    @SMALLEST.ptr // @18
    M=D


// array length == R15
    @R15
    D=M
    @array_len // @19
    M=D

// while array_len > 0, keep on checking BIGGEST.ptr and SMALLEST.ptr
(LOOP)
    // If array_len is <= 0 we've check all of the array items, so we jump to SWAP
    @array_len // @19 decress the len by 1
    M=M-1
    D=M
    @SWAP
    D;JLE

    // ITERATION
    // decress the address by 1
    @curr_ptr // @16  
    M=M-1

    // getting the biggest current value
    @BIGGEST.ptr // @17  
    A=M
    D=M

    // Calculating ((old biggest) - current_item)
    @curr_ptr // @16 
    A=M
    D=D-M

    // If D < 0, we want to set a new biggest, else, continue
    @AFTER_SWAP_BIGGEST // @41 
    D;JGE

    // Setting BIGGEST.ptr = current_ptr
    @curr_ptr // @16
    D=M

    @BIGGEST.ptr // @17
    M=D

(AFTER_SWAP_BIGGEST)

    // getting the smallest current value
    @SMALLEST.ptr // @18
    A=M
    D=M

    // Calculating ((old smallest) - current_item)
    @curr_ptr //@16
    A=M
    D=D-M

    // If D > 0, we want to set a new smallest, else, continue
    @AFTER_SWAP_SMALLEST // @53
    D;JLE

    // Setting SMALLEST.ptr = current_ptr
    @curr_ptr // @16
    D=M

    @SMALLEST.ptr // @18
    M=D

// start new ITERATION
(AFTER_SWAP_SMALLEST)
    
    @LOOP
    0;JMP

// swap
(SWAP)
    // x, y
    // x=x+y
    // y=x-y
    // x=x-y

    // x=x+y
    @BIGGEST.ptr // @17
    A=M
    D=M // y

    @SMALLEST.ptr // @18
    A=M
    M=M+D // x=x+y

    // y=x-y
    @SMALLEST.ptr
    A=M
    D=M

    @BIGGEST.ptr
    A=M
    M=D-M

    // x=x-y
    @BIGGEST.ptr
    A=M
    D=M

    @SMALLEST.ptr
    A=M
    M=M-D

// Program Ends.
(END)
    @END // @69
    0;JMP