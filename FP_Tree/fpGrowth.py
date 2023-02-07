import csv
import collections
import numpy
import operator


class FPTreeNode:
    def __init__(self, itemName, freqValue, parentNode):
        self.name = itemName
        self.value = freqValue
        self.parent = parentNode
        self.child = collections.OrderedDict()
    
    def display_tree_list(self):
        print(self.name, self.freq,end='')
        if len(self.child)>0:
            print(",[",end='')
        for c in self.child.values():
            print("[",end='')
            # For any children of the node, call the function recursively
            c.display_tree_list()
            if len(c.child)==0:
                print("]",end='')
        print("]",end='')
    



# Data Preprocessing(Cleaning)
def dataCleaning(userFile, userDelimiter, minSupport):
    dataSet = numpy.genfromtxt(userFile, dtype=str, delimiter=userDelimiter).tolist()
    
    # Clean data(empty string or infrequent data (i.e. < minSupport))
    freqItem = {} # To count the number of supports {itemName: num of support}
    for row in dataSet:
        for item in row:
            if item != '': # If is not an empty string
                if item not in freqItem:
                    freqItem[item] = 1 # Add to library
                else:
                    freqItem[item] += 1 # Increase the value by 1
    
    # Clean not satisfying items
    freqItem = {itemName:freqValue for itemName, freqValue in freqItem.items() if freqValue >= minSupport}
    # Clean those items in dataSet
    cleanedDataSet = []
    for row in dataSet:
        cleanedRow = []
        for item in row:
            if item in freqItem:
                dataSet[dataSet.index(row)].remove(item)
                cleanedRow.append(item)
        cleanedDataSet.append(cleanedRow)

    return cleanedDataSet, freqItem

def createFPTree(dataSet, freqItem):
    # Create root
    root = FPTreeNode('root',1,None)

    # Sort freqItem
    sortedFreqItem = sorted(freqItem.items(), key=operator.itemgetter(1),reverse=True)
    
    # Scan dataSet and add each transaction to FP Tree
    for row in dataSet:
        transaction = [] # should also be in descending order
        for item in sortedFreqItem:
            if item in row:
                transaction.append(item)
        # Update FPTree
        updateFPTREE(root,transaction)
    
    root.display_tree_list()

def updateFPTREE(initialNode, transaction):
    if transaction[0] in initialNode.child: # Already Exists
        initialNode.child[transaction[0]].freq += 1 # Increase the frequency by 1
    else:
        initialNode.child[transaction[0]] = FPTreeNode(transaction[0], 1, initialNode) # Create 1
    
    # Recursively call
    updateFPTREE(initialNode.child[transaction[0]], transaction[1::])






def runFPAlgorithm(userFile, userDelimiter, minSupport):
    dataSet, freqItem = dataCleaning(userFile, userDelimiter, minSupport)
    createFPTree(dataSet, freqItem)




# Driver Code
if __name__ == "__main__":
    inputFile = "./FP_Tree/ExampleDataSet/data1.csv"
    runFPAlgorithm(inputFile, ',', 2)
    
