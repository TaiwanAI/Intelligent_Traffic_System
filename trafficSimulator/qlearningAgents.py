from game import *
from learningAgents import ReinforcementAgent


import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """

  def __init__(self, **args):
    # "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    self.times = [5,2,1,0,-1,-2,-5]
    #initiate all actions (red, green)
    self.actions = []
    for i in self.times:
      for j in self.times:
        self.actions.append((i,j))

    self.qValue = util.Counter()
  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    
    # util.raiseNotDefined()

    print("state",state)
    print("action",action)
    return self.qValue[(state,action)]

  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    
    # util.raiseNotDefined()
    # print state, self.getLegalActions(state), len(self.getLegalActions(state))

    

    maxValue = -999999999
    firstIteration = True
    for action in self.actions:
      if firstIteration:
        maxValue = self.getQValue(state,action)
        firstIteration = False
        continue
      if self.getQValue(state,action) > maxValue:
        maxValue = self.getQValue(state,action)
    return maxValue

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    
    # util.raiseNotDefined()
    
    
    maxValue = -999999999999999
    bestAction = None
    bestActionSet = set()
    firstIteration = True
    for action in self.actions:
      if firstIteration:
        firstIteration = False
        maxValue = self.getQValue(state,action)
        bestAction = action
        continue
      if self.getQValue(state,action) > maxValue:
        maxValue = self.getQValue(state,action)
        bestAction = action
      elif self.getQValue(state,action) == maxValue:
        bestActionSet.add(action)
        bestActionSet.add(bestAction)
      # if self.getQValue(state, action) < -999999999:
      #   print self.getQValue(state, action)
    if len(bestActionSet) == 0:
      return bestAction    
    else:
      #break ties randomly
      return random.choice(list(bestActionSet))

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.actions
    if len(legalActions) == 0:
      return None
    action = None
        # util.raiseNotDefined()
    if util.flipCoin(self.epsilon):
      # print legalActions
      action = random.choice(legalActions)
    else:
      action = self.getPolicy(state)
    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    
    # util.raiseNotDefined()

    nextAction = self.getAction(nextState)
    sample = reward + self.discount * self.getQValue(nextState, nextAction)
    self.qValue[(state,action)] = self.getQValue(state,action) * (1-self.alpha) + self.alpha* sample
    # self.qValue[(state, action)] = self.getQValue(state, action) + self.alpha * (reward + self.discount * self.getValue(nextState) - self.getQValue(state, action))

