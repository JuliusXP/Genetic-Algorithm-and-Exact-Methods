import problems.Base as Base
import random
 
# Subclass for the Bin Packing problem, inheriting from the Base class
class GeneticBinPacking(Base.Base):
    def __init__(self, items, capacity, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience, crossoverType="onePoint", mutationType="bitFlip"):
        super().__init__(selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience, crossoverType, mutationType)
        self.items = items
        self.capacity = capacity

 # Each gene is the bin index assigned to that item
 # In which box is it?
 # Chromosome is a list, i is the positio of the object i.
    def createIndividual(self, chromosomSize):
        return [random.randint(0, chromosomSize - 1) for _ in range(chromosomSize)]
    
# change mutation to select random box
    def mutation(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutationProb:
                individual[i] = random.randint(0, len(individual) - 1)
        return individual
    

    def fitness(self, individual):
        loads = {} #stores weight for each box, {0: 15, 2: 8}, for example weight for box 0 is 15, for box 2 is 8
        for i, binId in enumerate(individual):
            loads[binId] = loads.get(binId, 0) + self.items[i]

        # How much is it over capacity
        overflow = sum(max(0, load - self.capacity) for load in loads.values())
        if overflow > 0: #invalid solution, bad score, score under 1
            return 1 / (1 + overflow)
        return 1 + (1 / len(loads)) #valid solution, good score, over 1. Better score if it uses less boxes

    def printResults(self, result, items, capacity):
        best = result["bestIndividual"]
        bins = {}
        for i, binId in enumerate(best):
            bins.setdefault(binId, []).append(items[i])

        print()
        print("Items:", items)
        print("Capacity:", capacity)
        print("Bins used:", len(bins))
        for binId, binItems in bins.items():
            print(f"  Bin {binId}: {binItems} (load {sum(binItems)})")
        print("Fitness:", result["bestFitness"])
        print("Generation:", result["bestGeneration"])


class BinPacking:
    #index: which index are we at | bins: list of opened boxes
    def recursive(self, items, capacity, index, bins):
        if index == len(items):
            return len(bins)

        best = float("inf")

        # First path: insert current obj inside opened box, with enough capacity
        for i in range(len(bins)):
            if bins[i] + items[index] <= capacity:
                bins[i] += items[index]
                best = min(best, self.recursive(items, capacity, index + 1, bins))
                bins[i] -= items[index] # backtrack step

        # Second path: open new box for obj
        bins.append(items[index])
        best = min(best, self.recursive(items, capacity, index + 1, bins))
        bins.pop() # backtrack step
        return best 

    def recursiveMinBins(self, items, capacity):
        return self.recursive(items, capacity, 0, [])

    def dp(self, items, capacity, index, bins, memo):
        if index == len(items):
            return len(bins)

        # key = index, sorted tuple of bins.
        # we sort the bins becasue it doesnt matter the order in which we loaded the bins.
        # it only matter which loaded bins exist at the moment.
        key = (index, tuple(sorted(bins)))
        if key in memo:
            return memo[key]

        best = float("inf")
        tried = set()
        for i in range(len(bins)):
            if bins[i] in tried:
                continue
            tried.add(bins[i])

            if bins[i] + items[index] <= capacity:
                bins[i] += items[index]
                best = min(best, self.dp(items, capacity, index + 1, bins, memo))
                bins[i] -= items[index]


        bins.append(items[index])
        best = min(best, self.dp(items, capacity, index + 1, bins, memo))
        bins.pop()

        memo[key] = best # save in memo
        return best

    def dpMinBins(self, items, capacity):
        return self.dp(items, capacity, 0, [], {})

    def printResults(self, items, capacity, result):
        print()
        print("Items:", items)
        print("Capacity:", capacity)
        print("Minimum bins:", result)


    def genetic(self):
        # small BinPacking
        items = [random.randint(1, 60) for i in range(20)]
        capacity = 100
        selectionType = "tournament"
        chromosomSize = len(items)
        populationSize = 50
        generations = 100
        tournamentSize = 3
        crossoverProb = 0.7
        mutationProb = 0.05
        elitismNum = 2
        patience = 20

        self.geneticSolver = GeneticBinPacking(items, capacity, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.geneticSolver.genetic_algorithm()
        self.geneticSolver.printResults(result, items, capacity)

        # medium BinPacking
        items = [random.randint(1, 100) for i in range(50)]
        capacity = 150
        selectionType = "tournament"
        chromosomSize = len(items)
        populationSize = 200
        generations = 500
        tournamentSize = 5
        crossoverProb = 0.8
        mutationProb = 0.1
        elitismNum = 10
        patience = 50

        self.geneticSolver = GeneticBinPacking(items, capacity, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.geneticSolver.genetic_algorithm()
        self.geneticSolver.printResults(result, items, capacity)

        # big BinPacking
        items = [random.randint(10, 60) for i in range(100)]
        capacity = 200
        selectionType = "tournament"
        chromosomSize = len(items)
        populationSize = 1000
        generations = 2000
        tournamentSize = 8
        crossoverProb = 0.9
        mutationProb = 0.15
        elitismNum = 20
        patience = 100

        self.geneticSolver = GeneticBinPacking(items, capacity, selectionType, chromosomSize, populationSize, generations, tournamentSize, mutationProb, crossoverProb, elitismNum, patience)
        result = self.geneticSolver.genetic_algorithm()
        self.geneticSolver.printResults(result, items, capacity)



    
    
    def bottomUpBinPacking(self, items, capacity):
        n = len(items)
        numMasks = 1 << n # how many subsets possible with n elements

        # subsetSum[mask] = total weight of items in that subset
        subsetSum = [0] * numMasks
        for mask in range(1, numMasks): # mask bits represents if an object is in the subset or not
            lastItem = (mask & (-mask)).bit_length() - 1 # last active bit 

            # subset weight without lastItem + lastItem weight, to go bottomUp.
            subsetSum[mask] = subsetSum[mask ^ (1 << lastItem)] + items[lastItem]

        # canditate[mask] = subset fits in a single bin
        candidate = [subsetSum[mask] <= capacity for mask in range(numMasks)]

        # minBins[mask] = min bins needed for that subset
        minBins = [0] * numMasks

        # bottomUp, builds table from small subsets to big subsets
        for mask in range(1, numMasks):
            best = float("inf")
            submask = mask # all subsets inside mask
            while submask > 0: 
                if candidate[submask]: # try with last filled box.
                    rest = mask ^ submask # obj of mask NOT in submask
                    best = min(best, minBins[rest] + 1)
                submask = (submask - 1) & mask
            minBins[mask] = best

        return minBins[numMasks - 1]

