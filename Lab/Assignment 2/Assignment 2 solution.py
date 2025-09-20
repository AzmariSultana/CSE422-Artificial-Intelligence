import random
import math

gridSize = 25
populationSize = 6
maxGenerations = 15
mutationRate = 0.1

components = {
    "ALU": (5, 5),
    "Cache": (7, 4),
    "Control Unit": (4, 4),
    "Register File": (6, 6),
    "Decoder": (5, 3),
    "Floating Unit": (5, 5)
}
componentNames = list(components.keys())

connections = [
    ("Register File", "ALU"),
    ("Control Unit", "ALU"),
    ("ALU", "Cache"),
    ("Register File", "Floating Unit"),
    ("Cache", "Decoder"),
    ("Decoder", "Floating Unit")
]

def readInput(filename="input.txt"):
    population = []
    with open(filename, 'r') as file:
        for line in file:
            nums = list(map(int, line.split()))
            individual = [(nums[i], nums[i+1]) for i in range(0, len(nums), 2)]
            population.append(individual)
    return population

def writeOutput(best, fitness, overlaps, wiringLength, area, filename="output.txt"):
    with open(filename, "w") as f:
        f.write(f"Best Fitness: {fitness:.2f}\n")
        f.write(f"Overlaps: {overlaps}\n")
        f.write(f"Wiring Length: {wiringLength:.2f}\n")
        f.write(f"Bounding Box Area: {area}\n")
        f.write("Optimal Coordinates (x, y):\n")
        for name, coord in zip(componentNames, best):
            f.write(f"{name}: {coord}\n")

def createIndividual():
    individual = []
    for comp in components:
        w, h = components[comp]
        x = random.randint(0, gridSize - w)
        y = random.randint(0, gridSize - h)
        individual.append((x, y))
    return individual

def createInitialPopulation():
    return [createIndividual() for i in range(populationSize)]

def calculateFitness(chromosome):
    overlaps = 0
    for i in range(len(chromosome)):
        x1, y1 = chromosome[i]
        w1, h1 = components[componentNames[i]]
        for j in range(i + 1, len(chromosome)):
            x2, y2 = chromosome[j]
            w2, h2 = components[componentNames[j]]
            if not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1):
                overlaps += 1

    wiringLength = 0
    for a, b in connections:
        i, j = componentNames.index(a), componentNames.index(b)
        xa, ya = chromosome[i]
        xb, yb = chromosome[j]
        wa, ha = components[a]
        wb, hb = components[b]
        ca = (xa + wa / 2, ya + ha / 2)
        cb = (xb + wb / 2, yb + hb / 2)
        dist = math.sqrt((ca[0] - cb[0]) ** 2 + (ca[1] - cb[1]) ** 2)
        wiringLength += dist

    xs = [x for (x, y) in chromosome]
    ys = [y for (x, y) in chromosome]
    ws = [components[name][0] for name in componentNames]
    hs = [components[name][1] for name in componentNames]
    xMin = min(xs)
    xMax = max(xs[i] + ws[i] for i in range(len(xs)))
    yMin = min(ys)
    yMax = max(ys[i] + hs[i] for i in range(len(ys)))
    area = (xMax - xMin) * (yMax - yMin)

    fitness = - (1000 * overlaps + 2 * wiringLength + 1 * area)
    return fitness, overlaps, wiringLength, area

def selectParents(population):
    tournamentSize = 3

    # First parent: best from selection
    tournamentSample = random.sample(population, tournamentSize)
    bestFromTournament = max(tournamentSample, key=lambda candidate: calculateFitness(candidate)[0])

    # Second parent: best from another random selection
    anotherSample = random.sample(population, tournamentSize)
    bestFromSample = max(anotherSample, key=lambda candidate: calculateFitness(candidate)[0])

    return bestFromTournament, bestFromSample

def singlePointCrossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    child1 = p1[:point] + p2[point:]
    child2 = p2[:point] + p1[point:]
    return child1, child2

def twoPointCrossover(p1, p2):
    point1 = random.randint(0, len(p1) - 2)
    point2 = random.randint(point1 + 1, len(p1) - 1)
    child1 = p1[:point1] + p2[point1:point2] + p1[point2:]
    child2 = p2[:point1] + p1[point1:point2] + p2[point2:]
    return child1, child2

def mutate(chromosome):
    newChromosome = chromosome.copy()     # Create a copy
    if random.random() < mutationRate:
        index = random.randint(0, len(newChromosome) - 1)
        w, h = components[componentNames[index]]
        newCoord = (random.randint(0, gridSize - w), random.randint(0, gridSize - h))
        newChromosome[index] = newCoord
    return newChromosome

def geneticAlgorithm():
    population = readInput()
    for gen in range(maxGenerations):
        fitnessScores = [calculateFitness(c) for c in population]

        indices = list(range(len(population)))
        indices.sort(key=lambda i: fitnessScores[i][0], reverse=True)
        sortedPopulation = [population[i] for i in indices]

        newPopulation = [c.copy() for c in sortedPopulation[:2]]
        while len(newPopulation) < populationSize:
            p1, p2 = selectParents(sortedPopulation)
            c1, c2 = singlePointCrossover(p1, p2)
            #c1, c2 = twoPointCrossover(p1, p2)     #for task2 just uncomment this line
            c1 = mutate(c1)
            c2 = mutate(c2)
            newPopulation += [c1, c2]
        population = newPopulation[:populationSize]

    best = max(population, key=lambda c: calculateFitness(c)[0])
    fitness, overlaps, wiringLength, area = calculateFitness(best)
    writeOutput(best, fitness, overlaps, wiringLength, area)

if __name__ == "__main__":
    geneticAlgorithm()
