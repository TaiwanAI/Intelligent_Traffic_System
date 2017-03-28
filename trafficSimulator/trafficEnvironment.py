class CrawlingRobotEnvironment(environment.Environment):

   def __init__(self, crawlingRobot):

       self.crawlingRobot = crawlingRobot

       # The state is of the form (armAngle, handAngle)
       # where the angles are bucket numbers, not actual
       # degree measurements
       self.state = None

       self.nArmStates = 9
       self.nHandStates = 13

       # create a list of arm buckets and hand buckets to
       # discretize the state space
       minArmAngle,maxArmAngle = self.crawlingRobot.getMinAndMaxArmAngles()
       minHandAngle,maxHandAngle = self.crawlingRobot.getMinAndMaxHandAngles()
       armIncrement = (maxArmAngle - minArmAngle) / (self.nArmStates-1)
       handIncrement = (maxHandAngle - minHandAngle) / (self.nHandStates-1)
       self.armBuckets = [minArmAngle+(armIncrement*i) \
          for i in range(self.nArmStates)]
       self.handBuckets = [minHandAngle+(handIncrement*i) \
        for i in range(self.nHandStates)]

       # Reset
       self.reset()

   def getCurrentState(self):
       """
         Return the current state
         of the crawling robot
       """
       return self.state

   def getPossibleActions(self, state):
       """
         Returns possible actions
         for the states in the
         current state
       """

       actions = list()

       currArmBucket,currHandBucket = state
       if currArmBucket > 0: actions.append('arm-down')
       if currArmBucket < self.nArmStates-1: actions.append('arm-up')
       if currHandBucket > 0: actions.append('hand-down')
       if currHandBucket < self.nHandStates-1: actions.append('hand-up')

       return actions

   def doAction(self, action):
       """
         Perform the action and update
         the current state of the Environment
         and return the reward for the
         current state, the next state
         and the taken action.

         Returns:
           nextState, reward
       """
       nextState, reward =  None, None

       oldX,oldY = self.crawlingRobot.getRobotPosition()

       armBucket,handBucket = self.state
       armAngle,handAngle = self.crawlingRobot.getAngles()
       if action == 'arm-up':
         newArmAngle = self.armBuckets[armBucket+1]
         self.crawlingRobot.moveArm(newArmAngle)
         nextState = (armBucket+1,handBucket)
       if action == 'arm-down':
         newArmAngle = self.armBuckets[armBucket-1]
         self.crawlingRobot.moveArm(newArmAngle)
         nextState = (armBucket-1,handBucket)
       if action == 'hand-up':
         newHandAngle = self.handBuckets[handBucket+1]
         self.crawlingRobot.moveHand(newHandAngle)
         nextState = (armBucket,handBucket+1)
       if action == 'hand-down':
         newHandAngle = self.handBuckets[handBucket-1]
         self.crawlingRobot.moveHand(newHandAngle)
         nextState = (armBucket,handBucket-1)
         
       newX,newY = self.crawlingRobot.getRobotPosition()
       
       # a simple reward function
       reward = newX - oldX
       
       self.state = nextState
       return nextState, reward


  