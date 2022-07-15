import copy
from time import sleep
import warnings
import numpy as np
import math
import os
from random import randint, random
from Trabalho_1_Interface import Interface

warnings.filterwarnings('ignore')

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def create_map(file):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, file)
    arq = open(filename,'r')
    aux = arq.readlines()
    map = []
    for linha in aux:
        if list(linha)[-1] == '\n':
            map.append(list(linha[0:-1]))
        else:
            map.append(list(linha))
    return map

def get_points(mapa):
    pontos = []
    for i in range(32):
        pontos.append(0)
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            elem = mapa[i][j]
            if elem == '0':
                pontos[0] = [i,j]
            elif elem == '1':
                pontos[1] = [i,j]
            elif elem == '2':
                pontos[2] = [i,j]
            elif elem == '3':
                pontos[3] = [i,j]
            elif elem == '4':
                pontos[4] = [i,j]
            elif elem == '5':
                pontos[5] = [i,j]
            elif elem == '6':
                pontos[6] = [i,j]
            elif elem == '7':
                pontos[7] = [i,j]
            elif elem == '8':
                pontos[8] = [i,j]
            elif elem == '9':
                pontos[9] = [i,j]
            elif elem == 'B':
                pontos[10] = [i,j]
            elif elem == 'C':
                pontos[11] = [i,j]
            elif elem == 'D':
                pontos[12] = [i,j]
            elif elem == 'E':
                pontos[13] = [i,j]
            elif elem == 'G':
                pontos[14] = [i,j]
            elif elem == 'H':
                pontos[15] = [i,j]
            elif elem == 'I':
                pontos[16] = [i,j]
            elif elem == 'J':
                pontos[17] = [i,j]
            elif elem == 'K':
                pontos[18] = [i,j]
            elif elem == 'L':
                pontos[19] = [i,j]
            elif elem == 'N':
                pontos[20] = [i,j]
            elif elem == 'O':
                pontos[21] = [i,j]
            elif elem == 'P':
                pontos[22] = [i,j]
            elif elem == 'Q':
                pontos[23] = [i,j]
            elif elem == 'S':
                pontos[24] = [i,j]
            elif elem == 'T':
                pontos[25] = [i,j]
            elif elem == 'U':
                pontos[26] = [i,j]
            elif elem == 'V':
                pontos[27] = [i,j]
            elif elem == 'W':
                pontos[28] = [i,j]
            elif elem == 'X':
                pontos[29] = [i,j]
            elif elem == 'Y':
                pontos[30] = [i,j]
            elif elem == 'Z':
                pontos[31] = [i,j]
    return pontos

def get_neighbors(map, point):
    neighbors = []
    if point[0] > 0:
        neighbors.append([point[0]-1,point[1]])
    if point[1] < len(map[0])-1:
        neighbors.append([point[0],point[1]+1])
    if point[0] < len(map)-1:
        neighbors.append([point[0]+1,point[1]])
    if point[1] > 0:
        neighbors.append([point[0],point[1]-1])
    return neighbors

def get_distance(ponto1, ponto2):
    vert = 0
    hori = 0
    if ponto1[0] > ponto2[0]:
        vert = ponto1[0] - ponto2[0]
    else:
        vert = ponto2[0] - ponto1[0]
    if ponto1[1] > ponto2[1]:
        hori = ponto1[1] - ponto2[1]
    else:
        hori = ponto2[1] - ponto1[1]
    return math.sqrt(vert**2 + hori**2)

def find_path_step(map, points, step, interface, custos):
    start = points[step]
    end = points[step+1]
    margem = [start] # Array para guardar pontos ja visitados e que ainda tenham vizinhos nao visitados
    caminho = [[0 for col in range(len(map[0]))] for row in range(len(map))] # Matriz para guardar o vizinho utilizado para chegar no ponto
    caminho[start[0]][start[1]] = ['s', 0]
    path = [end] # Melhor caminho da origem ate o destino
    while end not in margem:
        interface.update(caminho,path, step, custos)
        min = 100000
        current = [-1,-1] # Ponto que sera utilizado para alcancar o vizinho
        next_step = [-1,-1] # Vizinho
        remove = [] # Lista de pontos para remover da margem (nao possuem mais vizinhos nao visitados)
        for ponto in margem:
            neighbors = get_neighbors(map, ponto)
            if neighbors == []:
                remove.append(ponto)
            else:
                exist = None # Verificar se possui vizinho valido
                for vizinho in neighbors:
                    if caminho[vizinho[0]][vizinho[1]] == 0: # Ponto ainda nao visitado
                        exist = 1
                        # Calcula o custo estimado do passo para pegar o melhor vizinho
                        if map[vizinho[0]][vizinho[1]] == '.':
                            value = caminho[ponto[0]][ponto[1]][1] + 1 + get_distance(vizinho, end)
                            if value < min:
                                min = value
                                next_step = vizinho
                                current = ponto
                        elif map[vizinho[0]][vizinho[1]] == 'R':
                            value = caminho[ponto[0]][ponto[1]][1] + 5 + get_distance(vizinho, end)
                            if value < min:
                                min = value
                                next_step = vizinho
                                current = ponto
                        elif map[vizinho[0]][vizinho[1]] == 'F':
                            value = caminho[ponto[0]][ponto[1]][1] + 10 + get_distance(vizinho, end)
                            if value < min:
                                min = value
                                next_step = vizinho
                                current = ponto
                        elif map[vizinho[0]][vizinho[1]] == 'A':
                            value = caminho[ponto[0]][ponto[1]][1] + 15 + get_distance(vizinho, end)
                            if value < min:
                                min = value
                                next_step = vizinho
                                current = ponto
                        elif map[vizinho[0]][vizinho[1]] == 'M':
                            value = caminho[ponto[0]][ponto[1]][1] + 200 + get_distance(vizinho, end)
                            if value < min:
                                min = value
                                next_step = vizinho
                                current = ponto
                        else: #destino
                            value = caminho[ponto[0]][ponto[1]][1] + get_distance(vizinho, end)
                            if value < min:
                                min = value
                                next_step = vizinho
                                current = ponto
                if exist == None: # Ponto nao possui vizinhos validos
                    remove.append(ponto)
        for ponto in remove: # Remove pontos da margem
            margem.remove(ponto)
        # min eh a soma do custo total para alcancar o ponto + peso do vizinho + distancia euclidiana do vizinho ate o destino
        value = min - get_distance(next_step, end) # Salva o custo total para alcancar o vizinho (sem a distancia euclidiana)
        margem.append(next_step) # adiciona o vizinho na margem
        """
        Salva um "ponteiro" para o pai do vizinho
        [linha, coluna]
        [0, 1] - > Veio da direita
        [1, 0] - > Veio de baixo
        [0, -1] - > Veio da esquerda
        [-1, 0] - > Veio de cima
        Para achar o pai basta somar o array com a coordenada do poto
        """
        caminho[next_step[0]][next_step[1]] = [[current[0]-next_step[0],current[1]-next_step[1]],value] # Salva o pai e o custo para alcancar o ponto
    while start not in path: # Reconstitui o caminho tomado para alcancar o destino
        interface.update(caminho,path,step,custos)
        ant = caminho[path[0][0]][path[0][1]][0] # "Ponteiro" para o pai do primeiro ponto presente no path
        path.insert(0,[path[0][0]+ant[0],path[0][1]+ant[1]]) # Insere no inicio o pai
    interface.update([[0 for col in range(len(map[0]))] for row in range(len(map))],path,step,custos)
    custo = caminho[end[0]][end[1]][1] # Custo total para atingir o destino
    return path, custo

def gera_array_aleatorio(agilidades):
    array = [[0 for col in range(31)] for row in range(7)]
    for i in range(7):
        aux = []
        while len(aux) < 8:
            indice = randint(0,30)
            if indice not in aux:
                array[i][indice] = 1
                aux.append(indice)
    # O pior personagem vai ficar vivo no final
    min = agilidades[0]
    min_index = 0
    for i, val in enumerate(agilidades):
        if val < min:
            min = val
            min_index = i
    i = 0
    while True:
        if array[min_index][i] == 1:
            break
        i += 1
    array[min_index][i] = 0
    return array

def update_array(array, max, atual):
    aux = copy.deepcopy(array)
    n = math.ceil(atual/(max/32))
    num = randint(1,n)
    for i in range(num):
        i = randint(0,6)
        j = randint(0,30)
        if aux[i][j] == 0:
            aux[i][j] = 1
            k = randint(0,30)
            while k == j or aux[i][k] == 0:
                k = randint(0,30)
            aux[i][k] = 0
        else:
            aux[i][j] = 0
            k = randint(0,30)
            while k == j or aux[i][k] == 1:
                k = randint(0,30)
            aux[i][k] = 1
    return aux

def objective(array, etapas, agilidades):
    total = 0
    for j in range(31):
        soma = 0
        for i in range(7):
            soma += array[i][j] * agilidades[i]
        if soma == 0:
            soma = 0.000001
        total += etapas[j]/soma
    return total


def Simulated_annealing(etapas, agilidades, temp, interface):
    ext = 5 # Quantidade de Simulated Annealing a ser realizado
    intern = 100000 # Numero de passos em um Simulated Annealing
    for p in range(ext):
        best = gera_array_aleatorio(agilidades)
        best_val = objective(best,etapas,agilidades)
        if p == 0:
            melhor = best_val
            participou = copy.deepcopy(best)
        curr = copy.deepcopy(best)
        curr_val = best_val
        scores = []
        scores.append(best_val)
        for i in range(intern):
            printProgressBar(p*intern+i+1, ext*intern, prefix = 'Progress:', suffix = 'Complete', length = 50)
            t = temp / ((i/100)+1)
            candidate = update_array(curr, temp, t)
            candidate_val = objective(candidate, etapas, agilidades)
            if candidate_val < best_val:
                best = candidate
                best_val = candidate_val
                scores.append(best_val)
            diff = candidate_val - curr_val
            metropolis = np.exp(-diff / t)
            if diff < 0 or random() < metropolis:
                curr, curr_val = candidate, candidate_val
        if best_val < melhor:
            melhor = best_val
            participou = copy.deepcopy(best)  
    return participou, melhor
    


etapas = []
for i in range(31):
    etapas.append((i+1)*10)

agilidades = [1.8,1.6,1.6,1.6,1.4,0.9,0.7]

interface = Interface(300*5,82*7)
map = create_map('mapa.txt')
interface.add_map(map)
points = get_points(map)
path = []
custos = []
for i in range(31):
    caminho, custo = find_path_step(map,points,i,interface,custos)
    path.append(caminho)
    custos.append(custo)
interface.finish(path)
best, best_val = Simulated_annealing(etapas,agilidades,800,interface)
interface.update_finish(best, custos, best_val)

i=0
while True:
    i+=1