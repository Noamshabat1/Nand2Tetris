// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
M=-1
@END0
D;JEQ
@SP
A=M-1
M=0
(END0)
// C_PUSH constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// lt
@SP
A=M-1
D=M
@NEG1
D;JLT
@SP
A=M-1
A=A-1
D=M
@TRUE1
D;JLT
@COMP1
D;JMP
(NEG1)
@SP
A=M-1
A=A-1
D=M
@FALSE1
D;JGT
(COMP1)
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
D=M-D
@TRUE1
D;JLT
(FALSE1)
@SP
A=M-1
A=A-1
M=0
@END1
D;JMP
(TRUE1)
@SP
A=M-1
A=A-1
M=-1
(END1)
@SP
M=M-1
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
A=M-1
D=M
@NEG2
D;JLT
@SP
A=M-1
A=A-1
D=M
@FALSE2
D;JLT
@COMP2
D;JMP
(NEG2)
@SP
A=M-1
A=A-1
D=M
@TRUE2
D;JGT
(COMP2)
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
D=M-D
@TRUE2
D;JGT
(FALSE2)
@SP
A=M-1
A=A-1
M=0
@END2
D;JMP
(TRUE2)
@SP
A=M-1
A=A-1
M=-1
(END2)
@SP
M=M-1
// C_PUSH constant 56
@56
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
// C_PUSH constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=-M
A=A-1
M=D+M
// neg
@SP
A=M-1
M=-M
// and
@SP
M=M-1
A=M
D=M
A=A-1
M=D&M
// C_PUSH constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M
