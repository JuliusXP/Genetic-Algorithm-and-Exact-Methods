import random
import copy

"""

Dudas para el profe:
* Deberia de crear una variable para implementar el tamanyo de la cantidad de alelos del cromosoma?

"""

#Base class for Genetic Algorithms
class Base():
    def __init__(self, selectionType, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience):
        self.selectionType = selectionType
        self.populationSize = populationSize
        self.generations = generations
        self.tournamentSize = tournamentSize
        self.mutationProb = mutationProb
        self.crossoverProb = crossoverProb
        self.elitismNum = elitismNum
        self.patience = patience

    #Create an Individual chromosom, this function is polymorphic, it will be declared in the classes of each genetic algorithm
    def createIndividual(self):
        pass
    
    #Create a population of individuals
    def createPopulation(self):

        population = [self.createIndividual() for i in range(self.populationSize)]
        return population
    
    #Calculate the fitness of an individual, this function is polymorphic, it will be declared in the classes of each genetic algorithm
    def fitness(self, individual):
        pass

    #Select an individual from the population based on the selection type
    def selection(self, evaluated):

        if self.selectionType == "ranking":
            return self.rankingSelection(evaluated)

        if self.selectionType == "roulette":
            return self.rouletteSelection(evaluated)

        if self.selectionType == "tournament":
            return self.tournamentSelection(evaluated)

    #Select an individual based on ranking
    def rankingSelection(self, evaluated):

        #Sort the evaluated population by fitness in descending order
        ranking = sorted(evaluated, key=lambda x: x[1], reverse=True)
        rankingSize = len(ranking)

        #Create weights for each individual based on their rank, in this case the weight is the rank itself, 
        #example if there are 5 individuals, the weights will be [5, 4, 3, 2, 1], so the first individual has a weight of 5, the second has a weight of 4, and so on
        weights = []
        for i in range(rankingSize):
            weights.append(rankingSize-i)

        # Select an individual based on the weights
        selected = random.choices( ranking, weights, k=1 )[0]
        return selected[0]

    #Select an individual based on roulette selection
    def rouletteSelection(self, evaluated):

        # Create weights for each individual based on their fitness, in this case the weight it's literally the fitness value, 
        # so the higher the fitness, the higher the probability of being selected
        # example if there are 5 individuals, the weights will be [10, 8, 6, 4, 2], so the first individual has a weight of 10, the second has a weight of 8, and so on
        weights = []
        for individual, fitness in evaluated:
            weights.append(fitness)

        # Select an individual based on the weights
        selected = random.choices(evaluated, weights, k=1)[0]
        return selected[0]

    # Select an individual based on tournament selection
    def tournamentSelection(self, evaluated):

        #Select a random sample of individuals from the evaluated population for the tournament
        tournament = random.sample(evaluated, self.tournamentSize)

        #Select the best individual, in this case it's the first one
        best = tournament[0]

        # Compare the rest of the individuals in the tournament and select the best one
        for candidate in tournament[1:]:
            if candidate[1] > best[1]:
                best = candidate

        return best[0]

    # Crossover two parents to create two children
    def crossover(self, parent1, parent2):

        # Check if the crossover should be performed based on the crossover probability
        if random.random() > self.crossoverProb:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Choose a random crossover point
        point = random.randint(1, len(parent1)-1)

        # Create two children by combining the parents at the crossover point
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return child1, child2
    
    # Mutate an individual by flipping bits based on the mutation probability
    def mutation(self, individual):

        for i in range(len(individual)):
            # Check if the mutation should be performed based on the mutation probability
            if random.random() < self.mutationProb:
                # Bit Flip
                if individual[i] == 0:
                    individual[i] = 1
                else:
                    individual[i] = 0

        return individual
    
    # Implement elitism, which is the process of selecting the best individuals from the current generation and carrying them over to the next generation without modification
    def elitism(self, evaluated):

        populationSorted = sorted(evaluated, key=lambda x: x[1], reverse=True)
        
        elite = []
        for i in range(self.elitismNum):
            elite.append(copy.deepcopy(populationSorted[i][0]))

        return elite
    
    # Create a new generation of individuals based on the evaluated population
    def createNewGeneration(self, evaluated):

        newPopulation = []

        # 1. Implement elitism
        elite = self.elitism(evaluated)
        for individual in elite:
            newPopulation.append(copy.deepcopy(individual))

        # 2. Create new individuals through selection, crossover, and mutation until the new population is filled
        while len(newPopulation) < len(evaluated):

            parent1 = self.selection(evaluated)
            parent2 = self.selection(evaluated)

            child1, child2 = self.crossover(parent1, parent2)

            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            newPopulation.append(child1)

            if len(newPopulation) < len(evaluated):
                newPopulation.append(child2)

        return newPopulation

    # Implement the genetic algorithm, which is the main loop that runs the genetic algorithm for a specified number of generations or until a stopping criterion is met
    def genetic_algorithm(self):

        population = self.createPopulation()

        # Initialize variables to keep track of the best individual, its fitness, the generation it was found in, and a counter for no improvement
        bestIndividual = None
        bestFitness = float("-inf")
        bestGeneration = 0
        noImprovement = 0
        history = []

        for generation in range(self.generations):

            # Evaluate the population and calculate the fitness of each individual
            evaluated = [(individual, self.fitness(individual)) for individual in population]

            # Find the best individual in the current generation
            currentBest, currentFitness = max(evaluated, key=lambda x: x[1])
            history.append(currentFitness)

            # Update the best individual if the current best is better than the previous best
            if currentFitness > bestFitness:
                bestIndividual = copy.deepcopy(currentBest)
                bestFitness = currentFitness
                bestGeneration = generation
                noImprovement = 0

            else:
                noImprovement += 1

            #Stopping criterion based on patience, if there is no improvement for a certain number of generations, the algorithm will stop 
            if noImprovement >= self.patience:
                return {
                    "bestIndividual": bestIndividual,
                    "bestFitness": bestFitness,
                    "bestGeneration": bestGeneration,
                    "finalPopulation": population,
                    "history": history
                }

            population = self.createNewGeneration(evaluated)

        return {

            "bestIndividual": bestIndividual,
            "bestFitness": bestFitness,
            "bestGeneration": bestGeneration,
            "finalPopulation": population,
            "history": history
        }
    
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