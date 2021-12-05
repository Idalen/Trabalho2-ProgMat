import json
import os
import numpy as np
import matplotlib.pyplot as plt

colors = ['r','g','b','y']

def getName(nameVect,valueLine,dataParams,paramsDict,defaultName="Default"):
    idElem = -1
    #print(nameVect)
    #print(valueLine)
    #print(dataParams)
    #print(paramsDict)
    valueVec = [int(value) for value in valueLine[dataParams:]]
    maxValue = max(valueVec)
    if maxValue == -1:
        return defaultName
    maxIndex = valueVec.index(maxValue)
    return nameVect[maxIndex] + "=\n" + str(paramsDict[nameVect[maxIndex]][str(maxValue)])

def showAndSaveData(matrixPath,paramsDictPath,pos,dataParams=4):
    with open(paramsDictPath) as f:
        paramsDict = json.load(f)

    with open(matrixPath) as f:
        lines = f.readlines()
        matrixData = [line.replace("\n","").replace(" ","").split(",") for line in lines]

    matrixParams = matrixData[0][:dataParams]
    matrixHeading = matrixData[0][dataParams:]
    #print(matrixParams)
    #print(matrixHeading)

    barNames = [getName(matrixHeading,vec,dataParams,paramsDict) for vec in matrixData[1:]]
    #print(barNames)

    #y_pos = np.arange(len(barNames))

    y = (range(len(barNames)))
    y_pos = [2*i for i in y]

    heights = [dict([(matrixParams[elem],float(matrixData[vecPos][elem])) for elem in range(dataParams)]) for vecPos in range(1,len(matrixData))]
    #print(heights)



    fig, ax = plt.subplots()

    currentBars = [list(height.values())[pos] for height in heights]

    ax.bar(y_pos, currentBars,color=colors[pos])

    plt.xticks(y_pos, barNames)
    title = matrixPath.split("/")[-1].split(".")[0] + " - " + list(heights[0].keys())[pos]

    plt.title(title)
    ax.xaxis.set_tick_params(rotation=90,labelsize=8)

    plt.gcf().subplots_adjust(bottom=0.45)
    minY = min(currentBars,key=abs)
    maxY = max(currentBars,key=abs)
    difY = abs(maxY - minY)/10
    minY += difY if minY < 0 else -difY
    maxY += difY if minY >= 0 else -difY
    ax.set_ylim(ymin=minY,ymax=maxY)
    #fig.savefig("./figs/img_"+str(keyStrPairs[i])+".png")
    plt.savefig("./plots/"+title.replace(" ","")+".png")

files = [file for file in os.listdir("./results") if file.split(".")[-1] == "csv"]
for file in files:
  for pos in range(4):
    showAndSaveData("results/"+file,"paramsDict.json",pos)