#------------------------------------------------------------------------------------------------
# THIS SECTION IS USED FOR TESTING THE THE WINNING PERCENTAGE OF 
# THE SUPER COMPUTERS VS DIFFERENT OPPONENTS OVER 1000 GAMES
# ******** It is not necessary for the program to run**************
#------------------------------------------------------------------------------------------------
def winningPercent(QQ, Qrand1, Qrand2, t, states):
  
  TDWinPercentageTrainingFirst=[]
  TDDrawPercentageTrainingFirst=[]
  TDLossPercentageTrainingFirst=[]

  TDWinPercentageTrainingSec=[]
  TDDrawPercentageTrainingSec=[]
  TDLossPercentageTrainingSec=[]

  Player1PercentageTraining=[]
  DrawPercentageTraining=[]
  Player2PercentageTraining=[]
  
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
  
  for i in range(1000):
      #Play Against a Random computer
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

  #----------------------------------------------------------------------------------------------------
  #	This section plots a learning curve on a 
  #	graph to show the amount of wins vs how many 
  #	games played
  #----------------------------------------------------------------------------------------------------
  
  
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
  


