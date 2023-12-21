from random import randint


INT_MAX = 2147483647
# Número de cidades no TSP
V = 15  

# No de inicio 
START = 0

# População Inicial 
POP_SIZE = 10



class individual:
	def __init__(self) -> None:
		self.gnome = ""
		self.fitness = 0

	def __lt__(self, other):
		return self.fitness < other.fitness

	def __gt__(self, other):
		return self.fitness > other.fitness


# Função que retorna um numero aleatorio 
def rand_num(start, end):
	return randint(start, end-1)



def repeat(s, ch):
	for i in range(len(s)):
		if s[i] == ch:
			return True

	return False


# Function to return a mutated GNOME
def mutatedGene(gnome):
	gnome = list(gnome)
	while True:
		r = rand_num(1, V)
		r1 = rand_num(1, V)
		if r1 != r:
			temp = gnome[r]
			gnome[r] = gnome[r1]
			gnome[r1] = temp
			break
	return ''.join(gnome)


def create_gnome():
    gnome = '0'
    max_attempts = V * 2  # Definindo um limite máximo de tentativas

    while len(gnome) < V + 1:
        if len(gnome) == V:
            gnome += gnome[0]
            break

        temp = rand_num(1, V)
        if not repeat(gnome, str(temp)):
            gnome += str(temp)
            print("Current gnome:", gnome)  # Adicione esta linha para depuração
        else:
            print("Duplicate found, retrying")

        # Verifica se atingiu o limite máximo de tentativas
        if len(gnome) == V + 1 and not gnome.endswith(gnome[0]):
            print("Não foi possível criar um gnome válido. Reiniciando...")
            gnome = '0'
            max_attempts -= 1

            if max_attempts == 0:
                print("Atingido o limite máximo de tentativas. Saindo do loop.")
                break

    return gnome


# retorna o valor fitness
def cal_fitness(gnome, distance_matrix):
    f = 0
    for i in range(len(gnome) - 1):
        city1 = int(gnome[i])
        city2 = int(gnome[i + 1])
        if distance_matrix[city1][city2] == INT_MAX:
            return INT_MAX
        f += distance_matrix[city1][city2]

    return f


# Function to return the updated value
# of the cooling element.
def cooldown(temp):
	return (90 * temp) / 100



# Função do caixeiro viajante
def TSPUtil(distance_matrix):
	# Numero da geração
	gen = 1
	
	gen_thres = 5

	population = []
	temp = individual()

	
	for i in range(POP_SIZE):
		temp.gnome = create_gnome()
		temp.fitness = cal_fitness(temp.gnome, distance_matrix)
		population.append(temp)
		
        

	print("\nPopulação Inicial: \nValor Fitness\n")
	for i in range(POP_SIZE):
		print(population[i].gnome, population[i].fitness)
	print()

	found = False
	temperature = 10000

	
	while temperature > 1000 and gen <= gen_thres:
		population.sort()
		print("\nCurrent temp: ", temperature)
		new_population = []

		for i in range(POP_SIZE):
			p1 = population[i]

			while True:
				new_g = mutatedGene(p1.gnome)
				new_gnome = individual()
				new_gnome.gnome = new_g
				new_gnome.fitness = cal_fitness(new_gnome.gnome, distance_matrix)

				if new_gnome.fitness <= population[i].fitness:
					new_population.append(new_gnome)
					break

				else:
					prob = pow(
						2.7,
						-1
						* (
							(float)(new_gnome.fitness - population[i].fitness)
							/ temperature
						),
					)
					if prob > 0.5:
						new_population.append(new_gnome)
						break

		temperature = cooldown(temperature)
		population = new_population
		print("Geração", gen)
		print("GNOME	 Valor Fitness")

		for i in range(POP_SIZE):
			print(population[i].gnome,   population[i].fitness)
		gen += 1
		
def get_distance_matrix():
    return [
        [0, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29, 74, 23, 72, 46],
        [29, 0, 55, 46, 42, 43, 43, 23, 23, 31, 41, 51, 11, 52, 21],
        [82, 55, 0, 68, 46, 55, 23, 43, 41, 29, 79, 21, 64, 31, 51],
        [46, 46, 68, 0, 82, 15, 72, 31, 62, 42, 21, 51, 51, 43, 64],
        [68, 42, 46, 82, 0, 74, 23, 52, 21, 46, 82, 58, 46, 65, 23],
        [52, 43, 55, 15, 74, 0, 61, 23, 55, 31, 33, 37, 51, 29, 59],
        [72, 43, 23, 72, 23, 61, 0, 42, 23, 31, 77, 37, 51, 46, 33],
        [42, 23, 43, 31, 52, 23, 42, 0, 33, 15, 37, 33, 33, 31, 37],
        [51, 23, 41, 62, 21, 55, 23, 33, 0, 29, 62, 46, 29, 51, 11],
        [55, 31, 29, 42, 46, 31, 31, 15, 29, 0, 51, 21, 41, 23, 37],
        [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, 0, 65, 42, 59, 61],
        [74, 51, 21, 51, 58, 37, 37, 33, 46, 21, 65, 0, 61, 11, 55],
        [23, 11, 64, 51, 46, 51, 51, 33, 29, 41, 42, 61, 0, 62, 23],
        [72, 52, 31, 43, 65, 29, 46, 31, 51, 23, 59, 11, 62, 0, 59],
        [46, 21, 51, 64, 23, 59, 33, 37, 11, 37, 61, 55, 23, 59, 0]
    ]


if __name__ == "__main__":
    mp = get_distance_matrix()
    TSPUtil(mp)
