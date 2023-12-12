import random
import matplotlib.pyplot as plt
from alive_progress import alive_bar as ab

gene = '01' #alleles
population = 100 #maximum population size
generations = 100 #number of generations to study
l = 500 #length of gene

def generate_parent(length):
    genes = []
    while len(genes) < length:
        genes.append(random.choice(gene))
    return ''.join(genes)

def get_fitness(gene):
    absolute_fitness = 0
    for i in range(0,len(gene)):
        if gene[i] == '0':
            absolute_fitness += 1
    return absolute_fitness

def mutate(parent):
    prob = random.random()
    if prob > 0.75:
        mut = random.randint(0,1)
        pos = random.randint(0,len(parent)-1)
        if mut == 0:
            child = parent[:pos] + '0' + parent[pos+1:]
        else:
            child = parent[:pos] + '1' + parent[pos+1:]
    else:
        child = parent
    return child

def mate(parent1,parent2):
    child = ''
    for i in range(len(parent1)):
        prob = random.random()
        if prob > 0.5:
            child += parent1[i]
        else:
            child += parent2[i]
    return child

def selection(genome):
    new_genome = dict()
    avg_fitness = sum(genome.values())/len(genome)
    for i in genome:
        if genome[i] > avg_fitness:
            new_genome[i] = genome[i]
    return new_genome

def difference(parent1,parent2):
    diff = 0
    for i in range(len(parent1)):
        if parent1[i] != parent2[i]:
            diff += 1
    return diff
#Initializing population
genome = dict()

print('Initializing founder population...')
with ab(population) as barp:
    for _ in range(population):
        #the length of gene should be say l
        ind = generate_parent(l)
        genome[ind] = get_fitness(ind)
        barp()

popsizes = []
avg_fitness = []
gener = []
duplicates = []
diff_max = []
diff_min = []

initial_parent_sorted = sorted(genome.items(),key = lambda x:x[1],reverse = True)
initial_max = initial_parent_sorted[0][0]
initial_min = initial_parent_sorted[-1][0]

print('Starting evolution...')
with ab(generations) as bar:
    for i in range(generations):
        new_genome = selection(genome)
        filal = dict()
        wheel = []
        for j in new_genome:
            for k in range(new_genome[j]):
                wheel.append(j)
        duplicate_child = 0
        for _ in range(population):
            parent1 = random.choice(wheel)
            parent2 = random.choice(wheel)
            child = mate(parent1,parent2)
            child = mutate(child)
            if child in filal:
                duplicate_child += 1
            filal[child] = get_fitness(child)
        genome = filal
        max_fitness = max(genome.values())
        sorted_genome = sorted(genome.items(),key = lambda x:x[1],reverse = True)
        max_fit,min_fit = sorted_genome[0][0], sorted_genome[-1][0]
        diff_max.append(difference(max_fit,initial_max))
        diff_min.append(difference(min_fit,initial_min))
        fitnesses = []
        for fitnes in genome.values():
            fitnesses.append(fitnes/max_fitness)
        avg_fitness.append(sum(fitnesses)/len(fitnesses))
        popsizes.append(len(genome))
        gener.append(i)
        duplicates.append(duplicate_child)
        bar()

fig,axs = plt.subplots(2,2)

axs[0,0].plot(gener,avg_fitness,'r')
axs[0,0].set_title('Average Fitness vs Generation')

axs[0,1].plot(gener,popsizes,'b')
axs[0,1].set_title('Number of Individuals vs Generation')
axs[0,1].plot(gener,duplicates,'g')
axs[0,1].legend(['Unique Individuals','Same Individuals'])


axs[1,0].plot(gener,diff_max,'y',label = 'Max Fit')
axs[1,0].set_title('Difference between max fit gene vs Generation')
axs[1,1].plot(gener,diff_min,'k',label = 'Min Fit')
axs[1,1].set_title('Difference between min fit chromosome vs Generation')

fig.figure.suptitle(f'Initial Population Size: {population}, Number of Generations: {generations}, Chromosome Length: {l}')
plt.show()

print(f'Average Population size: {sum(popsizes)/len(popsizes)}')
print(f'Average Fitness: {sum(avg_fitness)/len(avg_fitness)}')
print(f'Average Duplicates: {sum(duplicates)/len(duplicates)}')
