// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// neg
@SP
A=M-1
M=-M
// C_PUSH constant 1
@1
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
// C_PUSH constant 32767
@32767
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
@NEG0
D;JLT
@SP
A=M-1
A=A-1
D=M
@TRUE0
D;JLT
@COMP0
D;JMP
(NEG0)
@SP
A=M-1
A=A-1
D=M
@FALSE0
D;JGT
(COMP0)
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
D=M-D
@TRUE0
D;JLT
(FALSE0)
@SP
A=M-1
A=A-1
M=0
@END0
D;JMP
(TRUE0)
@SP
A=M-1
A=A-1
M=-1
(END0)
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
// C_PUSH constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// neg
@SP
A=M-1
M=-M
// C_PUSH constant 1
@1
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
// gt
@SP
A=M-1
D=M
@NEG1
D;JLT
@SP
A=M-1
A=A-1
D=M
@FALSE1
D;JLT
@COMP1
D;JMP
(NEG1)
@SP
A=M-1
A=A-1
D=M
@TRUE1
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
D;JGT
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
// C_PUSH constant 20000
@20000
D=A
@SP
A=M
M=D
@SP
M=M+1
// neg
@SP
A=M-1
M=-M
// C_PUSH constant 1
@1
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
// C_PUSH constant 30000
@30000
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
// C_PUSH constant 20000
@20000
D=A
@SP
A=M
M=D
@SP
M=M+1
// C_PUSH constant 30000
@30000
D=A
@SP
A=M
M=D
@SP
M=M+1
// neg
@SP
A=M-1
M=-M
// C_PUSH constant 1
@1
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
// gt
@SP
A=M-1
D=M
@NEG3
D;JLT
@SP
A=M-1
A=A-1
D=M
@FALSE3
D;JLT
@COMP3
D;JMP
(NEG3)
@SP
A=M-1
A=A-1
D=M
@TRUE3
D;JGT
(COMP3)
@SP
A=M-1
D=M
@SP
A=M-1
A=A-1
D=M-D
@TRUE3
D;JGT
(FALSE3)
@SP
A=M-1
A=A-1
M=0
@END3
D;JMP
(TRUE3)
@SP
A=M-1
A=A-1
M=-1
(END3)
@SP
M=M-1
