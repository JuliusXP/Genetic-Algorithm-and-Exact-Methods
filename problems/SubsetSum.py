import Base
import random

# Subclass for the Subset Sum problem, inheriting from the Base class
class SubsetSum(Base.Base):
    def __init__(self, numbers, target, selectionType, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience):
        super().__init__(selectionType, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        self.numbers = numbers
        self.target = target

    #Create an Individual chromosome, which is a binary representation of the subset selection
    def createIndividual(self):
        individual = []

        for i in range(len(self.numbers)):
            individual.append(random.randint(0,1))

        return individual

    #Calculate the fitness of an individual, which is based on how close the sum of the selected numbers is to the target sum
    def fitness(self, individual):
        total = 0

        for i in range(len(individual)):
            if individual[i] == 1:
                total += self.numbers[i]

        difference = abs(self.target - total)
        return 1 / (1 + difference)