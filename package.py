#from bitstring import BitArray
#import sys
from bitstring import BitArray
import maths
import math
import random
import errors


def operatorConvert(op): #done
    """
    Convert operator to binary
    000 - addition
    001 - subtraction
    010 - multiplication
    011 - division
    100 - modulo
    101 - power
    110 - n choose k
    111 - percent of x
    """
    operator = BitArray(3)
    if op == '+':
        return operator
    elif op == '-':
        operator.invert(2)
        return operator
    elif op == '*': 
        operator.invert(1)
        return operator
    elif op == '/':
        operator.invert([1, 2])
        return operator
    elif op == 'mod':
        operator.invert(0)
        return operator
    elif op == '^':
        operator.invert([0, 2])
        return operator
    elif op == 'nck':
        operator.invert([0, 1])
        return operator
    elif op == '%':
        operator.invert([0, 1, 2])
        return operator


def numberToBinary(num, bits):       #done              
    """Convert int to binary array with lenght bits"""
    #print (f"Num: {num}")

    #Variables
    neg = False
    i = bits - 1

    #Check if negative
    if (num < 0):
        neg = True
        num += 1
        num = abs(num)

    #Convert to bits
    number = BitArray(bits)
    while num > 0:
        if num % 2 == 1:
            number[i] = 1
        num = math.floor(num / 2)
        i-=1

    #Invert if negative
    if (neg == True):
        number.invert()
    
    #print (f"Number binary: {number.bin}")
    #print (f"Number int: {number.int}")
    return number


def IDGen(socket): #done
    """Generate session ID"""
    ID = BitArray()
    ID = numberToBinary(random.randrange(1, 256), 8)
    packg = pack('+', 0, 1, ID, 0, 0, 0)
    print (f"Sending session ID: {packg.bin[0:3]} {packg.bin[3:35]} {packg.bin[35:37]}",
    f" {packg.bin[37:45]} {packg.bin[45:48]}")
    socket.send(packg.tobytes())
    print("-------------------------------------------------------")
    return ID

def status(num): #done
    """
    Change status to binary
    00 - ack
    01 - session ID
    10 - ack with float
    11 - error
    """
    #maybe do this using enum rather than numbers
    status = BitArray(numberToBinary(num, 2))
    return status

def err(num): #done
    """
    Change number to error code
    00 - none
    01 - division by 0
    10 - number bigger than 32 bits
    11 - n choose k: k bigger than n
    """
    error = BitArray(numberToBinary(num, 2))
    return error

def desperation(num):
    # temp = BitArray(1)
    # if num == 1:
    #     temp[0] = 1
    # print (f"num: {num}")
    # print (f"temp: {temp.bin}")
    temp = BitArray(numberToBinary(num,1))
    return temp

def pack(op, num, stat, id, last, first, errors): #done
    """
    Create package
    0-2 bits: operation
    3-34 bits: first number
    35-36 bits: status
    37-44 bits: session id
    45 bit: last
    46 bit: first
    47-48: errors
    49-55: pad
    """
    package = BitArray(0)
    #print(f" operacja {operatorConvert(op).bin}")
    package.append(operatorConvert(op))     #operacja

    #print(f"  liczba {numberToBinary(num,32).bin}")
    package.append(numberToBinary(num, 32)) #liczba
    #print(" status ")
    package.append(status(stat))            #status
    #print(" id ")
    package.append(id)                      #id
    #print(" last ")
    package.append(desperation(last))       #flaga ostatni
    #print(" first ")
    package.append(desperation(first))      #flaga pierwzy
    #print(" error ")
    package.append(err(errors))             #error
    if(package.len != 56):                  #pad
        temp = BitArray(56-package.len)
        #print(f"check len: {48-package.len}")
        package.append(temp)

    
    #print (f"Debug: {package.bin[0:3]} {package.bin[3:35]} {package.bin[35:37]}",
    #            f" {package.bin[37:45]} {package.bin[45:46]} {package.bin[46:47]} {package.bin[47:]}")
    #print(f"Size:  {package.len}")

    return package

def countTwo(op, a, b):
    """
    Returns result of operation 
    000 - addition
    001 - subtraction
    010 - multiplication
    011 - division
    100 - modulo
    101 - power
    110 - n choose k
    111 - percent of x
    """
    if op == "000" :
        return a + b
    elif op == "001":
        return  a - b
    elif op == "010":
        return  a * b
    elif op == "011":
        if b != 0:
            return  a / b
        else:
            raise errors.DivisionByZeroException("1")
    elif op == "100":
        return a % b
    elif op == "101":
        return a**b
    elif op == "110":
        if b > a:
            raise errors.BinomalTheoremException("3")
        else: 
            return maths.binomialTheorem(a, b)
    elif op == "111":
        return maths.percent(a, b)

def sendFirst(id, socket, error):
    #Input
    num1 = int(input("Number: "))
    while num1 < - 2147483648 or num1 >2147483647:    
        print("Wrong number! Input integer in range ",
        "from  -2,147,483,648 to 2,147,483,647 ")
        num1 = int(input("First number: "))
    
    #Pack
    packg = BitArray()
    packg = pack("+", num1, 0, id, 0, 1, 0)

    #Send package
    print (f"Sending first:  {packg.bin[0:3]} {packg.bin[3:35]} {packg.bin[35:37]}",
        f" {packg.bin[37:45]} {packg.bin[45:46]} {packg.bin[46:47]} {packg.bin[47:]}")
    
    socket.send(packg.tobytes())

    #Recieve package
    data = BitArray()
    data.append(socket.recv(1024))
    
    print (f"Recieved first: {data.bin[0:3]} {data.bin[3:35]} {data.bin[35:37]}",
        f" {data.bin[37:45]} {data.bin[45:46]} {data.bin[46:47]} {data.bin[47:]}")
    print("Sending next")

def sendPackage(id, socket):

    last = 'n'
    while not (last ==  'y'):
        op = input("Operator: ")
        while not (op == '+' or op == '-' or op == '*' or op == '/' or op == 'mod' or
        op == '^' or op == 'nck' or op == '%'):
            print("Wrong operator! Permitted operators: ",
            "+, -,  *, /, mod, ^, nck and %")
            op = input("Operator: ")

        num1 = int(input("Number: "))
        while num1 < - 2147483648 or num1 >2147483647:    
            print("Wrong number! Input integer in range ",
            "from  -2,147,483,648 to 2,147,483,647 ")
            num1 = int(input("First number: "))

        last = input("Is this last operation? (y/n) ")
        while not (last == 'y' or last == 'n'):
            print("Wrong answer! Permitted answers: ",
            "y and n")
            last = input("Is this last operation? (y/n) ")

        if last == 'n':
            lastf = 0
        elif last == 'y':
            lastf = 1

        #Creating package
        packg = BitArray()
        packg = pack(op, num1, 0, id, lastf, 0, 0)
        print (f"Sending:  {packg.bin[0:3]} {packg.bin[3:35]} {packg.bin[35:37]}",
            f" {packg.bin[37:45]} {packg.bin[45:46]} {packg.bin[46:47]} {packg.bin[47:]}")

        #Send package

        socket.send(packg.tobytes())

        #Recieve package
        data = BitArray()
        data.append(socket.recv(1024))

        print (f"Recieved: {data.bin[0:3]} {data.bin[3:35]} {data.bin[35:37]}",
            f" {data.bin[37:45]} {data.bin[45:46]} {data.bin[46:47]} {data.bin[47:]}")

        print(f"Status: {abs(data[35:37].uint)}")
        st = abs(data[35:37].uint)
        lastf = int(data[45])
        result = data[3:35].int
        

        #Errors
        if st == 3:
            err = data[47:49].uint
            if err == 1:
                print(f"Error ({err}): division by zero")
                last = 'y'
            elif err == 2:
                print(f"Error ({err}): number is bigger than 32 bits")
                last = 'y'
            elif err == 3:
                print(f"Error ({err}): in binomal theorem k can't be bigger than n")
                last = 'y'
        #Float
        elif st == 2:
            if lastf == 1:
                print(f"Final result is float and equals aproximately: {result}")
            elif lastf == 0:
                print(f"Intermediate result is float and equals aproximately: {result}")
        #Normal
        elif st == 0:
            if lastf == 1:
                print(f"Final result: {result}")
            elif lastf == 0:
                print(f"Intermediate result: {result}")
                



