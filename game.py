import numpy as np
import copy
from random import randrange

"""
We will check across the diagonal top left to bottom right, 
This will allow us to check all possible solutions for a win
"""

def threecheck(board):

    
        win=False
       
       #Top Left
        if board[0]!=0:
            #Row T-L to T-R
            if board[0]==board[1]:
                #Top Right            
                if board[2]==board[1]:
                    win=True
            #Column T-L to B-L
            if board[0]==board[3]:
                
                if board[3]==board[6]:
                    win=True
                    
        #Middle center
        if board[4]!=0:
            #Diagonal T-L to B-R
            if board[4]==board[0]:
                
                if board[4]==board[8]:
                    win=True
            #Diagonal B-L to T-R
            if board[4]==board[2]:
                
                if board[4] ==board[6]:
                    win=True
            #Column T-M to B-M
            if board[4]==board[1]:
                
                if board[4] == board[7]:
                    win=True
            #Row C-L to C-R
            if board[4]==board[3]:  
                    
                if board[4]==board[5]:
                    win=True
                    
        #Bottom Right
        if board[8]!=0:
            #Column T-R to B-R
            if board[8]==board[2]:
                #Top Right            
                if board[8]==board[5]:
                    win = True
            #Row B-L to B-R
            if board[8]==board[7]:
                
                if board[8]==board[6]:
                    win=True
    
        return win

"""
This will add the Move to the board
"""

def addMove(board, turn, index):
    if turn%2==1:
        board[index]=1
    else:
        board[index]=2


def gameOver(board, turn):

    return threecheck(board) is True or turn==10

