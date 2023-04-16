// C_PUSH constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 0
@SP
A=M-1
D=M
@THIS
M=D
@SP
M=M-1
// C_PUSH constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP pointer 1
@SP
A=M-1
D=M
@THAT
M=D
@SP
M=M-1
// C_PUSH constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP this 2
@2
D=A
@THIS
D=M+D
@R15
M=D
@SP
A=M-1
D=M
@R15
A=M
M=D
@SP
M=M-1
// C_PUSH constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_POP that 6
@6
D=A
@THAT
D=M+D
@R15
M=D
@SP
A=M-1
D=M
@R15
A=M
M=D
@SP
M=M-1
// C_PUSH pointer 0
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH pointer 1
@THAT
D=M
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
// C_PUSH this 2
@2
D=A
@THIS
A=M+D
D=M
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
// C_PUSH that 6
@6
D=A
@THAT
A=M+D
D=M
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
