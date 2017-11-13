# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # print "legal: ", legalMoves

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        scores = [manhattanDistance(newPos, food) for food in currentGameState.getFood().asList()]
        if len(scores)> 0:
            bestScore = min(scores)
        else:
            bestScore = 0

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            dist = manhattanDistance(newPos, ghostPos)
            if dist < 3 and ghost.scaredTimer == 0:
                return -1000
        return -bestScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        agents = gameState.getNumAgents()
        score, move = self.getStep(gameState, 0, self.depth, 0, agents, [])
        return move;
        # util.raiseNotDefined()

    def getStep(self, gameState, depth, finalDepth, index, totalIndex, val):
        if index == totalIndex and depth < finalDepth:
            index = 0
            depth += 1

        if depth == finalDepth:
            evaluation = self.evaluationFunction(gameState)
            return (evaluation, val[0])

        playerMoves = gameState.getLegalActions(index)

        if index == 0:
            moveEval = -10000
        else:
            moveEval = 10000
        result = None
        if len(playerMoves) > 0:
            for i in range(len(playerMoves)):
                eachMove = playerMoves[i]
                val1 = list(val)
                val1.append(eachMove)
                stateAfterMove = gameState.generateSuccessor(index, eachMove)
                score, move = self.getStep(stateAfterMove, depth, finalDepth, index+1, totalIndex, val1)
                if index == 0 and score > moveEval:
                    moveEval = max(moveEval, score)
                    result = move
                elif index > 0 and score < moveEval:
                    moveEval = min(moveEval, score)
                    result = move

                if (i == len(playerMoves)-1):
                    return (moveEval, result)
        else:
            evaluation = self.evaluationFunction(gameState)
            return (evaluation, val[0])

        return (moveEval, result)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agents = gameState.getNumAgents()
        score, move = self.getStep(gameState, 0, self.depth, 0, agents, [], -10000, 10000)
        return move;
        # util.raiseNotDefined()

    def getStep(self, gameState, depth, finalDepth, index, totalIndex, val, alpha, beta):
        if index == totalIndex and depth < finalDepth:
            index = 0
            depth += 1

        if depth == finalDepth:
            evaluation = self.evaluationFunction(gameState)
            return (evaluation, val[0])

        playerMoves = gameState.getLegalActions(index)

        if index == 0:
            moveEval = -10000
        else:
            moveEval = 10000
        result = None
        if len(playerMoves) > 0:
            for i in range(len(playerMoves)):
                eachMove = playerMoves[i]
                val1 = list(val)
                val1.append(eachMove)
                stateAfterMove = gameState.generateSuccessor(index, eachMove)
                score, move = self.getStep(stateAfterMove, depth, finalDepth, index + 1, totalIndex, val1, alpha, beta)
                if index == 0 and score > moveEval:
                    moveEval = score
                    result = move
                    alpha = max(alpha, moveEval)
                if index > 0 and score < moveEval:
                    moveEval = score
                    result = move
                    beta = min(beta, moveEval)

                if beta < alpha:
                    break
                if i == (len(playerMoves) - 1):
                    return moveEval, result
        else:
            evaluation = self.evaluationFunction(gameState)
            return evaluation, val[0]

        return moveEval, result

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        agents = gameState.getNumAgents()
        score, move = self.getStep(gameState, 0, self.depth, 0, agents, [], 0)
        return move;
        # util.raiseNotDefined()

    def getStep(self, gameState, depth, finalDepth, index, totalIndex, val, moves):
        if index == totalIndex and depth < finalDepth:
            index = 0
            depth += 1

        if depth == finalDepth:
            evaluation = self.evaluationFunction(gameState)
            if index > 0 and moves > 0:
                evaluation = float(evaluation * (float(1) / float(moves)))
            return (float(evaluation), val[0])

        playerMoves = gameState.getLegalActions(index)

        if index == 0:
            moveEval = float(-10000)
        else:
            moveEval = float(10000)
        result = None
        if len(playerMoves) > 0:
            for i in range(len(playerMoves)):
                eachMove = playerMoves[i]
                val1 = list(val)
                val1.append(eachMove)
                stateAfterMove = gameState.generateSuccessor(index, eachMove)
                score, move = self.getStep(stateAfterMove, depth, finalDepth, index+1, totalIndex, val1, len(playerMoves))
                if index == 0 and float(score) > float(moveEval):
                    moveEval = float(score)
                    result = move
                elif index > 0:
                    if moveEval == float(10000):
                        moveEval = float(score)
                    else:
                        moveEval += float(score)
                    result = move

                if (i == len(playerMoves)-1):
                    return (float(moveEval), result)
        else:
            evaluation = float(self.evaluationFunction(gameState))
            if index > 0 and moves > 0:
                evaluation = float(evaluation * (float(1) / float(moves)))
            return (float(evaluation), val[0])

        return (float(moveEval), result)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

