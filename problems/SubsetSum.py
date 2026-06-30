import problems.Base as Base
import random

# Subclass for the Subset Sum problem, inheriting from the Base class
class GeneticSubsetSum(Base.Base):
    def __init__(self, numbers, target, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience):
        super().__init__(selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        self.numbers = numbers
        self.target = target

    #Calculate the fitness of an individual, which is based on how close the sum of the selected numbers is to the target sum
    def fitness(self, individual):
        total = 0

        for i in range(len(individual)):
            if individual[i] == 1:
                total += self.numbers[i]

        difference = abs(self.target - total)
        return 1 / (1 + difference)

    def printResults(self, result, numbers, target):
        best = result["bestIndividual"]
        solution = []

        for i in range(len(best)):
            if best[i] == 1:
                solution.append(numbers[i])

        print()
        print("Numbers:", numbers)
        print("Target sum:", target)
        print("Best chromosome:", best)
        print("Subset:", solution)
        print("Sum:", sum(solution))
        print("Fitness:", result["bestFitness"])
        print("Generation:", result["bestGeneration"])

class SubsetSum:

    def recursiveSubsetSum(self, numbers, index, target):
        if target == 0:
            return []
        if index == 0:
            return None

        if numbers[index - 1] <= target:
            resultado = self.recursiveSubsetSum(numbers, index - 1, target - numbers[index - 1])
            if resultado != None:
                return resultado + [numbers[index - 1]]

        return self.recursiveSubsetSum(numbers, index - 1, target)


    def dpSubsetSum(self, numbers, index, target, memo=None):
        if memo is None:
            memo = {}
        
        key = (index, target)
        
        if key in memo:
            return memo[key]
        
        if target == 0:
            return []
        if index == 0:
            return None
        
        if numbers[index - 1] <= target:
            resultado = self.dpSubsetSum(numbers, index - 1, target - numbers[index - 1], memo)
            if resultado is not None:
                memo[key] = resultado + [numbers[index - 1]]
                return memo[key]
        
        resultado = self.dpSubsetSum(numbers, index - 1, target, memo)
        memo[key] = resultado
        return memo[key]


    def printResults(self, result, numbers, target):
        print()
        print(f"Numbers: {numbers}")
        print(f"Target: {target}")
        print(f"Result: {result}")


    def genetic(self):

        # Generate random numbers and a target sum for the Subset Sum problem
        numbers = [random.randint(1, 60) for i in range(20)]
        target = 100

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
        self.genetic = GeneticSubsetSum(numbers, target, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.genetic.genetic_algorithm()

        # Print the results of the genetic algorithm
        self.genetic.printResults(result, numbers, target)

        # Generate random numbers and a target sum for the Subset Sum problem
        numbers = [random.randint(1, 100) for i in range(50)]
        target = 450

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
        self.genetic = GeneticSubsetSum(numbers, target, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.genetic.genetic_algorithm()

        # Print the results of the genetic algorithm
        self.genetic.printResults(result, numbers, target)

        # Generate random numbers and a target sum for the Subset Sum problem
        numbers = [random.randint(10, 60) for i in range(100)]

        target = 1000

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
        self.genetic = GeneticSubsetSum(numbers, target, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.genetic.genetic_algorithm()

        # Print the results of the genetic algorithm
        self.genetic.printResults(result, numbers, target)