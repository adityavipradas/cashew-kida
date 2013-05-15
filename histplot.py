import pylab

BREADTH_FILENAME = "breadth.dat"

def loadthings(FILENAME):
    """
    Returns a list of all the bradths, lengths and thicknesses.
    """
    dimension = FILENAME.split('.')[0]
    print "Loading " + dimension + " from file ..."
    inFile = open(FILENAME, 'r')
    breadthList = []
    for line in inFile:
        breadthList.append(float(line.strip()))
    print " " , len(breadthList), dimension + " loaded."
    return breadthList

def labelPlot(thing):
    """
    Labels the current plot.
    """
    pylab.title('Distribution of '+ thing)
    pylab.xlabel('Various '+ thing)
    pylab.ylabel('Frequency')

def histPlot(dimensionList, string):
    """
    Plots histogram of corresponding things
    """
    pylab.figure()
    pylab.hist(dimensionList, bins = 12)
    labelPlot(string)
    
def calMean(X):
    """
    Returns mean of variables in list X.
    """
    return sum(X) / float(len(X))

def stdDev(X):
    """
    Returns Standard deviation of variable in list X.
    """
    mean = calMean(X)
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot / len(X))**0.5

def printMeanSd(dimension, string):
    """
    Prints Mean and Standard deviation for the word string
    """
    print "Mean for " + string + " is" ,calMean(dimension)
    print "Standard deviation " + string + "is", stdDev(dimension)

breadths = loadthings('breadth.dat')
lengths = loadthings('length.dat')
thicknesses = loadthings('thickness.dat')
lengthByBreadths = []
breadthByThickness = []
for i in range(len(breadths)):
    lengthByBreadths.append(lengths[i] / breadths[i])
    breadthByThickness.append(breadths[i] / thicknesses[i])
    
allList = [breadths, lengths, thicknesses, lengthByBreadths, breadthByThickness]
allString = ['breadth', 'length', 'thickness', 'length by breadth', 'breadths by thickness']
for i in range(len(allList)):
    histPlot(allList[i], allString[i])
    printMeanSd(allList[i], allString[i])

pylab.show()
