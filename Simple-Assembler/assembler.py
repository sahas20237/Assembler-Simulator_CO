from read_file import *

R = {
    "R0" : 0,
    "R1" : 0,
    "R2" : 0,
    "R3" : 0,
    "R4" : 0,
    "R5" : 0,
    "R6" : 0,
    "FLAGS" : 7,
    "V"  : 0,
    "L"  : 0,
    "G"  : 0,
    "E"  : 0,
    "Error" : 0,
}

FLAGS = {'V': 0, 'L': 0, 'G': 0, 'E': 0}

labels = {}

var = {}

digits = '0123456789'

def stringtobinary_8bit(string):
    n = int(string)
    num = 0
    answer = ""
    while n != 0:
        if n % 2 == 1:
            answer += "1"
        else:
            answer += "0"
        n //= 2
    size = len(answer)
    value = "0"*(8-size)
    answer = answer[::-1]
    value += answer
    return value

def validreg(string):
    if string[0]=='R' and int(string[1:])<=6:
        return True
    return False

def debug(temp):
    for i in temp.keys():
        print(i +": "+ str(temp[i]))

def BinaryToDecimal(binary):
    decimal = 0
    for digit in binary: 
        decimal = decimal*2 + int(digit) 
    return decimal

def DecimalToBinary(num):
    if num >= 1:
        DecimalToBinary(num // 2)
    print(num % 2, end = '')

def stringtobinary(string):
    returnstring="000"
    num = int(string)
    ##print(num-1)
    temp=""
    while(num>0):
        temp+= str(num%2)
        num/=2
        num = int(num)
    ##print(temp)
    for i in range(len(temp)):
        returnstring+=temp[len(temp)-i-1]
    #print(returnstring[-3:])
    return returnstring[-3:]

## sparsh was here:
def add(R1,R2,R3):
    if(validreg(R1) and validreg(R2) and validreg(R3)):
        R[R1] = R[R2]+R[R3]
        print("0000000"+stringtobinary(R1[1:])+stringtobinary(R2[1:])+stringtobinary(R3[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

def sub(R1, R2, R3):
    if(validreg(R1) and validreg(R2) and validreg(R3)):
        R[R1] = R[R2]-R[R3]
        if(R[R1]<0):
            R["V"] =1
            R[R1]=0
        print("0000100"+stringtobinary(R1[1:])+stringtobinary(R2[1:])+stringtobinary(R3[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

def multiply(R1,R2,R3):
    if(validreg(R1) and validreg(R2) and validreg(R3)):
        imm = R[R2]*R[R3]
        R[R1] = R[R2]*R[R3]
        print("0011000"+stringtobinary(R1[1:]) +stringtobinary(R2[1:])+stringtobinary(R3[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

def xor(R1,R2,R3):
    if(validreg(R1) and validreg(R2) and validreg(R3)):
        R[R1] = R[R1]^R[R2]
        print("01010"+"00"+stringtobinary(R1[1:]) +stringtobinary(R2[1:])+stringtobinary(R3[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

def OR(R1,R2,R3):
    if(validreg(R1) and validreg(R2) and validreg(R3)):
        R[R1] = (R[R1])|(R[R2])
        print("01011"+"00"+stringtobinary(R1[1:]) +stringtobinary(R2[1:])+stringtobinary(R3[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

def AND(R1,R2,R3):
    if(validreg(R1) and validreg(R2) and validreg(R3)):
        R[R1] = R[R1]&R[R2]
        print("01100"+"00"+stringtobinary(R1[1:]) +stringtobinary(R2[1:])+stringtobinary(R3[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

## rahul add here: done
def move_imm(R1, imm):
    for i in imm:
        if i not in digits:
            R["Error"]=1
            print("Invalid Imm Value, At line number: ", curIndex-len(var))
            return
    # print(imm)
    imm = int(imm)
    if(validreg(R1)):
        if imm<0 or imm>255:
            print("Out of Range, At line number: ", curIndex-len(var))
            R["Error"] = 1
            return
        R[R1] = imm
        # print(imm)
        print("00010"+stringtobinary(R1[1:])+stringtobinary_8bit(imm))
    else:
        R["Error"]= 1
        print("Invalid Imm Value, At line number: ", curIndex-len(var))


def unconditionaljump(mem_add, i):
    # print("01111"+ "000" + stringtobinary_8bit(i))
    return True


def jumpiflessthan(mem_add, i):
    if R["L"]==1:
        return True
    # print("10000"+ "000" + stringtobinary_8bit(i))
    return False


def jumpifgreaterthan(mem_add, i):
    if R["G"]==1:
        return True
    # print("10001"+ "000" + stringtobinary_8bit(i))
    return False

def jumpifequalto(mem_add, i):
    if R["E"]==1:
        return True
    # print("10010"+ "000" + stringtobinary_8bit(i))
    return False

def right_shift(R1,imm):
    # print(R[R1])
    # print(imm, type(imm))
    for i in imm:
        if i not in digits:
            R["Error"]= 1
            print("Invalid Imm Type, At line number: ", curIndex-len(var))
            return
    # print(imm)
    imm = int(imm)
    # print(imm, type(imm))
    if(validreg(R1)):
        if imm<0 or imm>255:
            print("Out of Range, At line number: ", curIndex-len(var))
            R["V"]=1
            R["Error"] = 1
            return
        x = R[R1]
        for i in range(imm):
            x //= 2
        R[R1]= x
        # print(x)
        # print(R[R1])
        print("01000"+stringtobinary(R1[1:])+stringtobinary_8bit(imm))
    else:
        R["Error"]= 1
        print("Invalid Imm Value, At line number: ", curIndex-len(var))

def left_shift(R1,imm):
    for i in imm:
        if i not in digits:
            R["Error"] = 1
            print("Invalid Imm Type, At line number: ", curIndex-len(var))
            return
    # print(imm)
    imm = int(imm)
    # print(imm, type(imm))
    if(validreg(R1)):
        if imm < 0 or imm > 255:
            print("Out of Range, At line number: ", curIndex-len(var))
            R["V"] = 1
            R["Error"] = 1
            return
        x = R[R1]
        for i in range(imm):
            x *= 2
        R[R1] = x
        # print(x)
        # print(R[R1])
        print("01001"+stringtobinary(R1[1:])+stringtobinary_8bit(imm))
    else:
        R["Error"] = 1
        print("Invalid Imm Value, At line number: ", curIndex-len(var))

## sahas add here: ok
# C
# Performs reg1 = reg2
def MoveRegister(rx, ry):
    if (ry == "FLAGS"):
        R[rx] = R[ry]
        print('00011' + '00000' + stringtobinary(rx[1:]) + '111')
        return
    # if(rx[0]!="R" or ry[0]!="R"):
    #     print("Invalid Register(s), At line number: ", curIndex-len(var))
    #     R["Error"]=1
    if(validreg(rx) and validreg(ry)):
        R[rx] = R[ry]
        print('0001100000' + stringtobinary(rx[1:]) + stringtobinary(ry[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

# Performs reg3/reg4 Stores the quotient in R0 and the remainder in R1.
def Divide(rx, ry):
    if R[ry]==0:
        R["Error"] =1
        print("ERROR: Division by 0 at line number", curIndex-len(var))
        return
    if(validreg(rx) and validreg(ry)):
        R["R0"] = R[rx]//R[ry]
        R["R1"] = R[rx]%R[ry]
        print('00111' + '00000' + stringtobinary(rx[1:]) + stringtobinary(ry[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))
    # print(R['R0'])
    # print(R['R1'])

# Performs bitwise NOT of reg2. Stores the result in reg1.
def Invert(rx, ry):
    if(validreg(rx) and validreg(ry)):
        string = bin(R[ry])[2:]
        n = len(string)
        answer=""
        for i in range(n):
            if string[i]=="1":
                answer+="0"
            else:
                answer+="1"
        print('0110100000'+ stringtobinary(rx[1:])+ stringtobinary(ry[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

def stringtodecimal(string):
    n = len(string)
    num = 0
    for i in range(n):
        num*=2
        if string[i]=="1":
            num+=1
    return num

# Compares reg1 and reg2 and sets up the FLAGS register.
def Compare(rx, ry):
    if(validreg(rx) and validreg(ry)):
        if R[rx] > R[ry]:
            R["G"] = 1
        elif R[rx] < R[ry]:
            R["L"] = 1
        elif R[rx] == R[ry]:
            R["E"] = 1
        print('0111000000' + stringtobinary(rx[1:]) + stringtobinary(ry[1:]))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

#D 
# Loads data from mem_addr into reg1.
def Load(rx, memaddr, i):
    if(validreg(rx)):
        if not(memaddr in var.keys()):
            print("variable doesnt exist, At line no", curIndex - len(var))
            R["Error"]=1
            return
        R[rx] = var[memaddr]
        print('00100' + stringtobinary(rx[1:]) + stringtobinary_8bit(str(i)))
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))

# Stores data from reg1 to mem_addr.
def Store(rx, memaddr, i):
    # print(memaddr)
    if(validreg(rx)):
        if not(memaddr in var.keys()):
            print("variable doesnt exist, At line no", curIndex - len(var))
            R["Error"]=1
            return 
        print('00101' + stringtobinary(rx[1:]) + stringtobinary_8bit(str(i)))
        var[memaddr] = R[rx]
    else:
        R["Error"]= 1
        print("Invalid Register(s), At line number: ", curIndex-len(var))
        

def check_label(line,i):
    temp = line.split(":")
    if len(temp)==2:
        labels[temp[0]] = i
        return True
    return False

def check_input_label(text):
    for i, j in labels.items():
        if i == text:
            return j   
        # else:
        #     print('label to defined At line number', curIndex - len(var))
        #     print("1001100000000000")
        #     R["ERROR"] = 1
        #     break

def storevar(variable):
    if variable in var.keys():
        print("Variable already defined")
        R["Error"] = 1
    else:
        var[variable]=0

fullcode=[]
# print(fullcode)

varIndex = 0
for line in list_of_instructions:
    temp = line
    if(temp[0:3]=="var"):
        varIndex+=1
    #print(type(temp))
    islabel = check_label(temp, len(fullcode)-varIndex)
    #print(temp)
    if(temp == ""):
        continue
    if islabel:
        fullcode.append(temp.split()[1:])
    else:
        fullcode.append(temp.split())

# print(fullcode)
# debug(labels)
curIndex = 0
while(True):
    if curIndex == len(fullcode):
        print("1001100000000000")
        break
    currentcode = fullcode[curIndex]
    curIndex += 1
    #print(currentcode)
    if(len(currentcode) == 0):
        continue
    if(currentcode[0]=="hlt"):
        if(curIndex!= len(fullcode)):
            print("1001100000000000")
            print("ERROR: hlt not being used as last instruction")
            break
        else:
            print("1001100000000000")
            break
    if(currentcode[0]=="var"):
        if (len(currentcode) == 2):
            if(varIndex>=curIndex):
            #print("Store")
                storevar(currentcode[1])
            else:
                print("ERROR: Variables Not at Top, At line no", curIndex - len(var))
                print("1001100000000000")
                break
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0]=="add"):
        if(len(currentcode)==4):
            add(currentcode[1], currentcode[2], currentcode[3])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0]=="sub"):
        if(len(currentcode) == 4):
            sub(currentcode[1], currentcode[2], currentcode[3])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0]=="mul"):
        if(len(currentcode) == 4):
            multiply(currentcode[1], currentcode[2], currentcode[3])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0]=="xor"):
        if(len(currentcode) == 4):
            xor(currentcode[1], currentcode[2], currentcode[3])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0]=="or"):
        if(len(currentcode) == 4):
            OR(currentcode[1], currentcode[2], currentcode[3])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0]=="and"):
        if(len(currentcode) == 4):
            AND(currentcode[1], currentcode[2], currentcode[3])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0] == "mov"):
        # print(currentcode)
        if(len(currentcode)!=3):
            print("Registers Inadequate: Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            R["Error"]=1
            break
        if (currentcode[1] not in R.keys()) or (currentcode[2][0] != '$' and currentcode[2] not in R.keys()):
            print("Invalid Register Name/Value at line number", curIndex-len(var))
            print("1001100000000000")
            R["Error"] =1
            break
        if currentcode[2][0] == '$':
            move_imm(currentcode[1], currentcode[2][1:])  
        else:
            MoveRegister(currentcode[1], currentcode[2])
    elif currentcode[0]=="st":
        if len(currentcode)==3:
            Store(currentcode[1], currentcode[2], curIndex)
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            R["Error"]=1
    elif currentcode[0]=="ld":
        if len(currentcode)==3:
            Load(currentcode[1], currentcode[2], curIndex)
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            R["Error"]=1
    elif(currentcode[0] == 'div'):
        if(len(currentcode) == 3):
            Divide(currentcode[1], currentcode[2])
        else:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
    elif(currentcode[0] == 'not'):
        if len(currentcode)!=3:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        Invert(currentcode[1], currentcode[2])
    elif(currentcode[0] == 'cmp'):
        if len(currentcode)!=3:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        Compare(currentcode[1], currentcode[2])
    elif(currentcode[0] == 'rs'):
        # print(currentcode)
        if len(currentcode)!=3 or currentcode[2][0] != '$' or len(currentcode[2][1:]) == 0:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        right_shift(currentcode[1], currentcode[2][1:])
    elif(currentcode[0] == 'ls'):    
        if len(currentcode)!=3 or currentcode[2][0] != '$' or len(currentcode[2][1:]) == 0:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break 
        left_shift(currentcode[1], currentcode[2][1:])
    # elif(currentcode[0] == 'ls'):    
    #     if len(currentcode)!=3:
    #         print("Invalid Syntax Length, At line no", curIndex - len(var))
    #         print("1001100000000000")
    #         break
    #     left_shift(currentcode[1], int(currentcode[2][1:]))     
    elif currentcode[0] == 'jmp':
        if len(currentcode)!=2:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        s = check_input_label(currentcode[1])
        if s == None:
            print("Label Not Defined, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        print('01111' + '000' + stringtobinary_8bit(str(labels[currentcode[1]])))
    elif currentcode[0] == 'jlt':
        if len(currentcode)!=2:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        s = check_input_label(currentcode[1])
        if s == None:
            print("Label Not Defined, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        print('10000' + '000' + stringtobinary_8bit(str(labels[currentcode[1]])))
    elif currentcode[0] == 'jgt':
        if len(currentcode)!=2:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        s = check_input_label(currentcode[1])
        if s == None:
            print("Label Not Defined, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        print('10001' + '000' + stringtobinary_8bit(str(labels[currentcode[1]])))
    elif currentcode[0] == 'je':
        if len(currentcode)!=2:
            print("Invalid Syntax Length, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        s = check_input_label(currentcode[1])
        if s == None:
            print("Label Not Defined, At line no", curIndex - len(var))
            print("1001100000000000")
            break
        print('10010' + '000' + stringtobinary_8bit(str(labels[currentcode[1]])))
    else:
        print("Instruction not Valid, At line no", curIndex - len(var))
        R["Error"]=1
    if(R["Error"]==1):
        print("1001100000000000")
        break
