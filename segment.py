#from bitstring import BitArray
#import sys
from bitstring import BitArray


def Operator(op):
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
        #operator[1] = 1
        #operator[2] = 1
        return operator
    elif op == '%':
        operator.invert(0)
        return operator

def Number(num):
    #number = bin(num)
    #print(f"Liczba binarna = {number}")
    #number = str(number)
    #print(f"Liczba binarna = {number}")
    #return number
    i = 15
    
    number = BitArray(16)
    while num > 0:
        if num % 2 == 1:
            number[i] = 1
        num = round(num / 2)
        i-=1
    return number