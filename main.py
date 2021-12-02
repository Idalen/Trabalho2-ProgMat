import numpy as np
from solver import Solver
import os
# t = m = linhas
# c = n = colunas
# a[i, j]:matrix = capacidade consumida do agente i ao realizar a tarefa j  
# cap[i]:list = capacidade do agente i

def guropiIteration(filePath):
    
    #Mudar isso, só está mokado
    cost = np.random.rand(20, 20)

    a = np.random.rand(20, 20)

    cap = np.random.rand(20)
    timeLimit = 3 * 60
    
    parametersPath = "./parameters.json"
    s = Solver(cost, a, cap, parametersPath, timeLimit)
    s.solve() 
    s.save(filePath.split(".")[0])


def main():
    filesList = [i for i in os.listdir("./inputs/") if ".in" in i]
    for i in range(len(filesList)):
        guropiIteration(filesList[i])


if __name__ == "__main__":
    main()