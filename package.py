#from bitstring import BitArray
#import sys
from bitstring import BitArray
import maths
import math


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


def numberToBinary(num):                     
    """Convert int to binary"""
    #TODO: negative numbers
    i = 31
    print (f"Num: {num}")
    number = BitArray(32)
    while num > 0:
        if num % 2 == 1:
            number[i] = 1
        num = math.floor(num / 2)
        i-=1
    print (f"Number: {number.int}")
    return number

# def binaryToNumber(num):                     
#     """Convert binary to int"""
#     #TODO: negative numbers

#     result = 0
#     for i in range(31, 0):
#         result += num[i].int * 2 **i
#     return result

def IDGen():
    ID = BitArray(8)
    return ID

def status():
    status = BitArray(2)
    return status

def pack(op, num1, num2):
    """Create package"""
    package = BitArray(0)
    package.append(operatorConvert(op))
    package.append(numberToBinary(num1))
    package.append(numberToBinary(num2))
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
