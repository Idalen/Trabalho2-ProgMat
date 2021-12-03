import numpy as np
from solver import Solver
import os
# t = m = linhas
# c = n = colunas
# a[i, j]:matrix = capacidade consumida do agente i ao realizar a tarefa j  
# cap[i]:list = capacidade do agente i
def fileRetriever(filePath):
    with open(filePath, "r") as f:
        lines = f.readlines()
    matrixLines = int(lines[0].split(" ")[0])
    getList = lambda lineStart, lineSize: [[int(item) for item in line.strip().split()] for line in lines[lineStart:lineStart+lineSize]]
    firstList = np.array(getList(1, matrixLines))
    secondList = np.array(getList(matrixLines+1, matrixLines))
    thirdList = np.array([int(i) for i in lines[-1].strip().split()])

    return firstList, secondList, thirdList

def guropiIteration(filePath,timeLimit=None):
    
    cost, a, cap = fileRetriever("./inputs/"+filePath)
    
    parametersPath = "./parameters"
    rulesPath = "./rules.txt"
    s = Solver(cost, a, cap, parametersPath, rulesPath, timeLimit)
    s.solve() 
    s.save(filePath.split(".")[0])






def main():
    timeLimit = 3 * 60
    filesList = [i for i in os.listdir("./inputs/") if ".in" in i]
    for i in range(len(filesList)):
        guropiIteration(filesList[i],timeLimit)


if __name__ == "__main__":
    main()