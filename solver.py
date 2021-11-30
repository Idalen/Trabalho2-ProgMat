from gurobipy import *
import numpy as np
from dataclasses import dataclass 
import json
import numpy as np
import pandas as pd

@dataclass
class results:
    node_count: int
    optimal_value: float
    bound: float
    gap: float        

class Solver:

    parameters = {}
    parametersCombinations = []

    def __init__(self, cost, a, capacity, parametersPath):
        self.cost = cost
        self.a = a
        self.cap = capacity
        self._setParameters(parametersPath)
        
    def _setParameters(self,parametersPath):
        with open(parametersPath) as f:
            self.parameters = json.load(f)
        self._setParametersCombinations()

    def _setParametersCombinations(self):
        paramsList = list(self.parameters.keys())
        paramsLen = len(paramsList)
        self._execRecursive(paramsList, paramsLen,0,"")

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

    def _execAllGurobis(self):
        gurobiDict = {
            "nodeCount": [],
            "objVal": [],
            "objBound": [],
            "MIPGap": []
        }

        for param in self.parameters:
            gurobiDict[param] = []

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
        self.model = Model("Generalized_Assigment")
        self._setModelParameters(index)
        numT,numC = np.shape(self.cost)
          
        x = []
        for t in range(numT):
            x.append([])
            for c in range(numC):
                x[t].append(self.model.addVar(vtype=GRB.BINARY,name="x %d %d"% (t, c)))

        self.model.update()

        constraint = []

        for c in range(numC):
            constraint.append(
                self.model.addConstr(quicksum(x[t][c] for t in range(numT)) == 1 ,'constraint%d' % c)
            )
        
        for t in range(numT):
            constraint.append(
                self.model.addConstr(quicksum(x[t][c]*self.a[t][c] for c in range(numC)) <= self.cap[t] ,'constraint%d' % t)
            )
            
        self.model.setObjective(quicksum(quicksum([x[t][c]*self.cost[t][c] for c in range(numC)]) for t in range(numT)), GRB.MAXIMIZE)
        
        self.model.optimize()
        result = {
            "nodeCount": int(self.model.nodeCount),
            "objVal": self.model.objVal,
            "objBound": self.model.objBound,
            "MIPGap": self.model.MIPGap
        }
        return result
    
    def solve(self):
        gurobiData = self._execAllGurobis()
        self.df = pd.DataFrame(gurobiData, columns=gurobiData.keys())
        
        
    def save(self, outputName):
        self.df.to_csv("./results/result_"+outputName+".csv", index=False)
