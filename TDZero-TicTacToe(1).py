
"""
TO DO:

Make draws worth points, 
possibly make second reward vector so that it chooses the best option for itself.

"""


import numpy as np
import copy
from random import randrange



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

"""
This will add the Move to the board
"""

def addMove(board, turn, index):
    if turn%2==1:
        board[index]=1
    else:
        board[index]=2

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
	    addMove(newBoard, turn, i)
		
	    gameOv=copy.deepcopy(GameOver)
	    #if gameOv is True:
	    #   if newTurn%2==playerThatWon%2:
	    #        R[currentState][i]=100.0
	    
	    if threecheck(newBoard) is True and gameOv is False:
		R[currentState][i]=100.0
		gameOv=True
		#winningPlayer=newTurn%2
		
		
		#we need to alter the reward from previous movement to reflect a loss
		#R[prevState][prevMove]=-100.0
		
	    #If the game is not over, the last player puts a piece down to draw
		
	    elif threecheck(newBoard) is False and gameOv is False and turn==9:
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
                
        
                
"""

Here we will train the Rewards function
 
"""  
def trainingAgainstRand1(states, t):
    nStates = np.shape(t)[0]
    nActions = np.shape(t)[1]
    
    Q = np.zeros((nStates,nActions))
    numberOfTimesStateVisted = np.zeros((nStates))
    setQNoBacktrack(Q,t)

    mu = 0.7
    gamma = 0.25
    epsilon = .15
    epsilon2 = 1

    nits = 0
    
    TDWinns=0
    TDDraww=0
    TDLosss=0
    while nits < 1000000:
        # Pick initial state
        s = 0
        # Stop when the accepting state is reached
        turn=0
        while threecheck(states[s]) is False and turn<8:
                       
        # epsilon-greedy
            
            if (np.random.rand()<epsilon):

                indices=[]
                for i in range(0,9):
                    if t[s][i]>-1:
                        indices.append(i)
                    
                pick = randrange(len(indices))
                a = indices[pick]
            else:
                a = np.argmax(Q[s,:])

            sprime = t[s][a]
            numberOfTimesStateVisted[sprime]+=1
            turn+=1
            
            #If this move wins us the game
            if threecheck(states[sprime]) is True:
                Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (100 + gamma*np.max(Q[sprime,:]) - Q[s,a])
                TDWinns= TDWinns+1
                s=sprime
                
            elif turn==8:
                TDDraww+=1
            #If not, let the computer pick
            else:
                Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (gamma*np.max(Q[sprime,:]) - Q[s,a])
		
		# Have the computer chooses a random action -> epsilon2 = 1
                if (np.random.rand()<epsilon2):
                
		    #we need to chose a random action
                    indices=[]
                    for i in range(0,9):
                        if t[sprime][i]>-1:
                            indices.append(i)
                    
                    pick = randrange(len(indices))
                    a2 = indices[pick]
		    
        		   #a is the index of the next state to move to    
                else:
                    a2 = np.argmax(Q[sprime,:])
                """
                if threecheck(board) is True:
                    Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (r + gamma*np.min(Q[sprime,np.where(t[s,:]>-1)]) - Q[s,a])
                """
                sDoublePrime = t[sprime][a2]
                if threecheck(states[sDoublePrime]):
                    r=-100.
                else:
                    r=0
		
        		
                Q[sprime,a2] += mu/(numberOfTimesStateVisted[sDoublePrime]+1) * (r + gamma*np.max(Q[sDoublePrime,:]) - Q[sprime,a2])
                numberOfTimesStateVisted[sDoublePrime]+=1            
                s = sDoublePrime
                turn+=1
                
                if threecheck(states[s])is True:
                    TDLosss+=1
                elif turn ==8:
                    TDDraww+=1


	

        nits = nits+1
        if nits%100==0:
            TDWinPercentageTrainingFirst.append(TDWinns/float(nits))
            TDDrawPercentageTrainingFirst.append(TDDraww/float(nits))	
            TDLossPercentageTrainingFirst.append(TDLosss/float(nits))
        
    return Q
    #print Q[0]
    

def trainingAgainstRand2(states, t):
    nStates = np.shape(t)[0]
    nActions = np.shape(t)[1]
    
    Q = np.zeros((nStates,nActions))
    numberOfTimesStateVisted = np.zeros((nStates))
    setQNoBacktrack(Q,t)

    mu = 0.7
    gamma = 0.25
    epsilon = 1
    epsilon2 = .15
    nits = 0
    
    TDWins=0
    TDDraw=0
    TDLoss=0
    while nits < 1000000:
        # Pick initial state
        s = 0
        # Stop when the accepting state is reached
        turn=0
        while threecheck(states[s]) is False and turn<8:
                       
        # epsilon-greedy
            
            if (np.random.rand()<epsilon):
                """
                we need to chose a random action
                
                """
                indices=[]
                for i in range(0,9):
                    if t[s][i]>-1:
                        indices.append(i)
                    
                pick = randrange(len(indices))
                a = indices[pick]
                """
                a is the index of the next state to move to
                """
                    
                #print s,a
            else:
                a = np.argmax(Q[s,:])

            # For this example, new state is the chosen action
            sprime = t[s][a]
            numberOfTimesStateVisted[sprime]+=1 
            turn+=1
            
            #If this move wins us the game
            if threecheck(states[sprime]) is True:
                Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (-100 + gamma*np.max(Q[sprime,:]) - Q[s,a])
                TDLoss+=1
                s=sprime
            elif turn==8:
                Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (20 + gamma*np.max(Q[sprime,:]) - Q[s,a])
                TDDraw+=1
            #If not, let the computer pick
            else:
                Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (gamma*np.max(Q[sprime,:]) - Q[s,a])
		
        		# Have the computer chooses a random action -> epsilon2 = 1
                if (np.random.rand()<epsilon2):
                
                #we need to chose a random action
                    indices=[]
                    for i in range(0,9):
                        if t[sprime][i]>-1:
                            indices.append(i)
                    
                    pick = randrange(len(indices))
                    a2 = indices[pick]
		    
        		#a is the index of the next state to move to    
                else:
                    a2 = np.argmax(Q[sprime,:])
                    """
                    if threecheck(board) is True:
                        Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (r + gamma*np.min(Q[sprime,np.where(t[s,:]>-1)]) - Q[s,a])
                    """
                sDoublePrime = t[sprime][a2]
                if threecheck(states[sDoublePrime]):
                    r=80
                elif turn ==7:
                    r=20
                    TDDraw+=1
                else:
                    r=0
		
        	     #print "here"
                Q[sprime,a2] += mu/(numberOfTimesStateVisted[sDoublePrime]+1) * (r + gamma*np.max(Q[sDoublePrime,:]) - Q[sprime,a2])
                numberOfTimesStateVisted[sDoublePrime]+=1            
                s = sDoublePrime
                turn+=1
                
                if threecheck(states[s])is True:
                    TDWins+=1
        
        nits = nits+1
        if nits%100==0:
            TDWinPercentageTrainingSec.append(TDWins/float(nits))
            TDDrawPercentageTrainingSec.append(TDDraw/float(nits))
            TDLossPercentageTrainingSec.append(TDLoss/float(nits))
        
    return Q
    #print Q[0]

def trainingAgainstLearner(states, t):
    nStates = np.shape(t)[0]
    nActions = np.shape(t)[1]
    
    Qplayer1 = np.zeros((nStates,nActions))
    Qplayer2 = np.zeros((nStates,nActions))
    numberOfTimesStateVisted = np.zeros((nStates))
    setQNoBacktrack(Qplayer1,t)
    setQNoBacktrack(Qplayer2,t)
    

    mu = 0.7
    gamma = 0.25
    epsilon = .1
    epsilon2 = .15
    nits = 0
    
    Player1Win=0
    Draw=0
    Player2Win=0
    while nits < 1000000:
        # Pick initial state
        s = 0
        # Stop when the accepting state is reached
        turn=0
        while threecheck(states[s]) is False and turn<8:
                       
        # epsilon-greedy
            
            if (np.random.rand()<epsilon):
                """
                we need to chose a random action
                
                """
                indices=[]
                for i in range(0,9):
                    if t[s][i]>-1:
                        indices.append(i)
                    
                pick = randrange(len(indices))
                a = indices[pick]
                """
                a is the index of the next state to move to
                """
                    
                #print s,a
            else:
                a = np.argmax(Qplayer1[s,:])

            # For this example, new state is the chosen action
            sprime = t[s][a]
            turn+=1
            numberOfTimesStateVisted[sprime]+=1 
            
            #If this move wins us the game
            if threecheck(states[sprime]) is True:
                Qplayer2[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (-100 + gamma*np.max(Qplayer2[sprime,:]) - Qplayer2[s,a])
                Qplayer1[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (100 + gamma*np.max(Qplayer1[sprime,:]) - Qplayer1[s,a])
                Player1Win+=1
                s=sprime
            elif turn==8:
                Qplayer2[s,a]+= mu/(numberOfTimesStateVisted[sprime]+1) * (20 + gamma*np.max(Qplayer2[sprime,:]) - Qplayer2[s,a])
                Qplayer1[s,a]+= mu/(numberOfTimesStateVisted[sprime]+1) * (gamma*np.max(Qplayer1[sprime,:]) - Qplayer1[s,a])
            #If not, let the computer pick
                Draw+=1
            else:
                Qplayer1[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (gamma*np.max(Qplayer1[sprime,:]) - Qplayer1[s,a])
                Qplayer2[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (gamma*np.max(Qplayer2[sprime,:]) - Qplayer2[s,a])
        		# Have the computer chooses a random action -> epsilon2 = 1
                if (np.random.rand()<epsilon2):
                
                #we need to chose a random action
                    indices=[]
                    for i in range(0,9):
                        if t[sprime][i]>-1:
                            indices.append(i)
                    
                    pick = randrange(len(indices))
                    a2 = indices[pick]
		    
        		#a is the index of the next state to move to    
                else:
                    a2 = np.argmax(Qplayer2[sprime,:])
                    """
                    if threecheck(board) is True:
                        Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (r + gamma*np.min(Q[sprime,np.where(t[s,:]>-1)]) - Q[s,a])
                    """
                sDoublePrime = t[sprime][a2]
                if threecheck(states[sDoublePrime]):
                    r1=-100
                    r2=80
                elif turn==7:
                    r1=0
                    r2=20
                    Draw+=1
                else:
                    r1=0
                    r2=0
		
        	     #print "here"
                Qplayer2[sprime,a2] += mu/(numberOfTimesStateVisted[sDoublePrime]+1) * (r2 + gamma*np.max(Qplayer2[sDoublePrime,:]) - Qplayer2[sprime,a2])
                Qplayer1[sprime,a2] += mu/(numberOfTimesStateVisted[sDoublePrime]+1) * (r1 + gamma*np.max(Qplayer1[sDoublePrime,:]) - Qplayer1[sprime,a2])
                numberOfTimesStateVisted[sDoublePrime]+=1            
                s = sDoublePrime
                turn+=1
                if threecheck(states[s])is True:
                    Player2Win+=1
                

        nits = nits+1
        if nits%100==0:
            Player1PercentageTraining.append(Player1Win/float(nits))
            DrawPercentageTraining.append(Draw/float(nits))
            Player2PercentageTraining.append(Player2Win/float(nits))

    #print Q[0]
    return [Qplayer1, Qplayer2]

def gameOver(board, turn):

    return threecheck(board) is True or turn==10

def soIHearYouLikeToPlay(Q,states):
    s=0
    board=copy.deepcopy(states[s])
    turn=1
    validMove=False
    print "Who wants to go first:"
    print "1. Me"
    print "2. Not Me"
    WhosFirst=int(raw_input('Input:'))
    

    if WhosFirst==1:
        
        while gameOver(board,turn) is False:
            
            #print board
            while validMove is False:
                move=int(raw_input('Where would you like to go?:'))
                if board[move]==0:
                    validMove=True
                else:
                    print "Invalid Move! Try again"
            board[move]=1
            validMove=False            
            
            turn+=1
            
            if gameOver(board, turn) is True:
                if threecheck(board) is True:
                    print "YOU WIN"
                    return
                else:
                    print board
                    print "ITS A DRAW"
                    return
                    
            #Computer will find the current state of the board
            print "---------------"

            s=stateChecker(states, board)
            a = np.argmax(Q[s,:])
            
            #print s
            #print a
            
            board[a]=2
            print board

            turn+=1            
            print "---------------"
        print "YOU LOSE"

    
    
    else:
        while gameOver(board,turn) is False:
            #Computer will find the current state of the board
            s=stateChecker(states, board)
            a = np.argmax(Q[s,:])
            
            board[a]=1
            turn+=1   
            print board
            
            
            if gameOver is True:
               if threecheck(board) is True:
                   print board
                   print "YOU LOSE"
                   return
               else:
                   print board
                   print "ITS A DRAW"
                   return           
            move=int(raw_input('Input:'))
            board[move]=2
            
            turn+=1

        print "YOU WIN"

        
        
def TwoComputersRand1(Q, t, states):
    s=0
    turn =1
    board=copy.deepcopy(states[s])
    while gameOver(board, turn) is False:
        #print board
        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)
        a = np.argmax(Q[s,:])
        
        board[a]=1
        sprime=t[s][a]
        s=sprime        
        turn+=1
        #print board
        if gameOver(board, turn) is True:
            if threecheck(board) is True:
#               print "Comp 1 WIN"
                #Comp1Win+=1
                return 1
            else:
                #print "ITS A DRAW"
                #Draw+=1                
                return 0
        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)
        indices=[]
        for i in range(0,9):
            if t[s][i]>-1:
                indices.append(i)
                    
        pick = randrange(len(indices))
        a = indices[pick]
        
        board[a]=2
        sprime=t[s][a]
        s=sprime
        turn+=1
    return 2
    #RandWin+=1
    #print board
    #print "Comp 2 Wins"
    
def TwoComputersRand2(Q, t, states):
    s=0
    turn =1
    board=copy.deepcopy(states[s])
    while gameOver(board, turn) is False:
        #print board
        indices=[]
        for i in range(0,9):
            if t[s][i]>-1:
                indices.append(i)
                    
        pick = randrange(len(indices))
        a = indices[pick]
        
        board[a]=2
        sprime=t[s][a]
        s=sprime
        turn+=1
        if gameOver(board, turn) is True:
            if threecheck(board) is True:
#               print "Comp 2 WIN"
                #Comp1Win+=1
                return 2
            else:
                #print "ITS A DRAW"
                #Draw+=1                
                return 0
        #Computer will find the current state of the board
        a = np.argmax(Q[s,:])
        
        board[a]=1
        sprime=t[s][a]
        s=sprime        
        turn+=1
        #print board

        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)

    return 1
    #RandWin+=1
    #print board
    #print "Comp 2 Wins"
    
def TwoComputers(Q1,Q2, t, states):
    s=0
    turn =1
    board=copy.deepcopy(states[s])
    while gameOver(board, turn) is False:
        #print board
        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)
        a = np.argmax(Q1[s,:])
        
        board[a]=1
        sprime=t[s][a]
        s=sprime        
        turn+=1
        #print board
        if gameOver(board, turn) is True:
            if threecheck(board) is True:
#               print "Comp 1 WIN"
                return 1
            else:
                #print "ITS A DRAW"
                #Draw+=1                
                return 0
        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)
        a = np.argmax(Q2[s,:])
        
        board[a]=2
        sprime=t[s][a]
        s=sprime
        turn+=1
    return 2
    #RandWin+=1
    #print board
    #print "Comp 2 Wins"
    
                
#-------------------------------------------------------------------------------------------

"""
States holds all boards
R holds all rewards
t holds list of actions, and location of state following action
"""
states=[]
R=[]
t=[]
TDWinPercentageTrainingFirst=[]
TDDrawPercentageTrainingFirst=[]
TDLossPercentageTrainingFirst=[]

TDWinPercentageTrainingSec=[]
TDDrawPercentageTrainingSec=[]
TDLossPercentageTrainingSec=[]

Player1PercentageTraining=[]
DrawPercentageTraining=[]
Player2PercentageTraining=[]

print "Loading states, please wait."
createAllPossibleStates(states, R, t)


#nStates= np.shape(R)[0]
#print nStates 

print "Time to get to the gym, brb."
Qrand1 = trainingAgainstRand1(states,t)
#Qrand2 = trainingAgainstRand2(states,t)

"""

QQ=trainingAgainstLearner(states, t)
Qplayer1=QQ[0]
Qplayer2=QQ[1]

TDCompWin1=0
RandWin1=0
Draw1=0

TDCompWin2=0
RandWin2=0
Draw2=0

PTDCompWin1=0
PRandWin1=0
PDraw1=0

PTDCompWin2=0
PRandWin2=0
PDraw2=0

RD=0
RP1=0
RP2=0

TRAINDRAW=0
TP1=0
TP2=0


#Play Against a Random computer
for i in range(1000):
    
    result=TwoComputersRand1(Qrand1,t, states)
    if result == 0:
        Draw1+=1
    elif result == 1: 
        TDCompWin1+=1
    else:
        RandWin1+=1
    
    result=TwoComputersRand2(Qrand2,t, states)
    if result == 0:
        Draw2+=1
    elif result == 1: 
        TDCompWin2+=1
    else:
        RandWin2+=1
        
    result=TwoComputersRand1(Qplayer1,t, states)
    if result == 0:
        PDraw1+=1
    elif result == 1: 
        PTDCompWin1+=1
    else:
        PRandWin1+=1
    
    result=TwoComputersRand2(Qplayer2,t, states)
    if result == 0:
        PDraw2+=1
    elif result == 1: 
        PTDCompWin2+=1
    else:
        PRandWin2+=1    
        
        
result=TwoComputers(Qrand1,Qrand2, t, states)
if result == 0:
    RD=1
elif result ==1: 
    RP1=1
else:
    RP2=1
    
result=TwoComputers(Qplayer1,Qplayer2, t, states)
if result == 0:
    TRAINDRAW=1
elif result ==1: 
    TP1=1
else:
    TP2=1   
    
resultPR=TwoComputers(Qplayer1,Qrand2, t, states)
resultRP=TwoComputers(Qrand1,Qplayer2, t, states)
    
print ""
print "------------------------------"
print""    
print "TRAINED AGAINST RANDOMS: "
print ""
print "When Going First: "
print "TDCOMPWIN: ",TDCompWin1
print "Draw: ",Draw1
print "TDLOSS: ",RandWin1
print ""
print "When Going Second: "
print "TDCOMPWIN: ",TDCompWin2
print "Draw: ",Draw2
print "TDLOSS: ",RandWin2
print ""
print "------------------------------"
print ""
print "Trained Against CPU: "
print ""
print "When Going First: "
print "TDCOMPWIN: ",PTDCompWin1
print "Draw: ",PDraw1
print "TDLOSS: ",PRandWin1
print ""
print "When Going Second: "
print "TDCOMPWIN: ",PTDCompWin2
print "Draw: ",PDraw2
print "TDLOSS: ",PRandWin2
print ""
print "------------------------------"
print ""
print "Two Randoms: "
print "Draw: ",RD
print "Player 1: ",RP1
print "Player 2: ",RP2
print ""
print "Two Training: "
print "Draw: ",TRAINDRAW
print "Player 1: ",TP1
print "Player 2: ",TP2
print ""
print "Trained player first: ", resultPR
print ""
print "TrainedRandom first: ",resultRP

"""


#----------------------------------------------------------------------------------------------------
#	This section plots a learning curve on a 
#	graph to show the amount of wins vs how many 
#	games played


"""
import matplotlib.pyplot as plt

plt.figure(1)
plt.title("TD Going First - Training Games")
plt.plot(range(len(TDDrawPercentageTrainingFirst)),TDWinPercentageTrainingFirst,label="Winning Going First")
plt.plot(range(len(TDDrawPercentageTrainingFirst)),TDDrawPercentageTrainingFirst,label="Draw Going First")
plt.plot(range(len(TDDrawPercentageTrainingFirst)),TDLossPercentageTrainingFirst,label="Loss Going First")
plt.legend(bbox_to_anchor=(1.5, .5), loc=2, borderaxespad=0.)

plt.figure(2)
plt.title("TD Going Second - Training Games")
plt.plot(range(len(TDDrawPercentageTrainingFirst)),TDWinPercentageTrainingSec,label="Winning Going Second")
plt.plot(range(len(TDDrawPercentageTrainingFirst)),TDDrawPercentageTrainingSec,label="Draw Going Second")
plt.plot(range(len(TDDrawPercentageTrainingFirst)),TDLossPercentageTrainingSec,label="Loss Going Second")
plt.legend(bbox_to_anchor=(.05, .05), loc=2, borderaxespad=0.)

plt.figure(3)
plt.title("Two TD Learners Against Each Other")
plt.plot(range(0,10000),Player1PercentageTraining, label="Player 1 Wins")
plt.plot(range(10000),Player2PercentageTraining, label="Player 2 Wins")
plt.plot(range(10000),DrawPercentageTraining,label="Draw")
plt.legend(bbox_to_anchor=(.05, .05), loc=2, borderaxespad=0.)
"""

#-----------------------------------------------------------------------------------------------------------
#	This section is a user menu that allows the 
#	user to determine if they want two trained 
#	computers to battle, or play against the super computer

mode=0
while mode!=3:
    print "Would you like:"
    print "1. Two computers to battle to the death"
    print "2. Play against the super computer"

    mode=int(raw_input('Input:'))

    if mode==1:
        print "You selected two computers"
    
        TwoComputers(QRand1,QRand2, t,states, Comp1Win,RandWin,Draw)
        print ""
        print ""

    elif mode==2:
        print "So you want to play?"
        print ""
        print ""
    
        soIHearYouLikeToPlay(Q, states)
    elif mode!=3:
        print "Invalid Response"
        print ""
        print""
    
print "done"
"""
