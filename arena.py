#
# This file deals with all functions that has two players/computers playing against each other. 
#


#------------------------------------------------------------------------------------------------
# PLAY AGAINST A COMPUTER
#------------------------------------------------------------------------------------------------

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
        
        while game.gameOver(board,turn) is False:
            
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
            
            if game.gameOver(board, turn) is True:
                if game.threecheck(board) is True:
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
        while game.gameOver(board,turn) is False:
            #Computer will find the current state of the board
            s=stateChecker(states, board)
            a = np.argmax(Q[s,:])
            
            board[a]=1
            turn+=1   
            print board
            
            
            if game.gameOver is True:
               if game.threecheck(board) is True:
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

#------------------------------------------------------------------------------------------------
# SUPER COMPUTER VS RANDOM COMPUTER
# Random Goes first
#------------------------------------------------------------------------------------------------
def TwoComputersRand1(Q, t, states):
    s=0
    turn =1
    board=copy.deepcopy(states[s])
    while game.gameOver(board, turn) is False:
        #print board
        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)
        a = np.argmax(Q[s,:])
        
        board[a]=1
        sprime=t[s][a]
        s=sprime        
        turn+=1
        #print board
        if game.gameOver(board, turn) is True:
            if game.threecheck(board) is True:
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

#------------------------------------------------------------------------------------------------
# SUPER COMPUTER VS RANDOM COMPUTER
# Supercomputer goes first
#------------------------------------------------------------------------------------------------

def TwoComputersRand2(Q, t, states):
    s=0
    turn =1
    board=copy.deepcopy(states[s])
    while game.gameOver(board, turn) is False:
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
        if game.gameOver(board, turn) is True:
            if game.threecheck(board) is True:
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

#------------------------------------------------------------------------------------------------
# SUPER COMPUTER VS SUPER COMPUTER
# 
#------------------------------------------------------------------------------------------------

def TwoComputers(Q1,Q2, t, states):
    s=0
    turn =1
    board=copy.deepcopy(states[s])
    while game.gameOver(board, turn) is False:
        #print board
        
        #Computer will find the current state of the board
        #s=stateChecker(states, board)
        a = np.argmax(Q1[s,:])
        
        board[a]=1
        sprime=t[s][a]
        s=sprime        
        turn+=1
        #print board
        if game.gameOver(board, turn) is True:
            if game.threecheck(board) is True:
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
