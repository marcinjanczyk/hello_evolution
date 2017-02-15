import string
import random
import functools
import time

allSymbols = string.digits + string.ascii_letters + string.punctuation + ' '

def giveRandomChar():
    """Returns  1 character from: digits + small_letters + big letters + punctutation"""
    return allSymbols[random.randrange(0,len(allSymbols),1)]

def calculateFitness(testString,targetString):
    """
    Function to calculate fitness
    testString = string tested against targetString
    targetString = string which is the solution for our GA
    Fitness is expressed as number of correct letters in correct position divided by total numbers of characters
    Returns calulated fitness in range <0,1>
    """
    fitness = 0
    for i in zip(testString,targetString):
        if i[0] == i[1]:
            fitness += 1
    return(fitness / len(targetString))
    
def createNewChromosome(lengthOfChromosome):
    """Creates new random set of letters (aka new genotype)"""
    tempString = ''
    for _ in range(lengthOfChromosome):
        tempString += giveRandomChar()
    return tempString

def doCrossover(parentA, parentB):
    """
    Takes two strings: parentA and parentB
    Performs two point crossover over parentA and parentB
    Returns 2 children - made from parents' crossover
    """
    locus = random.sample(range(len(parentB)),2)
    locus.sort()        
    childA = parentA[:locus[0]] + parentB[locus[0]:locus[1]] + parentA[locus[1]:]
    childB = parentB[:locus[0]] + parentA[locus[0]:locus[1]] + parentB[locus[1]:]
    return [childA, childB]

def doMutation(parent):
    """Performs mutation at """
    mutationLocus = random.randint(0,len(parent)-1)
    return(parent[:mutationLocus] + giveRandomChar() + parent[mutationLocus+1:])
 
def randomParents(phenotypeList,weightList):
    """
    Takes two lists: phenotypes and weights(fitness)
    Returns two DIFFERENT parents
    """
    # Copy lists to new variables
    zipped = list(zip(phenotypeList,weightList))
    totalSum = sum(x[1] for x in zipped)
    randomed = random.uniform(0,totalSum)
    counter = 0.0
    for x in range(len(zipped)):
        counter += zipped[x][1]
        if randomed <= counter:
            parentA = zipped[x][0]
            del zipped[x]
            break
    totalSum = sum(x[1] for x in zipped)
    randomed = random.uniform(0,totalSum)
    counter = 0.0
    for x in range(len(zipped)):
        counter += zipped[x][1]
        if randomed <= counter:
            parentB = zipped[x][0]
            del zipped[x]
            break
    return([parentA,parentB])

def startEvolution(targetString = "Hello-evolution", totalPopulation = 1000, defaultMutationRate = 0.05):
    
    starTime = time.time()
    ## create population and calculate fitness for each chromosome
    population = [createNewChromosome(len(targetString)) for _ in range(totalPopulation)]
    fitnessVal = [calculateFitness(i,targetString) for i in population]
    
    ## here we define function calculateFitness with "hard-added" targetString for comparison with testStrings
    partialFitness = functools.partial(calculateFitness, targetString = targetString)
    
    ## sorting, the best fitted chromosomes are at the begging
    population = sorted(population, key = partialFitness, reverse = True)
    fitnessVal = sorted(fitnessVal, reverse = True)
    
    generation = 1
    bestPhenotype = population[0]

    ## lay-out of summary based on work of github user thegrymek
    print('Generation | Fitness | Phenotype' + ' '*(len(targetString)- 9)  + ' | MutationRate')
    print('--------------------------------------' + '-' * len(targetString))
    partialLine = '{0:>10} | {1:>7} | {2:>9} | {3:>12}'.format(
                generation-1,
                round(fitnessVal[0],2),
                population[0],
                round(defaultMutationRate,2)
            )
    print(partialLine)

    while not bestPhenotype == targetString:
        ## selecting the best 20% of population
        population = population[:int(len(population)*0.2)]
        fitnessVal = fitnessVal[:int(len(fitnessVal)*0.2)]
                                
        ## calulcating rate of mutation - how often will genes mutate ?
        mutationRate = (1 - len(set(population)) / len(population) ) * 0.4      ## here we dynamically define mutation rate
        mutationRate = max(defaultMutationRate,mutationRate)                    ## but we can't let happen to not mutate at all - important in small populations
        ## populating with crossover
        while len(population) < totalPopulation:
            ## choose parents
            twoParents = randomParents(population,fitnessVal)
            ## create 2 children
            newChildren = doCrossover(twoParents[0],twoParents[1])
            
            ## mutation - does he mutate at creating child ?
            doWeMutate = random.random()
            if doWeMutate < mutationRate:
                newChildren[0] = doMutation(newChildren[0])
            elif doWeMutate > (1-mutationRate):
                newChildren[1] = doMutation(newChildren[1])
            
            ## append do existing population
            population.append(newChildren[0])
            population.append(newChildren[1])
            fitnessVal.append(partialFitness(newChildren[0]))
            fitnessVal.append(partialFitness(newChildren[1]))
        
        ## sort population and its' fitness by fitness
        population = sorted(population, key = partialFitness, reverse = True)
        fitnessVal = sorted(fitnessVal, reverse = True)
        bestPhenotype = population[0] 
        ## print another line of summary
        ## lay-out of summary based on work of github user thegrymek
        partialLine = '{0:>10} | {1:>7} | {2:>9} | {3:>12}'.format(
                generation,
                round(fitnessVal[0],2),
                population[0],
                round(mutationRate,2)
            )
        print(partialLine)
        generation += 1
    endTime = time.time()
    print("I found best solution in ", generation-1, "generations !")
    print("Solution has been found in ", round(endTime - starTime,2), "sec")

# END