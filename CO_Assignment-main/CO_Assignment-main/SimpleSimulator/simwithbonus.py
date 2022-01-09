import matplotlib.pyplot as plt
from read_file import list_of_instructions
R = {
    "R0": 0,
    "R1": 0,
    "R2": 0,
    "R3": 0,
    "R4": 0,
    "R5": 0,
    "R6": 0,
    "FLAGS": 7,
    "V": 0,
    "L": 0,
    "G": 0,
    "E": 0,
    "Error": 0,
}

FLAGS = {'V': 0, 'L': 0, 'G': 0, 'E': 0}

labels = {}

variables = {}

int_max = 1 << 16


def putflag():
    n = R["L"]
    n *= 10
    n = R["G"]
    n *= 10
    n = R["E"]
    return n


def printregister():
    print(DecimalToBinary_8bit(curIndex), end=" ")
    for i in R:
        if(i == "FLAGS"):
            break
        else:
            print(DecimalToBinary_16bit(R[i]), end=" ")
    flag = False
    print('000000000000', end="")
    for i in R:
        if(i == "FLAGS"):
            flag = True
            continue
        if(i == 'Error'):
            break
        if flag == True:
            print(R[i], end="")
    print()
    return


def converter(n):
    answer = 0
    while(n != 0):
        answer *= 2
        answer += n % 10
        n //= 10
    return answer


def DecimalToBinary_8bit(n):
    string = ""
    answer = ""
    while(n != 0):
        temp = n % 2
        n //= 2
        string += str(temp)
    n = len(string)
    for i in range(8-n):
        answer += '0'
    string = string[::-1]
    for i in string:
        answer += i
    return answer


def DecimalToBinary_16bit(n):
    string = ""
    answer = ""
    while(n != 0):
        temp = n % 2
        n //= 2
        string += str(temp)
    n = len(string)
    for i in range(16-n):
        answer += '0'
    string = string[::-1]
    for i in string:
        answer += i
    return answer


def debug(temp):
    for i in temp.keys():
        print(i + ": " + str(temp[i]))


def BinaryToDecimal(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal


def stringtobinary(string):
    returnstring = "000"
    num = int(string)
    ##print(num-1)
    temp = ""
    while(num > 0):
        temp += str(num % 2)
        num /= 2
        num = int(num)
    ##print(temp)
    for i in range(len(temp)):
        returnstring += temp[len(temp)-i-1]
    #print(returnstring[-3:])
    return returnstring[-3:]


def stringtoint(string):
    n = 0
    for i in string:
        n *= 2
        n += int(i)
    return n


def add(R1, R2, R3):
    r1 = stringtoint(R1)
    r2 = stringtoint(R2)
    r3 = stringtoint(R3)
    for i in R:
        if(r1 == 0):
            for j in R:
                if(r2 == 0):
                    for k in R:
                        if(r3 == 0):
                            R[i] = R[j]+R[k]
                            if R[i]//int_max >= 1:
                                R["V"] = 1
                                FLAGS["V"]=2
                            R[i] = R[i] % int_max
                            break
                        else:
                            r3 -= 1
                    break
                else:
                    r2 -= 1
            break
        else:
            r1 -= 1


def sub(R1, R2, R3):
    r1 = stringtoint(R1)
    r2 = stringtoint(R2)
    r3 = stringtoint(R3)
    for i in R:
        if(r1 == 0):
            for j in R:
                if(r2 == 0):
                    for k in R:
                        if(r3 == 0):
                            R[i] = R[j]-R[k]
                            if R[i] < 0:
                                R["V"] = 1
                                FLAGS["V"]=2
                                R[i] = 0
                            break
                        else:
                            r3 -= 1
                    break
                else:
                    r2 -= 1
            break
        else:
            r1 -= 1


def multiply(R1, R2, R3):
    r1 = stringtoint(R1)
    r2 = stringtoint(R2)
    r3 = stringtoint(R3)
    for i in R:
        if(r1 == 0):
            for j in R:
                if(r2 == 0):
                    for k in R:
                        if(r3 == 0):
                            R[i] = R[j]*R[k]
                            if R[i]//int_max >= 1:
                                R["V"] = 1
                                FLAGS["V"]=2
                            R[i] = R[i] % int_max
                            break
                        else:
                            r3 -= 1
                    break
                else:
                    r2 -= 1
            break
        else:
            r1 -= 1


def xor(R1, R2, R3):
    r1 = stringtoint(R1)
    r2 = stringtoint(R2)
    r3 = stringtoint(R3)
    for i in R:
        if(r1 == 0):
            for j in R:
                if(r2 == 0):
                    for k in R:
                        if(r3 == 0):
                            R[i] = R[j] ^ R[k]
                            break
                        else:
                            r3 -= 1
                    break
                else:
                    r2 -= 1
            break
        else:
            r1 -= 1


def OR(R1, R2, R3):
    r1 = stringtoint(R1)
    r2 = stringtoint(R2)
    r3 = stringtoint(R3)
    for i in R:
        if(r1 == 0):
            for j in R:
                if(r2 == 0):
                    for k in R:
                        if(r3 == 0):
                            R[i] = R[j] | R[k]
                            break
                        else:
                            r3 -= 1
                    break
                else:
                    r2 -= 1
            break
        else:
            r1 -= 1


def AND(R1, R2, R3):
    r1 = stringtoint(R1)
    r2 = stringtoint(R2)
    r3 = stringtoint(R3)
    for i in R:
        if(r1 == 0):
            for j in R:
                if(r2 == 0):
                    for k in R:
                        if(r3 == 0):
                            R[i] = R[j] & R[k]
                            break
                        else:
                            r3 -= 1
                    break
                else:
                    r2 -= 1
            break
        else:
            r1 -= 1
        # assembler.append("Invalid Register")

## rahul add here: done


def move_imm(R1, imm):
    r1 = stringtoint(R1)
    imm_val = stringtoint(imm)
    for i in R:
        if(r1 == 0):
            R[i] = imm_val
            break
        else:
            r1 -= 1
        # assembler.append("Invalid Register")


def right_shift(R1, imm):
    r1 = stringtoint(R1)
    imm = stringtoint(imm)
    for i in R:
        if(r1 == 0):
            x = R[i]
            for j in range(imm):
                x //= 2
            R[i] = x
            return
        else:
            r1 -= 1



def left_shift(R1, imm):
    r1 = stringtoint(R1)
    imm = stringtoint(imm)
    for i in R:
        if(r1 == 0):
            x = R[i]
            for j in range(imm):
                x *= 2
            R[i] = x
            return
        else:
            r1 -= 1


## sahas add here: ok
# C
# Performs reg1 = reg2
def MoveRegister(rx, ry):
    r1 = stringtoint(rx)
    r2 = stringtoint(ry)
    #print(r1,r2)
    if(r2 == 7):
        for i in R:
            if(r1 == 0):
                #debug(R)
                R[i] = R["E"] + 10*R["G"] + 100*R["L"]
                break
            else:
                r1 -= 1

        return
    KEYS = []
    VALS = []
    for i, j in R.items():
        KEYS.append(i)
        VALS.append(j)
    # print(KEYS, VALS)
    VALS[r1] = VALS[r2]
    for i in KEYS:
        for j in VALS:
            R[i] = j
            VALS.remove(j)
            break
    # print(KEYS, VALS)
    #debug(R)


# Performs reg3/reg4 Stores the quotient in R0 and the remainder in R1.
def Divide(rx, ry):
    r1 = stringtoint(rx)
    r2 = stringtoint(ry)
    KEYS = []
    VALS = []
    for i, j in R.items():
        KEYS.append(i)
        VALS.append(j)
    # print(KEYS, VALS)
    x = VALS[r1]//VALS[r2]
    y = VALS[r1] % VALS[r2]
    # print(VALS)
    VALS[1] = y
    VALS[0] = x
    # print(VALS)
    for i in KEYS:
        for j in VALS:
            R[i] = j
            VALS.remove(j)
            break
    # print(KEYS, VALS)


# Performs bitwise NOT of reg2. Stores the result in reg1.
def Invert(rx, ry):
    r1 = stringtoint(rx)
    r2 = stringtoint(ry)
    KEYS = []
    VALS = []
    for i, j in R.items():
        KEYS.append(i)
        VALS.append(j)
    temp = (1 << 16) - 1
    VALS[r1] = VALS[r2] ^ temp
    # print(KEYS, VALS)
    for i in KEYS:
        for j in VALS:
            R[i] = j
            VALS.remove(j)
            break
    # print(KEYS, VALS)


# Compares reg1 and reg2 and sets up the FLAGS register.
def Compare(rx, ry):
    r1 = stringtoint(rx)
    r2 = stringtoint(ry)
    KEYS = []
    VALS = []
    for i, j in R.items():
        KEYS.append(i)
        VALS.append(j)
    # print(KEYS, VALS)
    if VALS[r1] > VALS[r2]:
        VALS[10] = 1
        R["G"] = 1
        FLAGS["G"] = 2
    elif VALS[r1] < VALS[r2]:
        VALS[9] = 1
        R["L"] = 1
        FLAGS["L"] = 2
    elif VALS[r1] == VALS[r2]:
        VALS[11] = 1
        R["E"] = 1
        FLAGS["E"] = 2

    # print(KEYS, VALS)
    for i in KEYS:
        for j in VALS:
            R[i] = j
            VALS.remove(j)
            break
    # print(KEYS, VALS)
    # print(FLAGS)


#D
# Loads data from mem_addr into reg1.
def Load(rx, memaddr):
    r1 = stringtoint(rx)
    KEYS = []
    VALS = []
    for i, j in R.items():
        KEYS.append(i)
        VALS.append(j)
    # print(KEYS, VALS)
    # print(r2)
    VALS[r1] = variables[memaddr]
    # print(KEYS, VALS)
    for i in KEYS:
        for j in VALS:
            R[i] = j
            VALS.remove(j)
            break


# Stores data from reg1 to mem_addr.
def Store(rx, temp):
    r1 = stringtoint(rx)
    for i in R:
        if(r1 == 0):
            variables[temp] = R[i]
            break
        else:
            r1 -= 1


def reduce():
    for i in FLAGS:
        if FLAGS[i] == 2:
            FLAGS[i] = 1
        elif FLAGS[i] == 1:
            FLAGS[i] = 0
            R[i] = 0


def check_label(line, i):
    temp = line.split(":")
    # print(temp)
    if len(temp) == 2:
        labels[temp[0]] = i
        return True
    return False


fullcode = []
for line in list_of_instructions:
    temp = line
    fullcode.append(temp)

listofcurIndex = []
listofprogramcounter = []
#print(fullcode)
curIndex = -1
programcounter = -1
# counter = 50
while(True):
    printed = False
    curIndex += 1
    currentcode = fullcode[curIndex]
    programcounter += 1
    listofcurIndex.append(curIndex)
    listofprogramcounter.append(programcounter)
    """ print(curIndex)
    print(currentcode) """
    if(currentcode == '1001100000000000'):
        reduce()
        printregister()
        break
    """ if(counter==0):
        break
    counter-=1 """
    #debug(R)
    if(currentcode[0:5] == "00000"):
        add(currentcode[7:10], currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == "00001"):
        sub(currentcode[7:10], currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == "00110"):
        multiply(currentcode[7:10], currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == "01010"):
        xor(currentcode[7:10], currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == "01011"):
        OR(currentcode[7:10], currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == "01100"):
        AND(currentcode[7:10], currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == "00010"):
        move_imm(currentcode[5:8], currentcode[8:16])
    elif(currentcode[0:5] == "00011"):
        MoveRegister(currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == '00111'):
        Divide(currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == '01101'):
        Invert(currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == '01110'):
        Compare(currentcode[10:13], currentcode[13:16])
    elif(currentcode[0:5] == '01000'):
        right_shift(currentcode[5:8], currentcode[8:16])
    elif(currentcode[0:5] == '01001'):
        left_shift(currentcode[5:8], currentcode[8:16])
    elif (currentcode[0:5] == '01111'):
        printed = True
        reduce()
        printregister()
        #print(type(stringtoint(currentcode[8:16])), int(currentcode[8:16]))
        curIndex = stringtoint(currentcode[8:16])-1
    elif(currentcode[0:5] == '10001'):
        printed = True
        checker = False
        if(R["G"] == 1):
            checker = True
        reduce()
        printregister()
        if(checker == True):
            curIndex = stringtoint(currentcode[8:16])-1
    elif(currentcode[0:5] == '10010'):
        printed = True
        checker = False
        if(R["E"] == 1):
            checker = True
        reduce()
        printregister()
        if(checker == True):
            curIndex = stringtoint(currentcode[8:16])-1
    elif(currentcode[0:5] == '10000'):
        printed = True
        checker = False
        if(R["L"] == 1):
            checker = True
        reduce()
        printregister()
        if(checker == True):
            curIndex = stringtoint(currentcode[8:16])-1
    elif(currentcode[0:5] == '00101'):
        Store(currentcode[5:8], currentcode[8:16])
        listofcurIndex.append(stringtoint(currentcode[8:16]))
        listofprogramcounter.append(programcounter)
    elif(currentcode[0:5] == '00100'):
        Load(currentcode[5:8], currentcode[8:16])
    # print(curIndex)
    if(printed == False):
        reduce()
        printregister()

for i in fullcode:
    print(i)
for i in variables:
    # listofcurIndex.append(variables[i])
    print(DecimalToBinary_16bit(variables[i]))
for i in range(256-len(fullcode)-len(variables)):
    print('0000000000000000')

plt.scatter(listofprogramcounter, listofcurIndex, s= 100, c= 'cyan')
# ,xlim=(0,max(listofcurIndex)),ylim = (0,max(listofprogramcounter))
plt.title("Memory Access Trace")
plt.xlabel("Cycle Number")
plt.ylabel("Memory Address")
# plt.xlim(0, 30)
# plt.ylim(0, 30)
plt.show()
