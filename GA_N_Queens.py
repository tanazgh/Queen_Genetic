import random
import time

def create_random_chromosome(size): 
    return [random.randint(1, size) for _ in range(size)]

def print_chromosome(chrom):
    print("Chromosome = {},  Fitness = {}"
        .format(str(chrom), fitness(chrom)))    

def fitness(chromosome): # check if queens are garding each other
    score = 0

    for row in range(queen_num):
        col = chromosome[row]
        
        for other_row in range(queen_num):
            
            #queens cannot pair with itself
            if other_row == row:
                continue
            if chromosome[other_row] == col:
                continue
            if other_row + chromosome[other_row] == row + col:
                continue
            if other_row - chromosome[other_row] == row - col:
                continue
            #score++ if every pair of queens are non-attacking.
            score += 1
    
    #divide by 2 as pairs of queens are commutative
    return score/2

def probability(chromosome, fitness):
    return fitness(chromosome) / max_fitness

def random_pick(population, probabilities):
    population_with_probabilty = zip(population, probabilities)
    total = sum(w for c, w in population_with_probabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
        
def reproduce(x, y): #doing cross_over between two chromosomes
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

def mutate(x):  #randomly changing the value of a random index of a chromosome
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

def genetic_queen(population, fitness, mutation_probability):
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities) #best chromosome 1
        y = random_pick(population, probabilities) #best chromosome 2
        child = reproduce(x, y) #creating two new chromosomes from the best 2 chromosomes
        if random.random() < mutation_probability:
            child = mutate(child)
        print_chromosome(child)
        new_population.append(child)
        if fitness(child) == max_fitness: break
    return new_population          

def print_solution(queen_num, chrom_out):
    board = []

    for x in range(queen_num):
        board.append(["x"] * queen_num)
        
    for i in range(queen_num):
        board[queen_num-chrom_out[i]][i]="Q"
            

    for row in board:
        print (" ".join(row))
            

if __name__ == "__main__":
    queen_num = int(input("Enter Number of Queens: ")) 
    max_fitness = (queen_num*(queen_num-1))/2  # C(n,2)
    p_size = int(input("Enter Population Size: "))
    population = [create_random_chromosome(queen_num) for _ in range(p_size)]
    mutation_probability = float(input("Enter Mutation Probability: "))
    crossover_probability = 1-mutation_probability;

    start = time.time()

    generation = 1

    while max_fitness not in [fitness(chrom) for chrom in population]:
        print("=== Generation {} ===".format(generation))
        population = genetic_queen(population, fitness, mutation_probability)
        print("")
        print("Maximum Fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1

    chrom_out = []
    print("Solved in Generation {}!".format(generation-1))
    for chrom in population:
        if fitness(chrom) == max_fitness:
            print("");
            print("One of the solutions: ")
            chrom_out = chrom
            print_chromosome(chrom) 

    end = time.time()

    print("Solution Time: "+ str(end-start))

    print_solution(queen_num, chrom_out)        
            
           
            
    
