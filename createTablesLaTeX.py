import os



dictParams = {
    "0":{
        "0": "1"
    },
    "1":{
        "0": "2", 
        "1": "3", 
        "2": "4", 
        "3": "5"
    },
    "2":{
        "0": "6", 
        "1": "7" ,
        "2": "8" 
    },
    "4":{
        "2": "9" 
    },
    "5":{
        "2": "10" 
    }
}



def getConfNo(line,defaultName="0",dataParams=4):
    valueVec = [int(value) for value in line[dataParams:]]
    maxValue = max(valueVec)
    if maxValue == -1:
        return defaultName
    maxIndex = valueVec.index(maxValue)
    return dictParams[str(maxIndex)][str(maxValue)]





def createTableLaTeX(filePath):
    fullList =[""]*11
    print(fullList)
    with open(filePath, 'r') as f:
        lines = f.readlines()
    matrix = [line.replace(" ","").replace("\n","").split(",") for line in lines]

    lineEnding = "\\\\\\hline\n"
    text = "\\begin{center}\n\\begin{tabular}{|c|c|c|c|c|}\n\\hline\n$nodeCount$ & $objVal$ & $objBound$ & $MIPGap$ & $conf$"+lineEnding
    for line in matrix[1:]:
        print(line)
        auxText = "${}$ & ${}$ & ${}$ & ${}$ & $".format(line[0], line[1], line[2], line[3])
        lineNo = getConfNo(line)
        print(lineNo)
        auxText += lineNo + "$ " + lineEnding
        fullList[int(lineNo)] = auxText
    for i in range(11):
        text += fullList[i]
    text += "\\end{tabular}\n\\end{center}"
    
    with open("tablesLaTeX/" + filePath.split("/")[-1].split(".")[0] + ".tex", 'w') as f:
        f.write(text)


files = [file for file in os.listdir("./results") if file.split(".")[-1] == "csv"]
for file in files:
    print(file)
    createTableLaTeX("./results/"+file)