import random, math

#inicjalizacja generatora liczb losowych
random.seed(a=None)

class Sack:
    def __init__(self, geneAmt, sackSize):
        #inicjalizacja osobnika
        self.geneVals = {}
        self.size = sackSize
        self.fitness = 0
        #ustawienie genów na losowe wartości
        for i in range(geneAmt):
            self.geneVals.update({i : random.random()})
    
    def mutate(self):
        # szansa na mutację losowego genu do losowej wartości
        for x in range(len(self.geneVals)):
            if random.random() < 0.001+0.005*bestCount:
                self.geneVals[x] = random.random()

    def calcFitness(self, geneWorth, geneSize):
        #liczenie przystosowania
        if self.fitness == 0:
            self.fitness = 0
            self.curSize = 0
            #sortowanie genów według wartości
            self.sortedVals = sorted(self.geneVals.items(), key=lambda x: x[1])
            for x in self.sortedVals:
                #sumowanie wartości elementów do wypelnienia plecaka
                i = int(x[0])
                self.curSize += geneSize[i]
                if self.curSize < self.size:
                    self.fitness += geneWorth[i]
                else:
                    return True

class Population:
    def __init__(self, size, geneAmt, sackSize):
        #inicjalizacja populacji z określoną liczbą genów
        self.specimens = []
        self.size = size
        for i in range(size):
            self.specimens.append(Sack(geneAmt,sackSize))

    def popFitness(self,geneWorth,geneSize):
        #liczenie przystosowania i sortowanie
        for spec in self.specimens:
            spec.calcFitness(geneWorth,geneSize)
        self.specimens.sort(key=lambda x: x.fitness, reverse=True)
        return self.specimens[0].fitness
    
    def crossover(self):
        #krzyżowanie top 50% populacji
        children = []
        for x in range(0, int(self.size/2), 2):
            pair = mateSpecimens(self.specimens[math.floor(x*random.random())], self.specimens[math.floor(x*random.random())])
            children.append(pair[0])
            children.append(pair[1])
            #usunięcie 2 najgorszych osobników
            del self.specimens[-3:-1]
        for child in children:
            #wstawienie dzieci do populacji
            self.specimens.append(child)
        
def LoadData(fileName):
    #ladowanie danych z pliku
    f = open(fileName,"r")
    fLines = f.read().split('\n')
    gSackSize = float(fLines[0]);
    gWorth = []
    gSize = []
    for x in range(1,len(fLines)):
        tmp = fLines[x].split(' ')
        if len(tmp) == 1:
            tmp = fLines[x].split('\t')
        gSize.append(float(tmp[1]))
        gWorth.append(float(tmp[2]))
        
    return [gSackSize,gWorth,gSize]

def mateSpecimens(spec1,spec2):
    #wyznaczenie miejsca krzyżowania
    crossPoint = random.randint(0, len(spec1.geneVals))
    #inicjalizacja dzieci
    child1 = Sack(len(spec1.geneVals), spec1.size)
    child2 = Sack(len(spec1.geneVals), spec1.size)
    child1.geneVals={}
    child2.geneVals={}
    #wstawienie genów rodziców do dzieci
    for x in range(len(spec1.geneVals)):
        if x < crossPoint:
            child1.geneVals.update({x : spec1.geneVals[x]})
            child2.geneVals.update({x : spec2.geneVals[x]})
        else:
            child1.geneVals.update({x : spec2.geneVals[x]})
            child2.geneVals.update({x : spec1.geneVals[x]})
    #mutacja dzieci
    child1.mutate()
    child2.mutate()
    return [child1,child2]
    

#ladowanie danych
params = LoadData("knapsack data large.txt")

gWorth = params[1]
gSize = params[2]
gSackSize = params[0]
gPopulSize = 1000
gGenomeSize = len(gWorth)
genCount = 0
#stworzenie populacji
popul = Population(gPopulSize,gGenomeSize,gSackSize)
#inicjalizacja przystosowania
bestfit = popul.popFitness(gWorth,gSize)
newfit = 0
print(bestfit)
#licznik stabilizacji
global bestCount
bestCount = 0
#tworzenie kolejnych generacji póki wartość nie ustablizuje się na 150 generacji
while bestCount < 100:
    genCount += 1
    popul.crossover()
    newfit = popul.popFitness(gWorth,gSize)
    if newfit==bestfit:
        bestCount += 1
    else:
        bestfit = newfit
        print(bestfit)
        bestCount = 0
print(genCount)





