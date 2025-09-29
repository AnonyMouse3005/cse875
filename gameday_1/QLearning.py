# -----------------------------------------------------------------
# Game Day 1:  Learning Day
# QLearning algorithm implemented by Leen-Kiat Soh
#
# 1.  The program below is not documented so that each team's 
# responsibility is to document the following code clearly 
# and completely.
#
# 2.  The function computeAlpha() is implemented as a default design.
# Each team's responsiblity is to revise the design according to their
# game strategy.
#
# 3.  The function decideAction() is implemented as a random action
# selector.  Each team's responsiblity is to revise the design 
# according to their game strategy.
#
# Note also that the program reads in two input csv files so as to 
# simulate the transition probability of (s,a,s') and generate the 
# rewards r(s,a,s').  With these two functions, the main body of the 
# program essentially receives the next state from the "environment" 
# together with the next state's rewards.
# 
# You are not allowed to modify the code after "MAIN BODY" except for
# one line regarding the alpha (i.e., learning rate).
# -----------------------------------------------------------------

import random
import numpy
import csv

MAX_ITERATION = 250000
ALPHA = 0.9
BETA = 0.9

qTable = []
tpTable = []

MAX_NUM_ACTIONS = 6
MAX_NUM_STATES = 6

def initialize():
   # initialize the Q table and the count of state-action pairs
   for i in range(0,MAX_NUM_STATES):
      temp = []
      for j in range(0,MAX_NUM_ACTIONS):
         temp.append(0)
      # end for j
      qTable.append(temp)
   # end for i

# end initialize

def readTPTable():

   # first initialize
   for i in range(0,MAX_NUM_STATES):
      temp = []
      for j in range(0,MAX_NUM_ACTIONS):
         temp2 = []
         for k in range(0,MAX_NUM_STATES):
            temp2.append(0)
	 # end for k
         temp.append(temp2)
      # end for j
      tpTable.append(temp)
   # end for j

   # then read from input file
   with open("TPTable.csv",'r') as csv_infile:
      data_reader = csv.reader(csv_infile,delimiter=',')
      for row in data_reader:
         s = int(row[0])
         a = int(row[1])
         s_next = int(row[2])
         p = float(row[3])
         tpTable[s][a][s_next] = p
      # end for
   # end with open

# end readTPTable      

def obtainReward(s,a,s_next):

   rTable = []
   with open("r.csv",'r') as csv_infile:
      data_reader = csv.reader(csv_infile,delimiter=',')
      for row in data_reader:
         rTable.append(float(row[0]))
      # end for
   # end with open

   r = numpy.random.normal(rTable[s_next], 0.1, 1)

   return r

# end obtainReward

def obtainNextState(s,a):

   pnum = random.random()
   i = 0
   lb = 0
   found = False

   while (found == False and i < MAX_NUM_STATES):
      ub = lb + tpTable[s][a][i]
      if (pnum >= lb and pnum <= ub):
         found = True
      else:
         lb = ub
         i = i + 1
      # end if
   # end while

   if i >= MAX_NUM_STATES:
      i = s # back to the current state

   return i

# end obtainNextState

def computeAlpha(alpha,t):  # TODO
   alpha = alpha*(MAX_ITERATION - t)/(1.0*MAX_ITERATION)
   return alpha
# end computeAlpha

def decideAction(s, epsilon=0.5):
   '''
   Decide action given current state s using the standard epsilon-greedy algorithm.
   Reference:
   Sutton, R. S. & Barto, A. G. 1998 Reinforcement learning: an introduction. Cambridge, MA: MIT Press.
   '''
   # return random.randint(0,MAX_NUM_ACTIONS-1)
   if random.uniform(0, 1) < epsilon:  # explore with probability `epsilon`
      return random.randint(0,MAX_NUM_ACTIONS-1)  # randomly select an action in the action space
   else:  # exploit with probability `1-epsilon`
      q_s = qTable[s]
      return q_s.index(max(q_s))  # select the action with the highest Q-value for the current state
# end decideAction

def computeValue(s):
   max = qTable[s][0]
   for j in range(1,MAX_NUM_ACTIONS):
      if (qTable[s][j] > max):
         max = qTable[s][j]
   # end for j
   return max
# end computeValue

# -------------------------------------------------------
# MAIN BODY
# -------------------------------------------------------
# Do not modify the code in the following section, 
# except for the line that dictates how alpha 
# will change or stay as a constant.
# -------------------------------------------------------

initialize()
readTPTable()
t = 0
alpha = ALPHA
s = 0
rewardSoFar = 0

while (t < MAX_ITERATION):
   alpha = computeAlpha(alpha,t) # only if we want alpha to be dependent on t
   a = decideAction(s) 
   s_next = obtainNextState(s,a)
   if (s == s_next):
      r = 0
   else:
      r = obtainReward(s,a,s_next)
   # rewardSoFar = rewardSoFar + r
   # print("rewardSoFar = " + str(rewardSoFar))
   val = computeValue(s_next)
   qTable[s][a] = (1 - alpha)*qTable[s][a] + alpha*(r + BETA*val)

   print("t = " + str(t))
   s = s_next
   t = t + 1
  
# end while


# print out the Q table
for i in range(0,MAX_NUM_STATES):
   for j in range(0,MAX_NUM_ACTIONS):
      #print("["+str(i)+"]["+str(j)+"]: "+str(qTable[i][j]))
      print(str(qTable[i][j]))

# print out final total rewards
#print("Total rewards = " + str(rewardSoFar))
print(str(rewardSoFar))

