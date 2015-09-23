import numpy as np
import copy
from random import randrange

import game.py
import arena.py
import gym.py
import  winningPercent.py

"""

Piece State,
0 = Empty
1 = X
2 = O

  0  |  1  |  2  
  ---------------
  3  |  4  |  5
  ---------------
  6  |  7  |  8
"""  
  
"""
This will check if the current state exists,

IF YES: return index of it
IF NO: return -1
"""
        
def stateChecker(states, board):
    index=-1    
    i=0
    
    while i<len(states) and index==-1:
        match=True
        j=0
        while j<9 and match is True:
            if states[i][j]!=board[j]:
                match=False
            j+=1
        if match is True:
            index=i
        
        i+=1
    

    return index



"""This will start us cranking out all possible states    """    
               
def createAllPossibleStates(states, R, t):

            
            board=[0,0,0,0,0,0,0,0,0]
            states.append(board)
            createAllStates(states,R, t,board, 1, -1, -1 , False,)
            print "Woe, that was tough!"
            
                    
    	
    
def createAllStates(states, R, t, board, turn, previousState, previousMove, GameOver):

    currentState=copy.deepcopy(len(states)-1)
    #prevMove=copy.deepcopy(previousMove)
    #prevState=copy.deepcopy(previousState)
        
    newTurn=copy.deepcopy(turn)
    #playerThatWon=copy.deepcopy(winningPlayer)
    R.append([0.,0.,0.,0.,0.,0.,0.,0.,0.])
    t.append([0,0,0,0,0,0,0,0,0])

    """
    if turn==10:
	#print "DRAW"
	R.append([-1,-1,-1,-1])
	return 
    """
    for i in range(0,9):
	currentMove=copy.deepcopy(i)
	
	#Check for empty square
	if board[i]==0:

	    newBoard=copy.deepcopy(board)  
	    game.addMove(newBoard, turn, i)
		
	    gameOv=copy.deepcopy(GameOver)
	    #if gameOv is True:
	    #   if newTurn%2==playerThatWon%2:
	    #        R[currentState][i]=100.0
	    
	    if game.threecheck(newBoard) is True and gameOv is False:
		R[currentState][i]=100.0
		gameOv=True
		#winningPlayer=newTurn%2
		
		
		#we need to alter the reward from previous movement to reflect a loss
		#R[prevState][prevMove]=-100.0
		
	    #If the game is not over, the last player puts a piece down to draw
		
	    elif game.threecheck(newBoard) is False and gameOv is False and turn==9:
		#R[prevState][prevMove]=25
		R[currentState][i]=25
		gameOv=True
		
	    #Here we will find if we will be at a previously                             
	    check=stateChecker(states, newBoard)
		    
	    if check==-1: #If this is a board we have not seen
		
		states.append(newBoard) 
		t[currentState][currentMove]=len(states)-1
		    
		#Go to next state from current move
		#We will have to send the info for current state and move in case it results in a direct loss
	       
				    
		createAllStates(states,R, t, newBoard,newTurn+1, currentState, currentMove, gameOv)
	    
	    else: 
	        # if this is, all we will ahve to do is append the INDEX FOR THE next state
		# This will allow us to quickly jump to that state.
		
		t[currentState][currentMove]=check
	
	#IF the square is taken, we can not place a piece there 
	#so there is not corresponding cation or reward
	else:
	    
	    R[currentState][currentMove]=-np.inf
	    t[currentState][currentMove]=-1



def setQNoBacktrack(Q,t):
    for i in range (len(t)):
        for j in range (len(t[0])):
            if t[i][j]==-1:
                Q[i,j]=-np.inf
                

    
                
#-------------------------------------------------------------------------------------------

"""
States holds all boards
R holds all rewards
t holds list of actions, and location of state following action

"""
states=[]
R=[]
t=[]


print "Loading states, please wait."
createAllPossibleStates(states, R, t)


#nStates= np.shape(R)[0]
#print nStates 

print "Time to get to the gym, brb."
Qrand1 = trainingAgainstRand1(states,t)
Qrand2 = trainingAgainstRand2(states,t)



QQ=trainingAgainstLearner(states, t)
Qplayer1=QQ[0]
Qplayer2=QQ[1]

# ****** If you want to calculate winning percentages of the learners, enable the next line**********
winningPercentages.winningPercent(QQ, Qrand1, Qrand2, t, states)



#-----------------------------------------------------------------------------------------------------------
#	This section is a user menu that allows the 
#	user to determine if they want two trained 
#	computers to battle, or play against the super computer


mode=0
while mode!=3:
    print "Would you like:"
    print "1. Two computers to battle to the death"
    print "2. Play against the super computer"
    print "3. Quit"

    mode=int(raw_input('Input:'))

    if mode==1:
        print "You selected two computers"
    
        arena.TwoComputers(QRand1,QRand2, t,states, Comp1Win,RandWin,Draw)
        print ""
        print ""

    elif mode==2:
        print "So you want to play?"
        print ""
        print ""
    
        arena.soIHearYouLikeToPlay(Q, states)
    elif mode!=3:
        print "Invalid Response"
        print ""
        print""
    
print "done"

