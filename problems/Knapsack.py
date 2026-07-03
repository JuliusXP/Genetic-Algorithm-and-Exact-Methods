import random 

from genetic_algorithm import GeneticAlgorithm 

class KnapsackGA(GeneticAlgorithm):
    
    def __int__(self, values, weights, capacities, **gaParams):
        super().__init__(**gaParams)
        self.values = values 
        self.weights = weights
        self.capacities = capacities 
        self.dimensions = len(capacities)

        #create one gene per item 
    def createIndividual(self):
        return [random.randint(0,1) for _ in self.values ]
    
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
    

    def solve(self):
         result = self.run()
         chromosome = result["bestIndividual"]
         return [i for i, gene in enumerate(chromosome) if gene]
class KnapsackExact: 
    def __int__(self, values, weights, capacities):
        self.values = values
        self.weights = weights
        self.capacities = capacities
        self.dimensions = len(capacities)