from dwave_qbsolv import QBSolv
import numpy as np
from dwave.system import LeapHybridSampler
from dwave.system.composites import EmbeddingComposite
from dwave.system.samplers import DWaveSampler
from dwave.system.samplers import DWaveCliqueSampler
#from dwave.system.samplers import SimulatedAnnealingSampler
import neal
import dimod
from tabu import TabuSampler
import dwave.inspector

#sampler = LeapHybridSampler()
#sampler =EmbeddingComposite(DWaveSampler())
#sampler =dimod.RandomSampler()
#sampler =DWaveCliqueSampler()

# this function solves a given QUBO-Matrix Q with Qbsolv
def solve_with_qbsolv(Q, n, timeout=1):
    response = QBSolv().sample_qubo(Q, num_repeats=100, timeout=timeout)
    #response = TabuSampler().sample_qubo(Q, num_repeats=100, timeout=timeout)
    #response = neal.SimulatedAnnealingSampler().sample_qubo(Q, num_repeats=100, timeout=timeout)
    solution = [response.samples()[0][i] for i in range(n)]
    return solution

def solve_with_Tabu(Q, n, timeout=1):
  
    response = TabuSampler().sample_qubo(Q, num_repeats=100, timeout=timeout)
    
    solution = [response.samples()[0][i] for i in range(n)]
    return solution
    
def solve_with_SA(Q, n, timeout=1):

    response = neal.SimulatedAnnealingSampler().sample_qubo(Q, num_repeats=100, timeout=timeout)
    solution = [response.samples()[0][i] for i in range(n)]
    return solution
    
    
    

def solve_with_Leap(Q, n, leap_inf,num,idx,num_repeats=1): 
    S=sampler.sample_qubo(Q)
    leap_inf[num][idx].append(S.info)
    answer = S.lowest().samples()[0]
    print("   Answer received...")
    solution = [answer[i] for i in range(n)]
    return solution
def solve_with_dwave(Q, n, Dwave_inf,num,idx): 
    global bqm
    
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    #Dwave_inf[num][idx].append(bqm)
    S=sampler.sample(bqm, num_reads=100)
    Dwave_inf[num][idx].append(S.info)
    answer = S.lowest().samples()[0]
    print("   Answer received...")
    # print(len(len(bqm.linear)))
    # print(len(len(bqm.quadratic)))
    solution = [answer[i] for i in range(n)]
    return solution
    
    

def transform(naeimeh_graph):
    edges = {}
    for key in naeimeh_graph.keys():
        i, j = key.split(",")
        i, j = int(i)-1, int(j)-1
        edges[(i,j)] = naeimeh_graph[key]
    return edges



# this function calculates the value of a solution for a given QUBO-Matrix Q
def getValue(Q, solution):
    ones = [i for i in range(len(solution)) if solution[i] == 1]
    value = 0
    for x in ones:
        for y in ones:
            if (x,y) in Q.keys():
                value += Q[(x,y)]
    return value



# this function prints the first n row/columns of a QUBO-Matrix Q
def printQUBO(Q, n):
    for row in range(n):
        for column in range(n):
            if row > column:
                print("        ", end = '')
                continue
            printing = ""
            if (row,column) in Q.keys() and Q[(row,column)] != 0:
                printing = str(float(Q[(row,column)]))
            printing += "_______"
            printing = printing[:7]
            printing += " "
            print(printing, end = '')
        print("")



def generate_problem(n, mean=0.5):
    edges = {}
    for i in range(n):
        for j in range(n):
            if i < j:
                edges[(i,j)] = np.random.sample() - mean
    return edges



def add(Q, i, j, v):
    if (i,j) not in Q.keys():
        Q[(i,j)] = v
    else:
        Q[(i,j)] += v



def value(c, edges):
    v = 0
    for i in c:
        for j in c:
            if i < j:
                v += edges[(i,j)]
    return v
