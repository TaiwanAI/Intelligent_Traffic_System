from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

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
    self.times = [10,5,2,1,0,-1,-2,-5,-10]
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

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    
    self.weights = util.Counter()

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    
   
    qValue = 0.0
    featureVector = self.featExtractor.getFeatures(state,action)
    
    for feature in featureVector:
      
      qValue += self.weights[feature] * featureVector[feature]  
    return qValue

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
     
    # util.raiseNotDefined()
    # identityExtractor = IdentityExtractor()
    featureVector = self.featExtractor.getFeatures(state,action)
    for feature in featureVector:
      # print self.weights[feature]
      correction = reward + self.discount* self.getValue(nextState)-self.getQValue(state,action)
      self.weights[feature] +=  self.alpha* correction* featureVector[feature]
      # print self.weights[feature], correction, featureVector[feature]
  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
       
      # for feature in self.weights:
      #   print self.weights[feature]
      pass
