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


def IDGen(): #TODO: Used adresses
    """Generate session ID"""
    ID = BitArray(0)
    ID = numberToBinary(random.randrange(0, 256), 8)
    return ID

def status():
    """Change status to binary"""
    status = BitArray(2)
    return status

def pack(op, num1, num2):
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
    package.append(status())
    package.append(IDGen()) 
    package.append(3)
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
