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


    def _feasible(self,indices):
        for d in range(self.dimensions):
            used = sum(self.weights[i][d] for i in indicies)
            if used > self.capacities[d]:
                return False
        return True
        

    def exhaustive(self): 
        n = len(self.values)
        bestValue = -1 
        bestSubset = []
        
        for mask in range(1<<n):
            chosen = [i for i in range(n) if mask & (i<<i)]
            if self._feasible(chosen): 
                value = sum(self.values[i] for i in chosen)
                if value > bestValue: 
                    bestValue = value 
                    bestSubset = chosen 
        return bestSubset