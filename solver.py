from gurobipy import * # Imports gurobipy
import numpy as np # Imports numpy
from dataclasses import dataclass # Imports dataclass
import json # Imports json reader
import numpy as np # Imports numpy
import pandas as pd # Imports pandas
import os # Imports OS

class Solver:

    parameters = {}
    parametersCombinations = []

    # Class constructor
    def __init__(self, costPerWorkerPerTask, capacityCostPerWorkerPerTask, availableCapacityPerWorker, parametersPath, timeLimit):
        self.timeLimit = timeLimit
        self.costPerWorkerPerTask = costPerWorkerPerTask
        self.capacityCostPerWorkerPerTask = capacityCostPerWorkerPerTask
        self.availableCapacityPerWorker = availableCapacityPerWorker
        # Sets the parameters from the given parameters path
        self._setParameters(parametersPath)
        
    # Opens each parameters file and calls setParametersCombinations for them
    def _setParameters(self,parametersPath):
        paramsFiles = [f for f in os.listdir(parametersPath) if f.split(".")[-1] == "json"]
        for paramsFile in paramsFiles:
            with open(parametersPath+"/"+paramsFile) as f:
                self.parameters = json.load(f)
            self._setParametersCombinations()
        print(self.parametersCombinations)

    # Calls the execRecursive and initializes all the possible combinations for the current parameters file
    def _setParametersCombinations(self):
        paramsList = list(self.parameters.keys())
        paramsLen = len(paramsList)
        self._execRecursive(paramsList, paramsLen,0,"")

    # Generates all the possible combinations for the current parameters file
    def _execRecursive(self,paramsList, paramsLen, pos, text):
        if pos == paramsLen:
            text = text[:-1]
            splittedText = text.split("\n")
            values = dict([(paramsList[i],splittedText[i].split(":")[1].strip()) for i in range(len(splittedText))])
            self.parametersCombinations.append({"description":text,"values":values})
            return

        for val in self.parameters[paramsList[pos]].values():
            self._execRecursive(paramsList, paramsLen,pos+1,text+paramsList[pos]+":"+str(val)+"\n")

    def _setModelParameters(self,index):
        for param in self.parametersCombinations[index]["values"].items():
            self.model.setParam(param[0], int(param[1]))

    ##
    # Runs the gurobi optimization for each parameters combination
    ## 
    def _execAllGurobis(self):
        # Initializes the gurobi output dictionary
        gurobiDict = {
            "nodeCount": [],
            "objVal": [],
            "objBound": [],
            "MIPGap": []
        }

        # Adds the given parameters to the dictionary
        for param in self.parameters:
            gurobiDict[param] = []

        # Executes gurobi for each parameter combination (generated in the constructor) 
        gurobiData = []
        for i in range(len(self.parametersCombinations)):
            gurobiData.append(self._gurobi(i))
            for params in self.parameters:
                gurobiDict[params].append(self.parametersCombinations[i]["values"][params])

        for elem in gurobiData:
            for item in elem.items():
                gurobiDict[item[0]].append(item[1])
        
        return gurobiDict

    def _gurobi(self,index):

        # Initializes model
        self.model = Model("Generalized_Assigment")
        # Sets a time limit
        if self.timeLimit:
            self.model.setParam("TimeLimit", self.timeLimit)
        # Defines the current parameters combination
        self._setModelParameters(index)
        # Gets the shape of the input matrix
        numT,numC = np.shape(self.costPerWorkerPerTask)
        
        # Initializes the output matrix
        x = []
        for t in range(numT):
            x.append([])
            for c in range(numC):
                x[t].append(self.model.addVar(vtype=GRB.BINARY,name="x %d %d"% (t, c)))

        # Updates gurobi model
        self.model.update()

        # Initializes the constraints array
        constraint = []

        # Adds the constraint that each task can only be executed by one worker
        for c in range(numC):
            constraint.append(
                self.model.addConstr(quicksum(x[t][c] for t in range(numT)) == 1 ,'constraint%d' % c)
            )
        
        # Adds the constraint that each worker can only execute the amount of worker that he can handle
        for t in range(numT):
            constraint.append(
                self.model.addConstr(quicksum(x[t][c]*self.capacityCostPerWorkerPerTask[t][c] for c in range(numC)) <= self.availableCapacityPerWorker[t] ,'constraint%d' % t)
            )

        # Defines the objective of the optimization, that is maximize the cost sum
        self.model.setObjective(quicksum(quicksum([x[t][c]*self.costPerWorkerPerTask[t][c] for c in range(numC)]) for t in range(numT)), GRB.MAXIMIZE)
        
        # Runs the optimization
        self.model.optimize()

        # Sets the result into the output dictionary
        result = {
            "nodeCount": int(self.model.nodeCount),
            "objVal": self.model.objVal,
            "objBound": self.model.objBound,
            "MIPGap": self.model.MIPGap
        }

        return result
    
    # Solves the given problem
    def solve(self):
        gurobiData = self._execAllGurobis()
        self.df = pd.DataFrame(gurobiData, columns=gurobiData.keys())
        
        
    def save(self, outputName):
        self.df.to_csv("./results/result_"+outputName+".csv", index=False)
