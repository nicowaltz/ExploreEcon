#!/usr/bin/env python3

from random import random
import time
from math import *
import sys

ERASE=True
 
C,R=5,5 #number of columns, rows

I=C*R #number of singers

choir = []
pchoir = []
history = list()

#-- program

#- initialise the choir
def initialise():
    global choir
    global pchoir
    choir=[[0 for i in range(C)] for i in range(R)] #initialising the choir array
    pchoir=[[0 for i in range(C)] for i in range(R)]

    setup()

def run(): 
    while True:
        if strategy(): break
        time.sleep(0.4)
        print_choir(ERASE)
    

def main():
    initialise()
    print_choir(False)
    run()

    print("Iterations: %d Loss: %.4f" % (len(history), loss()))

#-- output

def print_choir(erase):
    if erase:
        for i in range(R+1): sys.stdout.write("\033[F") 
        
    for i in range(R):
        for j in range(C):
            pitch = choir[i][j]
            print(("b" if pitch<0 else ("0" if pitch==0 else "#")) + "  ",end="")
        print()
    print()
    return True
#-- helpers

#- calls the strategy of choice
def strategy():
    return discrete_monitor()

#- calls the setup function of choice
def setup():
    return discrete_random()

def loss():
    TSS=0
    ns_bar=0
    for i in range(R):
        for j in range(C):
            pitch = choir[i][j]
            ns_bar+=pitch
            TSS += pitch ** 2
    
    return TSS/I + ((ns_bar/I)**2) * (1/I - 1)

#-- game parameters

#- the "look what the people around me are doing" strategy
def discrete_monitor():
    global choir
    global history
    
    # J indexes
    # 0 1 2 
    # 7 s 3 
    # 6 5 4
   
    for i in range(R):
        for j in range(C):
            J=[None for i in range(8)]
            top = i-1 >= 0
            left = j-1 >= 0
            bottom = i+1 < R
            right = j+1 < C
            
            if top:
                J[1] = choir[i-1][j]
                if right:
                    J[2] = choir[i-1][j+1]
                    J[3] = choir[i][j+1]
                if left:
                    J[0] = choir[i-1][j-1]
                    J[7] = choir[i][j-1]
            if bottom:
                J[5] = choir[i+1][j]
                if right:
                    J[4] = choir[i+1][j+1]
                    J[3] = choir[i][j+1]
                if left:
                    J[6] = choir[i+1][j-1]
                    J[7] = choir[i][j-1]
            
            eval_dm_player(i,j,J)
           

    history.append(choir)
    if choir == pchoir: 
        
        return True

    choir = [[s for s in row] for row in pchoir]

    
    
    return False

def eval_dm_player(i,j,J):
    global pchoir
    s = choir[i][j]
    flat=0
    on=0
    sharp=0
    for k in range(8):
        if J[k] == -1:
            flat+=1
        if J[k] == 0:
            on+=1
        if J[k] == 1:
            sharp+=1

    maximum=max(flat, on, sharp)
    double = False
    result = 2
    if flat == maximum:
        double = True
        result = -1
    if on == maximum:
        result = 0
        if double:
            result = s
        double = True
    if sharp == maximum:
        result = 1
        if double:
            result = s

    pchoir[i][j]=result


def discrete_random():
    global choir
    for i in range(R):
        for j in range(C):
            choir[i][j] = int(10 * random())%3 - 1
    

if __name__=="__main__":
    main()