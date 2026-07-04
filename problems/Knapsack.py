import random 

import problems.Base as Base 

class KnapsackGA(Base.Base):
    
    def __int__(self, values, weights, capacities,selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience):
        super().__init__(selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        self.values = values 
        self.weights = weights
        self.capacities = capacities 
        self.dimensions = len(capacities)

    
    def fitness(self, individual):
        value = 0
        used = [0] * self.dimensions
        for i, gene in enumerate(individual):
             if gene:
                value += self.values[i]
                for d in range(self.dimensions):
                    used[d] += self.weights[i][d]
        overflow = sum(max(0,used[d] - self.capacities[d]) for d in range(self.dimensions))

        if overflow == 0:
             return 1 + value
        return 1 / (1 + overflow)
    

class KnapsackExact: 
    
    #Knapsack with recursion 
    def recursive(W, val, wt, n):

        # Base Case
        if n == 0 or W == 0:
            return 0

        pick = 0

        # Pick nth item if it does not exceed the capacity of knapsack
        if wt[n - 1] <= W:
            pick = val[n - 1] + recursive(W - wt[n - 1], val, wt, n - 1)
        
        # Don't pick the nth item
        notPick = recursive(W, val, wt, n - 1)
        
        return max(pick, notPick)

    def recursiveKnapsack(W, val, wt):
        n = len(val)
        return recursive(W, val, wt, n)

    #DP Knapsack 
    def dp(W, val, wt, n, memo):

        # Base Case
        if n == 0 or W == 0:
            return 0

        # Check if we have previously calculated the same subproblem
        if memo[n][W] != -1:
            return memo[n][W]

        pick = 0

        # Pick nth item if it does not exceed the capacity of knapsack
        if wt[n - 1] <= W:
            pick = val[n - 1] + dp(W - wt[n - 1], val, wt, n - 1, memo)

        # Don't pick the nth item
        notPick = dp(W, val, wt, n - 1, memo)

        # Store the result in memo[n][W] and return it
        memo[n][W] = max(pick, notPick)
        return memo[n][W]

    def dpKnapsack(W, val, wt):
        n = len(val)

        # Memoization table to store the results
        memo = [[-1] * (W + 1) for _ in range(n + 1)]

        return dp(W, val, wt, n, memo)

    #genetic 
