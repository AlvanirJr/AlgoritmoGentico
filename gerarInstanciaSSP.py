'''
lenString representa o tamanho da string a ser gerada
'''

from random import *

def generateSSP_Instance(lenString = 1000, numStringCp = 10, minLen = 50, maxLen = 60):
    instance = []
    sigma = ['a','c','g','t']

    string = ""    
    for i in range(lenString):
        letter = randint(0,3)
        string += sigma[letter]

    stringCp = ""
    for i in range(numStringCp):
        stringCp += string
    numFrag = len(stringCp)/((minLen + maxLen)/2)

    cutInit = 0
    for i in range(numFrag):
        cutFinal = randint(minLen + cutInit, maxLen + cutInit)
        s = stringCp[cutInit:cutFinal]
        cutInit = cutFinal
        instance.append(s)

    while(len(instance[-1]) < minLen):
        instance.pop(-1)
        
    return instance,stringCp
        
#usar "".find(sub)
