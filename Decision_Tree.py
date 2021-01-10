from csv import reader
from math import log2

def loadData(filename):
    with open(filename) as f:
        rd = reader(f)
        header = next(rd)
        X,y = [], []
        for row in rd:
            X.append(row[0:-1])
            y.append(row[-1])
    return X, y, header

def countByClass(y):
    dic = {}
    for i in y:
        if i not in dic:
            dic[i] = 0
        dic[i] += 1
    return dic

def entropy(dic):
    s = sum(dic.values())
    #print(s)
    return sum([(-dic[k]/s)*log2(dic[k]/s) for k in dic])

def countByAttr(X,y,col):
    dic = {}
    for row, c in zip(X,y):
        k = row[col]
        if k not in dic:
            dic[k] = {}
        if c not in dic[k]:
            dic[k][c] = 0
        dic[k][c] += 1
    return dic

def informationGain(X,y,col):
    dic = countByAttr(X,y,col)
    D = sum([sum(dic[k].values()) for k in dic])
    infoA_D = sum([entropy(dic[k]) * sum(dic[k].values())/D for k in dic])
    return infoA_D

def gain(X,y):
    dic=countByClass(y)
    ent = entropy(dic)
    n = len(X[0])
    arr = []
    for i in range(n):
        inf = informationGain(X,y,i)
        arr.append(ent - inf)
    return arr

def findPosMax(arr):
    p = 0
    for i in range(1, len(arr)):
        if arr[i] > arr[p]:
            p = i
    return p

def subtable(X, y, col):
    dic = {}
    for x, c in zip(X,y):
        k = x[col]
        if k not in dic:
            dic[k] = {'X': [], 'y': []}
        dic[k]['X'].append(x)
        dic[k]['y'].append(c)
    return dic

def buildTree(X,y,header):
    arr = gain(X,y)
    p = findPosMax(arr)
    node = header[p]
    tree = {node:{}}
    table = subtable(X,y,p)
    for k in table:
        classify = countByClass(table[k]['y'])
        if len(classify) == 1:
            tree[node][k] = next(iter(classify))
        else:
            tree[node][k] = buildTree(table[k]['X'], table[k]['y'],header)
    return tree

def predict(tree, x):
    for k in tree:
        child = tree[k][x[k]]
        if type(child) is dict:
            return predict(child,x)
        return child
        
#Train    
X, y, header = loadData('tennis.csv')
tree = buildTree(X,y,header)
print(tree)

#Test
x = {'Outlook': 'sunny',
     'Temperature': 'hot',
     'Humidity':'high',
     'Windy':'Strong'}
pred = predict(tree,x)
print('Predict:', pred)
