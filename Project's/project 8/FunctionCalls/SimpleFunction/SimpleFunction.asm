(SimpleFunction.test)
@SP
D=M
@LCL
M=D
@SP
M=M+1
A=M-1
M=0
@SP
M=M+1
A=M-1
M=0
// C_PUSH local 0
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH local 1
@1
D=A
@LCL
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
// not
@SP
A=M-1
M=!M
// C_PUSH argument 0
@0
D=A
@ARG
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
// C_PUSH argument 1
@1
D=A
@ARG
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
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
// C_POP argument 0
@0
D=A
@ARG
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
@ARG
D=M+1
@SP
M=D
@R13
M=M-1
A=M
D=M
@THAT
M=D
@R13
M=M-1
A=M
D=M
@THIS
M=D
@R13
M=M-1
A=M
D=M
@ARG
M=D
@R13
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP
