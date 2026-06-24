import problems.SubsetSum as SubsetSum
import random

def main():

    # Generate random numbers and a target sum for the Subset Sum problem
    numbers = [random.randint(1, 100) for i in range(50)]
    target = random.randint(100, 500)
    selectionType = "tournament"
    populationSize = 1000
    generations = 1000
    tournamentSize = 5
    crossoverProb = 0.8
    mutationProb = 0.1
    elitismNum = 10
    patience = 10

    # Create an instance of the SubsetSum class and run the genetic algorithm
    subsetSum = SubsetSum.SubsetSum(numbers, target, selectionType, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
    result = subsetSum.genetic_algorithm()

    # Print the results of the genetic algorithm
    subsetSum.printResults(result, numbers, target)

if __name__ == "__main__":
    main()