import csv
import os
import random
import statistics
import threading
import time

from problems.SubsetSum import GeneticSubsetSum, SubsetSum
from problems.PartitionProblem import GeneticPartition, PartitionProblem
from problems.BinPacking import GeneticBinPacking, BinPacking
from problems.Knapsack import KnapsackGA, KnapsackExact

# Each GA configuration is run this many times, since results are random.
# Mean and standard deviation are reported instead of a single run.
REPEATS = 10

# Hard cap per exact-method call. Exhaustive methods can blow up on some
# random instances; without this the script could hang forever on one call.
# Raise this if you want to wait longer for bigger sizes to finish.
EXACT_TIMEOUT_SECONDS = 600

# Set to True (or env var ONLY_BOTTOMUP=1) to only measure bottom-up methods,
# skipping the parameter sweep and the already-measured recursive/dp/GA runs
ONLY_BOTTOMUP = os.environ.get("ONLY_BOTTOMUP") == "1"


class ExactTimeout(Exception):
    pass


# Cross-platform timeout: runs func in a daemon thread so it never blocks
# the script from continuing, even on Windows where signal.alarm is unavailable.
def withTimeout(func, seconds):
    result = {}

    def target():
        try:
            result["value"] = func()
        except Exception as error:
            result["error"] = error

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(seconds)

    if thread.is_alive():
        raise ExactTimeout()

    if "error" in result:
        raise result["error"]

    return result["value"]

SWEEP_FIELDNAMES = [
    "problem", "parameter", "value",
    "fitnessMean", "fitnessStd",
    "timeMean", "timeStd",
    "convergenceGenMean", "totalGenerationsMean",
]

GROWTH_FIELDNAMES = ["problem", "method", "size", "fitness", "time"]


def timeIt(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    return result, time.perf_counter() - start


# Runs a GA configuration REPEATS times and summarizes fitness, time and convergence
def runGA(gaClass, positionalArgs, gaParams):
    fitnesses, times, convergenceGens, totalGens = [], [], [], []

    for _ in range(REPEATS):
        ga = gaClass(*positionalArgs, **gaParams)
        result, elapsed = timeIt(ga.genetic_algorithm)
        fitnesses.append(result["bestFitness"])
        times.append(elapsed)
        convergenceGens.append(result["bestGeneration"])
        totalGens.append(len(result["history"]))

    return {
        "fitnessMean": statistics.mean(fitnesses),
        "fitnessStd": statistics.pstdev(fitnesses),
        "timeMean": statistics.mean(times),
        "timeStd": statistics.pstdev(times),
        "convergenceGenMean": statistics.mean(convergenceGens),
        "totalGenerationsMean": statistics.mean(totalGens),
    }


def logLine(logFile, text):
    print(text)
    logFile.write(text + "\n")


# Runs the baseline config with one parameter swapped out at a time (one-factor-at-a-time study)
def sweepParameter(csvWriter, logFile, problemName, gaClass, positionalArgs, baseline, paramName, values):
    for value in values:
        params = dict(baseline)
        params[paramName] = value
        row = runGA(gaClass, positionalArgs, params)
        row.update({"problem": problemName, "parameter": paramName, "value": value})
        csvWriter.writerow(row)

        logLine(logFile,
                f"{problemName:12} | {paramName:16} = {str(value):10} | "
                f"fitness={row['fitnessMean']:.3f}+/-{row['fitnessStd']:.3f} | "
                f"gen={row['convergenceGenMean']:.1f}/{row['totalGenerationsMean']:.1f} | "
                f"time={row['timeMean']:.3f}s+/-{row['timeStd']:.3f}s")


def baselineParams():
    return {
        "selectionType": "tournament",
        "populationSize": 150,
        "generations": 300,
        "tournamentSize": 3,
        "mutationProb": 0.05,
        "crossoverProb": 0.7,
        "elitismNum": 3,
        "patience": 40,
        "crossoverType": "onePoint",
        "mutationType": "bitFlip",
        "initMethod": "random",
    }


# Every parameter required by the assignment, swept one at a time against the baseline
SWEEPS = {
    "chromosomSize": [10, 20, 40, 60],
    "populationSize": [30, 100, 300, 600],
    "initMethod": ["random", "heuristic"],
    "selectionType": ["roulette", "ranking", "tournament"],
    "tournamentSize": [2, 5, 10, 20],
    "crossoverProb": [0.5, 0.7, 0.9],
    "crossoverType": ["onePoint", "twoPoint", "uniform"],
    "mutationProb": [0.01, 0.05, 0.1, 0.2],
    "mutationType": ["bitFlip", "swap"],
    "elitismNum": [1, 5, 10, 20],
    "generations": [50, 150, 300, 600],
    "patience": [10, 40, 100, 200],
}


def buildProblemInstance(problemName, size):
    if problemName == "SubsetSum":
        numbers = [random.randint(1, 60) for _ in range(size)]
        target = sum(numbers) // 2
        return (numbers, target)
    if problemName == "Partition":
        numbers = [random.randint(1, 60) for _ in range(size)]
        return (numbers,)
    if problemName == "BinPacking":
        items = [random.randint(1, 60) for _ in range(size)]
        return (items, 100)
    if problemName == "Knapsack":
        values = [random.randint(10, 100) for _ in range(size)]
        weights = [[random.randint(1, 30)] for _ in range(size)]
        return (values, weights, [size * 15])


def runProblemSweep(csvWriter, logFile, problemName, gaClass):
    baseSize = 30
    positionalArgs = buildProblemInstance(problemName, baseSize)
    baseline = baselineParams()
    baseline["chromosomSize"] = baseSize

    logLine(logFile, f"\n--- {problemName}: parameter sweep ---")

    for paramName, values in SWEEPS.items():
        if paramName == "chromosomSize":
            # Initial set size varies the problem instance itself, not just a GA param
            for size in values:
                args = buildProblemInstance(problemName, size)
                params = dict(baseline)
                params["chromosomSize"] = size
                row = runGA(gaClass, args, params)
                row.update({"problem": problemName, "parameter": "chromosomSize", "value": size})
                csvWriter.writerow(row)
                logLine(logFile,
                        f"{problemName:12} | {'chromosomSize':16} = {str(size):10} | "
                        f"fitness={row['fitnessMean']:.3f}+/-{row['fitnessStd']:.3f} | "
                        f"gen={row['convergenceGenMean']:.1f}/{row['totalGenerationsMean']:.1f} | "
                        f"time={row['timeMean']:.3f}s+/-{row['timeStd']:.3f}s")
            continue

        if paramName == "tournamentSize":
            fixedBaseline = dict(baseline)
            fixedBaseline["selectionType"] = "tournament"
            sweepParameter(csvWriter, logFile, problemName, gaClass, positionalArgs, fixedBaseline, paramName, values)
        else:
            sweepParameter(csvWriter, logFile, problemName, gaClass, positionalArgs, baseline, paramName, values)


# Times exact methods and the GA across growing input sizes, to study time growth.
# Each exact method stops being tested once it exceeds EXACT_TIMEOUT_SECONDS,
# since larger sizes would only be slower.
def sizeGrowthStudy(csvWriter, logFile, problemName, exactRunners, gaClass, sizes, methodsOnly=None):
    logLine(logFile, f"\n--- {problemName}: size growth study ---")
    skippedMethods = set()

    for size in sizes:
        positionalArgs = buildProblemInstance(problemName, size)
        runners = exactRunners(positionalArgs)

        if methodsOnly is not None:
            runners = {label: call for label, call in runners.items() if label in methodsOnly}

        for label, exactCall in runners.items():
            if label in skippedMethods:
                continue

            try:
                fitness, elapsed = timeIt(lambda: withTimeout(exactCall, EXACT_TIMEOUT_SECONDS))
                csvWriter.writerow({"problem": problemName, "method": label, "size": size, "fitness": fitness, "time": elapsed})
                logLine(logFile, f"{problemName:12} | {label:12} | size={size:5} | time={elapsed:.4f}s")
            except ExactTimeout:
                skippedMethods.add(label)
                logLine(logFile, f"{problemName:12} | {label:12} | size={size:5} | SKIPPED (exceeded {EXACT_TIMEOUT_SECONDS}s)")

        if methodsOnly is None:
            params = dict(baselineParams(), chromosomSize=size)
            gaSummary = runGA(gaClass, positionalArgs, params)
            csvWriter.writerow({"problem": problemName, "method": "GA", "size": size,
                                "fitness": gaSummary["fitnessMean"], "time": gaSummary["timeMean"]})
            logLine(logFile,
                    f"{problemName:12} | {'GA':12} | size={size:5} | "
                    f"fitness={gaSummary['fitnessMean']:.3f} | time={gaSummary['timeMean']:.3f}s")


def subsetSumExactRunners(positionalArgs):
    numbers, target = positionalArgs
    exact = SubsetSum()

    def recursiveQuality():
        subset = exact.recursiveSubsetSum(numbers, len(numbers), target)
        return sum(subset) if subset is not None else 0

    def dpQuality():
        subset = exact.dpSubsetSum(numbers, len(numbers), target)
        return sum(subset) if subset is not None else 0

    def bottomUpQuality():
        found = exact.BottomUpisSubsetSum(numbers, target)
        return target if found else 0

    return {"recursive": recursiveQuality, "dpTopDown": dpQuality, "bottomUp": bottomUpQuality}


def partitionExactRunners(positionalArgs):
    numbers, = positionalArgs
    exact = PartitionProblem()
    return {
        "recursive": lambda: int(exact.recursiveEqualPartition(numbers)),
        "dpTopDown": lambda: int(exact.dpEqualPartition(numbers)),
        "bottomUp": lambda: int(exact.BottomUpequalPartition(numbers)),
    }


def binPackingExactRunners(positionalArgs):
    items, capacity = positionalArgs
    exact = BinPacking()
    return {
        "recursive": lambda: exact.recursiveMinBins(items, capacity),
        "dpTopDown": lambda: exact.dpMinBins(items, capacity),
        "bottomUp": lambda: exact.bottomUpBinPacking(items, capacity),
    }


def knapsackExactRunners(positionalArgs):
    values, weights, capacities = positionalArgs
    wt = [w[0] for w in weights]
    W = capacities[0]
    exact = KnapsackExact()
    return {
        "recursive": lambda: exact.recursiveKnapsack(W, values, wt),
        "dpTopDown": lambda: exact.dpKnapsack(W, values, wt),
        "bottomUp": lambda: exact.buttomUpKnapsack(W, values, wt),
    }


# Growth sizes are capped so exhaustive recursion stays feasible.
# Bin Packing branches the hardest, so its ceiling is the lowest.
GROWTH_SIZES = {
    "SubsetSum": [10, 15, 18, 20, 22, 24],
    "Partition": [10, 15, 18, 20, 22, 24],
    "BinPacking": [8, 10, 12, 14, 16, 18, 20],
    "Knapsack": [10, 14, 18, 20, 22, 24],
}


def main():
    random.seed(42)
    os.makedirs("results", exist_ok=True)

    if ONLY_BOTTOMUP:
        runBottomUpOnly()
        return

    with open("results/report.txt", "w") as logFile:
        logLine(logFile, "GA comparative study")
        logLine(logFile, f"Each GA configuration repeated {REPEATS} times (mean +/- std shown)")

        with open("results/parameter_sweep.csv", "w", newline="") as f:
            csvWriter = csv.DictWriter(f, fieldnames=SWEEP_FIELDNAMES)
            csvWriter.writeheader()

            runProblemSweep(csvWriter, logFile, "SubsetSum", GeneticSubsetSum)
            runProblemSweep(csvWriter, logFile, "Partition", GeneticPartition)
            runProblemSweep(csvWriter, logFile, "BinPacking", GeneticBinPacking)
            runProblemSweep(csvWriter, logFile, "Knapsack", KnapsackGA)

        with open("results/size_growth.csv", "w", newline="") as f:
            csvWriter = csv.DictWriter(f, fieldnames=GROWTH_FIELDNAMES)
            csvWriter.writeheader()

            sizeGrowthStudy(csvWriter, logFile, "SubsetSum", subsetSumExactRunners, GeneticSubsetSum, GROWTH_SIZES["SubsetSum"])
            sizeGrowthStudy(csvWriter, logFile, "Partition", partitionExactRunners, GeneticPartition, GROWTH_SIZES["Partition"])
            sizeGrowthStudy(csvWriter, logFile, "BinPacking", binPackingExactRunners, GeneticBinPacking, GROWTH_SIZES["BinPacking"])
            sizeGrowthStudy(csvWriter, logFile, "Knapsack", knapsackExactRunners, KnapsackGA, GROWTH_SIZES["Knapsack"])

        logLine(logFile, "\nDone. See results/parameter_sweep.csv and results/size_growth.csv for raw data.")


# Only measures bottomUp, writes to separate files so previous results aren't overwritten
def runBottomUpOnly():
    with open("results/report_bottomup.txt", "w") as logFile:
        logLine(logFile, "Bottom-up only run")

        with open("results/size_growth_bottomup.csv", "w", newline="") as f:
            csvWriter = csv.DictWriter(f, fieldnames=GROWTH_FIELDNAMES)
            csvWriter.writeheader()

            sizeGrowthStudy(csvWriter, logFile, "SubsetSum", subsetSumExactRunners, GeneticSubsetSum, GROWTH_SIZES["SubsetSum"], methodsOnly=["bottomUp"])
            sizeGrowthStudy(csvWriter, logFile, "Partition", partitionExactRunners, GeneticPartition, GROWTH_SIZES["Partition"], methodsOnly=["bottomUp"])
            sizeGrowthStudy(csvWriter, logFile, "BinPacking", binPackingExactRunners, GeneticBinPacking, GROWTH_SIZES["BinPacking"], methodsOnly=["bottomUp"])
            sizeGrowthStudy(csvWriter, logFile, "Knapsack", knapsackExactRunners, KnapsackGA, GROWTH_SIZES["Knapsack"], methodsOnly=["bottomUp"])

        logLine(logFile, "\nDone.")


if __name__ == "__main__":
    main()
