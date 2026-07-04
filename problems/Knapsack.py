import random 

import problems.Base as Base 

class KnapsackGA(Base.Base):
    
    def __init__(self, values, weights, capacities,selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience):
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

# Genetic Knapsack
    def genetic(self):

       #Generate random values and weights for small Knapsack
        values = [random.randint(10, 100) for i in range(20)]

        weights = [random.randint(1, 30) for i in range(20)]

        capacities = [100]

        selectionType = "tournament"
        chromosomSize = len(values)
        populationSize = 50
        generations = 100
        tournamentSize = 3
        crossoverProb = 0.7
        mutationProb = 0.05
        elitismNum = 2
        patience = 20

        self.geneticSolver = KnapsackGA(
            values,
            weights,
            capacities,
            selectionType,
            chromosomSize,
            populationSize,
            generations,
            tournamentSize,
            mutationProb,
            crossoverProb,
            elitismNum,
            patience
        )

        result = self.geneticSolver.genetic_algorithm()
        self.geneticSolver.printResults(result, values, weights, capacities)

        # Case 2: Midium Knapsack 
        values = [random.randint(10, 150) for i in range(50)]

        weights = [ [random.randint(1, 50)] for i in range(50)]

        capacities = [500]

        selectionType = "tournament"
        chromosomSize = len(values)
        populationSize = 200
        generations = 500
        tournamentSize = 5
        crossoverProb = 0.8
        mutationProb = 0.1
        elitismNum = 10
        patience = 50

        self.geneticSolver = KnapsackGA(
            values,
            weights,
            capacities,
            selectionType,
            chromosomSize,
            populationSize,
            generations,
            tournamentSize,
            mutationProb,
            crossoverProb,
            elitismNum,
            patience
        )

        result = self.geneticSolver.genetic_algorithm()
        self.geneticSolver.printResults(result, values, weights, capacities)

        # Case 3: BigKnapsack 
        values = [random.randint(20, 200) for i in range(100)]

        weights = [
            [random.randint(5, 80)]
            for i in range(100)
        ]

        capacities = [1500]

        selectionType = "tournament"
        chromosomSize = len(values)
        populationSize = 1000
        generations = 2000
        tournamentSize = 8
        crossoverProb = 0.9
        mutationProb = 0.15
        elitismNum = 20
        patience = 100

        self.geneticSolver = KnapsackGA(
            values,
            weights,
            capacities,
            selectionType,
            chromosomSize,
            populationSize,
            generations,
            tournamentSize,
            mutationProb,
            crossoverProb,
            elitismNum,
            patience
        )

        result = self.geneticSolver.genetic_algorithm()
        self.geneticSolver.printResults(result, values, weights, capacities)

#Button Up DP 
def buttonUpKnapsack(W, val, wt):
    n = len(wt)
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Build table dp[][] in bottom-up manner
    for i in range(n + 1):
        for j in range(W + 1):

            # If there is no item or the knapsack's capacity is 0
            if i == 0 or j == 0:
                dp[i][j] = 0
            else:
                pick = 0

                # Pick ith item if it does not exceed the capacity of knapsack
                if wt[i - 1] <= j:
                    pick = val[i - 1] + dp[i - 1][j - wt[i - 1]]

                # Don't pick the ith item
                notPick = dp[i - 1][j]

                dp[i][j] = max(pick, notPick)

    return dp[n][W]
