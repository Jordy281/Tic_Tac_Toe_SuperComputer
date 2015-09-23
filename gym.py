"""

Here we will train the Rewards function
 
"""  
import numpy as np
import copy
from random import randrange
import game.py

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
        while game.threecheck(states[s]) is False and turn<8:
                       
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
            if game.threecheck(states[sprime]) is True:
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
                if game.threecheck(states[sDoublePrime]):
                    r=-100.
                else:
                    r=0
		
        		
                Q[sprime,a2] += mu/(numberOfTimesStateVisted[sDoublePrime]+1) * (r + gamma*np.max(Q[sDoublePrime,:]) - Q[sprime,a2])
                numberOfTimesStateVisted[sDoublePrime]+=1            
                s = sDoublePrime
                turn+=1
                
                if game.threecheck(states[s])is True:
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
        while game.threecheck(states[s]) is False and turn<8:
                       
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
            if game.threecheck(states[sprime]) is True:
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
                    if game.threecheck(board) is True:
                        Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (r + gamma*np.min(Q[sprime,np.where(t[s,:]>-1)]) - Q[s,a])
                    """
                sDoublePrime = t[sprime][a2]
                if game.threecheck(states[sDoublePrime]):
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
                
                if game.threecheck(states[s])is True:
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
        while game.threecheck(states[s]) is False and turn<8:
                       
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
            if game.threecheck(states[sprime]) is True:
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
                    if game.threecheck(board) is True:
                        Q[s,a] += mu/(numberOfTimesStateVisted[sprime]+1) * (r + gamma*np.min(Q[sprime,np.where(t[s,:]>-1)]) - Q[s,a])
                    """
                sDoublePrime = t[sprime][a2]
                if game.threecheck(states[sDoublePrime]):
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
                if game.threecheck(states[s])is True:
                    Player2Win+=1
                

        nits = nits+1
        if nits%100==0:
            Player1PercentageTraining.append(Player1Win/float(nits))
            DrawPercentageTraining.append(Draw/float(nits))
            Player2PercentageTraining.append(Player2Win/float(nits))

    #print Q[0]
    return [Qplayer1, Qplayer2]

