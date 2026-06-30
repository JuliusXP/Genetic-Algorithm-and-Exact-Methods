import problems.Base as Base
import random

# Subclass for the Subset Sum problem, inheriting from the Base class
class GeneticPartition(Base.Base):
    def __init__(self, numbers, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience):
        super().__init__(selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        self.numbers = numbers

    #Calculate the fitness of an individual
    def fitness(self, individual):
        totalUno = 0
        totalDos = 0

        for i in range(len(individual)):
            if individual[i] == 1:
                totalUno += self.numbers[i]
            else:
                totalDos += self.numbers[i]

        difference = abs(totalUno - totalDos)
        return 1 / (1 + difference)

    def printResults(self, result, numbers):
        best = result["bestIndividual"]
        solution = []

        for i in range(len(best)):
            if best[i] == 1:
                solution.append(numbers[i])

        print()
        print("Numbers:", numbers)
        print("Best chromosome:", best)
        print("Subset:", solution)
        print("Sum:", sum(solution))
        print("Fitness:", result["bestFitness"])
        print("Generation:", result["bestGeneration"])

class PartitionProblem:

    def recursive(self, n, numbers, sum):
    
        # base cases
        if sum == 0:
            return True
        if n == 0:
            return False

        # If element is greater than sum, then ignore it
        if numbers[n-1] > sum:
            return self.recursive(n-1, numbers, sum)

        # Check if sum can be obtained by any of the following
        # either including the current element
        # or excluding the current element
        return self.recursive(n-1, numbers, sum) or self.recursive(n-1, numbers, sum - numbers[n-1])

    def recursiveEqualPartition(self, numbers):
        
        # Calculate sum of the elements in array
        numbersSum = sum(numbers)
        
        # If sum is odd, there cannot be two 
        # subsets with equal sum
        if numbersSum % 2 != 0:
            return False 
            
        return self.recursive(len(numbers), numbers, numbersSum // 2)
    
    def dp(self, n, arr, sum, memo):
        
        # base cases
        if sum == 0:
            return True
        if n == 0:
            return False

        if memo[n-1][sum] != -1:
            return memo[n-1][sum]

        # If element is greater than sum, then ignore it
        if arr[n-1] > sum:
            return self.dp(n-1, arr, sum, memo)

        # Check if sum can be obtained by any of the following
        # either including the current element
        # or excluding the current element
        memo[n-1][sum] = self.dp(n-1, arr, sum, memo) or self.dp(n-1, arr, sum - arr[n-1], memo)
        return memo[n-1][sum]

    def dpEqualPartition(self, arr):
        
        # Calculate sum of the elements in array
        arrSum = sum(arr)

        # If sum is odd, there cannot be two 
        # subsets with equal sum
        if arrSum % 2 != 0:
            return False

        memo = [[-1 for _ in range(arrSum+1)] for _ in range(len(arr))]
        
        return self.dp(len(arr), arr, arrSum // 2, memo)
    
    def printResults(self, numbers, result):
        print()
        print(numbers)
        if result == True:
            print("Si existe un conjunto")
        else:
            print("No existe un conjunto")
        
    
    def genetic(self):
        # Generate random numbers and a target sum for the Subset Sum problem
        numbers = [random.randint(1, 60) for i in range(20)]

        selectionType = "tournament"
        chromosomSize = len(numbers)
        populationSize = 50
        generations = 100
        tournamentSize = 3
        crossoverProb = 0.7
        mutationProb = 0.05
        elitismNum = 2
        patience = 20

        # Create an instance of the SubsetSum class and run the genetic algorithm
        self.genetic = GeneticPartition(numbers, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.genetic.genetic_algorithm()

        # Print the results of the genetic algorithm
        self.genetic.printResults(result, numbers)

        # Generate random numbers and a target sum for the Subset Sum problem
        numbers = [random.randint(1, 100) for i in range(50)]

        selectionType = "tournament"
        chromosomSize = len(numbers)
        populationSize = 200
        generations = 500
        tournamentSize = 5
        crossoverProb = 0.8
        mutationProb = 0.1
        elitismNum = 10
        patience = 50

        # Create an instance of the SubsetSum class and run the genetic algorithm
        self.genetic = GeneticPartition(numbers, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.genetic.genetic_algorithm()

        # Print the results of the genetic algorithm
        self.genetic.printResults(result, numbers)

        # Generate random numbers and a target sum for the Subset Sum problem
        numbers = [random.randint(10, 60) for i in range(100)]

        selectionType = "tournament"
        chromosomSize = len(numbers)
        populationSize = 1000
        generations = 2000
        tournamentSize = 8
        crossoverProb = 0.9
        mutationProb = 0.15
        elitismNum = 20
        patience = 100

        # Create an instance of the SubsetSum class and run the genetic algorithm
        self.genetic = GeneticPartition(numbers, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.genetic.genetic_algorithm()

        # Print the results of the genetic algorithm
        self.genetic.printResults(result, numbers)
