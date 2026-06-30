import random
import problems.SubsetSum as SubsetSum
import problems.PartitionProblem as Partition

def main():

    # Generate random numbers and a target sum for the Subset Sum problem
    numbersSubset = [random.randint(1, 10) for i in range(10)]
    targetSubset = random.randint(1, 50)

    subset = SubsetSum.SubsetSum()
    recursiveSubsetResult = subset.recursiveSubsetSum(numbersSubset, len(numbersSubset), targetSubset)
    subset.printResults(recursiveSubsetResult, numbersSubset, targetSubset)

    dpSubsetResult = subset.dpSubsetSum(numbersSubset, len(numbersSubset), targetSubset)
    subset.printResults(dpSubsetResult, numbersSubset, targetSubset)

    subset.genetic()

    # Generate random numbers for the Partition Problem
    numbersPartition = [random.randint(1, 10) for i in range(10)]

    partition = Partition.PartitionProblem()
    recursivePartitionResult = partition.recursiveEqualPartition(numbersPartition)
    partition.printResults(numbersPartition, recursivePartitionResult)

    dpPartitionResult = partition.dpEqualPartition(numbersPartition)
    partition.printResults(numbersPartition, dpPartitionResult)

    partition.genetic()

if __name__ == "__main__":
    main()