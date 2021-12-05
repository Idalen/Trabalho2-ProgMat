import numpy as np # Imports numpy
from solver import Solver # Imports solver class
import os # Imports OS

## 
# Retrieves the data from a file as three lists
# 
# string filePath
##
def fileRetriever(filePath):
    # Opens the file
    with open(filePath, "r") as f:
        lines = f.readlines()
    # Reads the amount of lines of the matrix
    matrixLines = int(lines[0].split(" ")[0])
    # Reads the data into a list
    getList = lambda lineStart, lineSize: [[int(item) for item in line.strip().split()] for line in lines[lineStart:lineStart+lineSize]]
    # Separates into three lists
    firstList = np.array(getList(1, matrixLines))
    secondList = np.array(getList(matrixLines+1, matrixLines))
    thirdList = np.array([int(i) for i in lines[-1].strip().split()])

    return firstList, secondList, thirdList

##
# Runs the guropi iteration on the given file
#
# t = m = linhas
# c = n = colunas
# a[i, j]:matrix = capacidade consumida do agente i ao realizar a tarefa j  
# cap[i]:list = capacidade do agente i
#
# string filePath
# int timeLimit
##
def guropiIteration(filePath,timeLimit=None):
    # Gets the data from the given input file
    costPerWorkerPerTask, capacityCostPerWorkerPerTask, availableCapacityPerWorker = fileRetriever("./inputs/"+filePath)
    # Defines the parameters path
    parametersPath = "./parameters"
    # Initializes the gurobi solver
    s = Solver(costPerWorkerPerTask, capacityCostPerWorkerPerTask, availableCapacityPerWorker, parametersPath, timeLimit)
    # Solves the problem
    s.solve() 
    # Saves the resolution on a new .csv file
    s.save(filePath.split(".")[0])


# Main method
def main():
    # Defines the time limit as 3 minutes
    timeLimit = 3 * 60
    # Reads the input files
    filesList = [i for i in os.listdir("./inputs/") if ".in" in i]
    # Runs the gurobi iteration on each input file
    for i in range(len(filesList)):
        guropiIteration(filesList[i],timeLimit)

# If current file is main file, runs the main method 
if __name__ == "__main__":
    main()