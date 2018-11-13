#from bitstring import BitArray
#import sys
from bitstring import BitArray
import maths
import math
import random


def operatorConvert(op):
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


def numberToBinary(num, bits):                     
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


def IDGen(socket): #TODO: Used adresses
    """Generate session ID"""
    ID = BitArray()
    ID = numberToBinary(random.randrange(0, 256), 8)
    pack = packOne('+', 0, 0, ID, 1)
    print (f"Sending session ID: {pack.bin[0:3]} {pack.bin[3:35]} {pack.bin[35:37]}",
    f" {pack.bin[37:45]} {pack.bin[45:48]}")
    socket.send(pack.tobytes())
    return ID

def status(num):
    """
    Change status to binary
    00 - normal (?)
    01 - session ID
    10 - number out of range (?, posiible merge with error?)
    11 - error

    Alternative status may be: <- used at the moment
    00 - two arguments
    01 - last
    10 - ack and intermediate result(ask whether it is required since it's TCP)
    11 - more arguments <- not used
    """
    #maybe do this using enum rather than numbers
    status = BitArray(numberToBinary(num, 2))
    return status

def packTwo(op, num1, num2, stat, id, pad):
    """
    Create package
    0-2 bits: operation
    3-34 bits: first number
    35-66 bits: second number
    67-68 bits: status
    69-76 bits: session id
    77-79 bits: padding/for future use
    """
    package = BitArray(0)
    package.append(operatorConvert(op))
    package.append(numberToBinary(num1, 32))
    package.append(numberToBinary(num2, 32))
    package.append(numberToBinary(stat, 2))
    package.append(id) 
    package.append(3)
    return package

def packOne(op, num, stat, id, pad):
    """
    Create package
    0-2 bits: operation
    3-34 bits: first number
    35-36 bits: status
    37-44 bits: session id
    45-47 bits: padding/for future use
    """
    package = BitArray(0)
    package.append(operatorConvert(op))
    package.append(numberToBinary(num, 32))
    package.append(numberToBinary(stat, 2))
    package.append(id) 
    package.append(numberToBinary(pad, 3))
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
            return  0 #TODO: exception, some error code, etc
    elif op == "100":
        return a % b
    elif op == "101":
        return a**b
    elif op == "110":
        return maths.binomialTheorem(a, b)
    elif op == "111":
        return maths.percent(a, b)

def sendTwo(id, socket, st):
    """Function for creating packages for two numbers"""

    #Input for package
    op = input("Operator: ")
    while not (op == '+' or op == '-' or op == '*' or op == '/' or op == 'mod' or
    op == '^' or op == 'nck' or op == '%'):
        print("Wrong operator! Permitted operators: ",
        "+, -,  *, /, mod, ^, nck and %")
        op = input("Operator: ")

    num1 = int(input("First number: "))
    while num1 < - 2147483648 or num1 >2147483647:    
        print("Wrong number! Input integer in range ",
        "from  -2,147,483,648 to 2,147,483,647 ")
        num1 = int(input("First number: "))

    num2 = int(input("Second number: "))
    while num2 < - 2147483648 or num1 >2147483647:    
        print("Wrong number! Input integer in range ",
        "from  -2,147,483,648 to 2,147,483,647 ")
        num2 = int(input("First number: "))

    #Creating package
    pack = BitArray()
    pack = packTwo(op, num1, num2, st, id, 0)
    print (f"Sending: {pack.bin[0:3]} {pack.bin[3:35]} {pack.bin[35:67]}",
    f"{pack.bin[67:69]} {pack.bin[69:77]} {pack.bin[77:]}")

    #Send package
    socket.send(pack.tobytes())

    #Recieve package
    data = BitArray()
    data.append(socket.recv(1024))

    print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]}", 
    f"{data.bin[35:37]} {data.bin[37:45]}",
    f"{data.bin[45:]}")
    print(f"Status: {abs(data[35:37].int)}")
    if abs(data[35:37].int) == 2:
        result = data[3:35].int           
        clientID = data[37:45].bin
        if st == 1:
            print(f"Final result: {result}")
        elif st == 0:
            print(f"Intermediate result: {result}")


def sendOne(id, socket):

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

        if last == 'n':
            st = 0
            #TODO set this in pad field and give this status number session id
            #st = 0
            #pad = ?
        elif last == 'y':
            st = 1
        #Creating package
        pack = BitArray()
        pack = packOne(op, num1, st, id, 0)
        print (f"Sending: {pack.bin[0:3]} {pack.bin[3:35]} {pack.bin[35:37]}",
        f" {pack.bin[37:45]} {pack.bin[45:48]}")

        #Send package

        socket.send(pack.tobytes())

        #Recieve package
        data = BitArray()
        data.append(socket.recv(1024))

        print(f"Recieved: {data.bin[0:3]} {data.bin[3:35]}", 
        f"{data.bin[35:37]} {data.bin[37:45]} {data.bin[45:]}")
        print(f"Status: {abs(data[35:37].int)}")
        if abs(data[35:37].int) == 2:
            result = data[3:35].int           
            clientID = data[37:45].bin
            if st == 1:
                print(f"Final result: {result}")
            elif st == 0:
                print(f"Intermediate result: {result}")