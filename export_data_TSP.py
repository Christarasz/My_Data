from tkinter import *
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        plt.scatter(self.x,self.y,color="red")

    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = np.sqrt((xDis ** 2) + (yDis ** 2))
        return distance

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"



#############
class Fitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness= 0.0

    def routeDistance(self):
        if self.distance ==0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i + 1 < len(self.route):
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
            return self.fitness


###########
def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route


##########
def initialPopulation(popSize, cityList):
    population = []

    for i in range(0, popSize):
        population.append(createRoute(cityList))
    return population

##########
def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)

###########
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults

########
def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool


########
def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child

#######
def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])

    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

###########

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))

            city1 = individual[swapped]
            city2 = individual[swapWith]

            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

########
def mutatePopulation(population, mutationRate):
    mutatedPop = []

    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

#########
def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

##########
def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    text.delete('1.0',END)
    text.update()
    pop = initialPopulation(popSize, population)
    initial_distance=np.round(1 / rankRoutes(pop)[0][1],decimals=2,out=None)
    # print("Initial distance was : " ,initial_distance)
    text.insert(END,"  Initial distance : %5.1f m \n" %(initial_distance))

    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)

    final_distance=np.round(1 / rankRoutes(pop)[0][1],decimals=2,out=None)
    # print("Final distance is : ",final_distance)
    text.insert(END,"  Final distance : %5.1f m \n " %(final_distance))

    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    text.insert(END," Best route : {}".format(bestRoute))
    return bestRoute
#############
# cityList = []
#
# for i in range(0,25):
#     cityList.append(City(x=int(random.random() * 200), y=int(random.random() * 200)))

########

def run_programm ():
    x_v,y_v,number_data,popSize,eliteSize,mutationRate,generations=get_values()

    cityList = []
    for i in range(0,number_data):
        cityList.append(City(x=random.randint(0,x_v), y=random.randint(0,y_v)))
    geneticAlgorithm(population=cityList, popSize=popSize, eliteSize=eliteSize, mutationRate=mutationRate, generations=generations)
    plt.show()

def get_values():
    x_v=random.randint(0,int(entry2.get()))
    y_v=random.randint(0,int(entry3.get()))
    number_data=int(entry1.get())
    popSize=int(entry4.get())
    eliteSize=int(entry5.get())
    generations=int(entry6.get())
    mutationRate=float(entry7.get())
    return (x_v,y_v,number_data,popSize,eliteSize,mutationRate,generations)

master=Tk()
master.title(" ")
master.geometry('600x400')

label_title=Label(master,text="TSP random data creation",bg="black",fg="red",font=50)
label_title.grid(row=0,column=0,columnspan=5)

label_1=Label(master,text="Number of data",width=20,font=26)
label_1.grid(row=1,column=0,sticky="WE")

entry1=Entry(master,width=4,bg="yellow",fg="black")
entry1.grid(row=1,column=1,sticky="W")

label_2=Label(master,text="X axis limit",width=20,font=26)
label_2.grid(row=2,column=0,sticky="WE")

entry2=Entry(master,width=4,bg="yellow",fg="black")
entry2.grid(row=2,column=1,sticky="W")

label3=Label(master,text="Y axis limit",width=20,font=26)
label3.grid(row=3,column=0,sticky="WE")

entry3=Entry(master,width=4,bg="yellow",fg="black")
entry3.grid(row=3,column=1,sticky="W")

label4=Label(master,text="Set population size",width=20,font=26)
label4.grid(row=1,column=3,sticky="WE")

entry4=Entry(master,width=4,bg="yellow",fg="black")
entry4.grid(row=1,column=4,sticky="W")

label5=Label(master,text="Set elite size",width=20,font=26)
label5.grid(row=2,column=3,sticky="WE")

entry5=Entry(master,width=4,bg="yellow",fg="black")
entry5.grid(row=2,column=4,sticky="W")

label6=Label(master,text="Set generations number",width=20,font=26)
label6.grid(row=3,column=3,sticky="WE")

entry6=Entry(master,width=4,bg="yellow",fg="black")
entry6.grid(row=3,column=4,sticky="W")

label7=Label(master,text="Set mutation Rate",width=20,font=26)
label7.grid(row=4,column=3,sticky="WE")

entry7=Entry(master,width=4,bg="yellow",fg="black")
entry7.grid(row=4,column=4,sticky="W")

btn1=Button(master,text="Read data",width=13,font=26,bg="red",fg="black")
btn1.grid(row=3,column=0,sticky="ES")

btn=Button(master,text="Run ",width=13,font=26,bg="red",fg="black",command=run_programm)
btn.grid(row=4,column=0,sticky="EN")

text=Text(master,bg="green",fg="black",font=20,height=10,width=70)
text.grid(row=3,column=1,sticky="W",rowspan=2)

master.rowconfigure(0,weight=0)
master.rowconfigure(1,weight=1)
master.rowconfigure(2,weight=1)
master.rowconfigure(3,weight=1)
master.rowconfigure(4,weight=1)
master.rowconfigure(5,weight=0)

master.columnconfigure(0,weight=1)
master.columnconfigure(1,weight=0)
master.columnconfigure(2,weight=0)
master.columnconfigure(3,weight=1)
master.columnconfigure(4,weight=1)

master.mainloop()




