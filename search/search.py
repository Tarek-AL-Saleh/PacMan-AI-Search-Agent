# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):

    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    stack=util.Stack()
    visited=set() # to mark the visited nodes
    stack.push((problem.getStartState(), [], 0))
    
    while not stack.isEmpty(): 
        state, path, cost = stack.pop() # take the position, the path till this node, and the total cost

        if state not in visited: #if we didn't check it before
            visited.add(state) # mark it as checked or visited

            if problem.isGoalState(state): #if it is the goal state, return the goal path
                return path    
               
            for successor, action, stepCost in problem.getSuccessors(state): #add every valid unvisited successor to the stack
                if successor not in visited:
                    stack.push((successor, path + [action], cost + stepCost))

    return [] # if the goal state is not reachable, then return an empty list 

def breadthFirstSearch(problem: SearchProblem):

    """Search the shallowest nodes in the search tree first."""
    # same as dfs but use a FIFO Queue instead of a LIFO Stack
    queue = util.Queue() 
    visited = set()
    queue.push((problem.getStartState(), [], 0))

    while not queue.isEmpty():
        state, path, cost = queue.pop()

        if state not in visited:
            visited.add(state)

            if problem.isGoalState(state):
                return path
            
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    queue.push((successor, path + [action], cost + stepCost))
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""

    frontier = util.PriorityQueue()
    visited = set()
    frontier.push((problem.getStartState(), [], 0), 0)

    while not frontier.isEmpty(): #pick a node from the priority queue according to the least total cost 
        state, path, cost = frontier.pop()

        if problem.isGoalState(state): # check the goal after choosing the node
            return path

        if state not in visited:
            visited.add(state)
            
            for successor, action, step_cost in problem.getSuccessors(state):
                new_cost = cost + step_cost
                frontier.push((successor, path + [action], new_cost), new_cost) #the priority is according to the total cost to take the action
    return [] 

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial. 
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    """Search the node that has the lowest combined cost and heuristic first."""

    frontier = util.PriorityQueue()
    visited = set()
    frontier.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem)) # the nodes are stored in the PriorityQueue in the shape of: (((PositionX,PositionY),Actions,Total_cost), Heuristic+Total_cost)

    while not frontier.isEmpty():
        current_state, actions, current_cost = frontier.pop()

        if problem.isGoalState(current_state):
            return actions
        
        if current_state not in visited:
            visited.add(current_state)

            for successor, action, step_cost in problem.getSuccessors(current_state):
                new_cost = current_cost + step_cost
                priority = new_cost + heuristic(successor, problem) # Priority is found by the sum of the Heuristic and the total cost
                frontier.push((successor, actions + [action], new_cost), priority)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
