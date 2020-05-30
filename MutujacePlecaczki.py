import random, math, matplotlib.pyplot as plt

class Sack:
    def __init__(self, geneAmt, sackSize):
        #inicjalizacja osobnika
        self.geneVals = []
        self.size = sackSize
        self.fitness = 0
        #ustawienie genów na losowe wartości
        for i in range(geneAmt):
            self.geneVals.append(1 if random.random()>0.5 else 0)

    def mutate(self):
        # szansa na mutację losowego genu
        for x in range(gGenomeSize):
            #1 do 6% na od 0 do 20 generacji bez poprawy
            if random.random() < 0.01+0.001*(bestCount if bestCount<50 else 50):
                self.geneVals[x] = 0 if self.geneVals[x]==1 else 1

    def calcFitness(self, geneWorth, geneSize):
        #liczenie przystosowania
        if self.fitness == 0:
            self.fitness = 0
            self.curSize = 0
            for i in range(gGenomeSize):
                #sumowanie wartości elementów do wypelnienia plecaka
                if self.geneVals[i]:
                    self.curSize += geneSize[i]
                    self.fitness += geneWorth[i]
            if self.curSize > self.size:
                self.fitness *= 0.3


class Population:
    def __init__(self, size, geneAmt, sackSize):
        #inicjalizacja populacji z określoną liczbą genów
        self.specimens = []
        self.size = size
        for i in range(size):
            self.specimens.append(Sack(geneAmt,sackSize))

    def popFitness(self,geneWorth,geneSize):
        #liczenie przystosowania i sortowanie
        global gAvgFit
        gAvgFit = 0;
        for spec in self.specimens:
            spec.calcFitness(geneWorth,geneSize)
            gAvgFit += spec.fitness
        gAvgFit = gAvgFit/gPopulSize
        self.specimens.sort(key=lambda x: x.fitness, reverse=True)
        return self.specimens[0].fitness

    def crossover(self):
        #krzyżowanie top 50% populacji
        children = []
        for x in range(0, int(self.size/2), 2):
            pair = mateSpecimens(self.specimens[math.floor(x*random.random())],
                self.specimens[math.floor(x*random.random())]
                )
            #pair = mateSpecimens(self.specimens[x],self.specimens[x+1])
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
        #upewnienie sie czy dane oddzielone spacja czy tabem
        tmp = fLines[x].split(' ')
        if len(tmp) == 1:
            tmp = fLines[x].split('\t')
        gSize.append(float(tmp[1]))
        gWorth.append(float(tmp[2]))

    return [gSackSize,gWorth,gSize]

def mateSpecimens(spec1,spec2):
    #wyznaczenie miejsca krzyżowania
    crossPoint = gGenomeSize/2+random.randint(-gGenomeSize/4,gGenomeSize)

    #inicjalizacja dzieci
    child1 = Sack(gGenomeSize, spec1.size)
    child2 = Sack(gGenomeSize, spec1.size)
    child1.geneVals=[]
    child2.geneVals=[]

    #wstawienie genów rodziców do dzieci
    for x in range(gGenomeSize):
        if x < crossPoint:
            child1.geneVals.append(spec1.geneVals[x])
            child2.geneVals.append(spec2.geneVals[x])
        else:
            child1.geneVals.append(spec2.geneVals[x])
            child2.geneVals.append(spec1.geneVals[x])
    #mutacja potomków
    child1.mutate()
    child2.mutate()
    return [child1,child2]


#inicjalizacja generatora liczb losowych
random.seed(a=None)
global bestCount
global gAvgFit
global gPopulSize
global gGenomeSize
gAvgFit = 0

#ladowanie danych
params = LoadData("knapsack data large.txt")
gWorth = params[1]
gSize = params[2]
gSackSize = params[0]
#rozmiar populacji
gPopulSize = 1500
gGenomeSize = len(gWorth)

#licznik generacji
genCount = 0

#licznik stabilizacji
bestCount = 0

#stworzenie populacji
popul = Population(gPopulSize,gGenomeSize,gSackSize)

#inicjalizacja przystosowania
gBestFit = popul.popFitness(gWorth,gSize)
newFit = gBestFit

#inicjalizacja wartości do wykresu
plotx = [genCount]
ploty = []
ploty.append([gBestFit])
ploty.append([gAvgFit])

#tworzenie kolejnych generacji póki wartość nie ustablizuje się na 50 generacji
while bestCount < 100:
    genCount += 1
    popul.crossover()
    newFit = popul.popFitness(gWorth,gSize)
    if newFit <= gBestFit:
        bestCount += 1
    else:
        gBestFit = newFit
        print(gBestFit)
        bestCount = 0
    plotx.append(genCount)
    ploty[0].append(gBestFit)
    ploty[1].append(gAvgFit)
    plt.plot(plotx,ploty[0],'r',plotx,ploty[1],'g')
    plt.pause(0.05)

print("Ilość generacji:")
print(genCount)
print("Najlepszy wynik")
print(gBestFit)
print("Wciśnij enter by kontynuować...")
input()
