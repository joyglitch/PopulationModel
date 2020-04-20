from __future__ import print_function, division

import sys

import numpy as np
import random

class Animal:

    # requried variables: needed for subclasses
    location = [0,0]
    probRepro = 0
    sense = 3
    lifeSpan = 100
    beStill = False
    mated = False
    matedLast = 0

    def __init__(self, mapSize, location=None, maxHunger=10, hunger=0, age=0):

        if location == None:
            location = [np.random.randint(0, mapSize), np.random.randint(0, mapSize)]
        self.location = location

        self.steps = age
        self.mapSize = mapSize
        self.stepSize = 1
        self.foodEaten = 0
        self.hunger = hunger
        self.alive = True
        self.maxHunger = maxHunger

    def step(self, direct = None):
        self.hunger = self.hunger + 1
        self.steps = self.steps + 1

        #move once for every stepSize
        for i in range(0, self.stepSize):
            #one for each direction
            if(direct == None):
                direct = np.random.randint(0,8)

            # if the direction is 1,0,7 move x by +1
            if ((direct==0) or (direct==1) or (direct==7)):
                self.location[0] = self.location[0] + 1

            # if the direction is 1,2,3 move y by +1
            if ((direct==1) or (direct==2) or (direct==3)):
                self.location[1] = self.location[1] + 1

            # if the direction is 3,4,5 move x by -1
            if ((direct==3) or (direct==4) or (direct==5)):
                self.location[0] = self.location[0] - 1

            # if the direction is 5,6,7 move y by -1
            if ((direct==5) or (direct==6) or (direct==7)):
                self.location[1] = self.location[1] - 1
        self.locationCheck()

    # check if location needs to wrap
    def locationCheck(self):
        for i in range(0,2):
            if (self.location[i] >= self.mapSize):
                self.location[i] = self.location[i] - self.mapSize
            elif (self.location[i] < 0):
                self.location[i] = self.mapSize - abs(self.location[i])

    def vicinityCheck(self, animal2):
        a1X = self.location[0]
        a1Y = self.location[1]
        a2X = animal2.location[0]
        a2Y = animal2.location[1]

        sense = 1
        nearby = False

        for i in range(-sense, (sense+1)):
            if nearby == False:
                if (a1X == (a2X + i)):
                    for j in range(-sense, (sense+1)):
                        if nearby == False:
                            if (a1Y == (a2Y + j)):
                                nearby = True
        return nearby

    def interactOwnSpecies(self, partner, animalArray, probLitter=False):
        together = False
        mated = False
        if not partner.beStill:
            together = self.vicinityCheck(partner)
        if together:
            if self.mated == False and partner.mated == False:
                if not probLitter:
                    if np.random.rand() < self.probRepro:
                        for i in range(0, self.avgLitter):
                            baby = self.reproduce(animalArray, partner)
                            if baby == False:
                                break
                            self.reproduced(partner)
                            mated = True
                else:
                    reproOdds = self.probRepro
                    for i in range(0, self.maxLitter):
                        baby = False
                        if np.random.rand() < reproOdds:
                            baby = self.reproduce(animalArray, partner)
                            if baby == False:
                                break # animals not of age so don't try again
                            reproOdds = reproOdds - 0.05
                            mated = True
                            self.reproduced(partner)
                return mated
        return False

    def reproduce(self, animalArray, partner, ofAge, baby):
        # need to be of age to reproduce
        if self.steps > ofAge and partner.steps > ofAge:
            # check if they have enough energy to reproduce
            if self.hunger < self.maxHunger/2 and partner.hunger < partner.maxHunger/2:
                animalArray.append(baby)
                animalArray[-1].step()
                self.mated = True
                self.matedLast = self.steps
                partner.mated = True
                partner.matedLast = partner.steps
                return True
        return False

    def reproduced(self, partner):
        self.hunger = self.hunger * 1.25               # Edit this value?
        partner.hunger = partner.hunger * 1.25         # Edit this value?

    def hunt(self, foodArray):
        ax = self.location[0]
        ay = self.location[1]
        sense = self.sense

        inRange = []
        for i in range(0, len(foodArray)):
            tempx = foodArray[i].location[0]
            if tempx < (ax+sense) and tempx > (ax-sense):
                # good X, so check Y
                tempy = foodArray[i].location[1]
                if tempy < (ay+sense) and tempy > (ay-sense):
                    inRange.append(i)

        if (len(inRange) == 0):
            return None

        steps = sense + 1
        closestFood = []

        for i in range(0, len(inRange)):

            tempx = foodArray[inRange[i]].location[0]
            tempy = foodArray[inRange[i]].location[1]

            if(abs(ax-tempx) > abs(ay-tempy)):
                if(steps > abs(ax-tempx)):
                    steps = abs(ax-tempx)
                    closestFood = foodArray[inRange[i]].location
            else:
                if(steps > abs(ax-tempx)):
                    steps = abs(ay-tempy)
                    closestFood = foodArray[inRange[i]].location

        # pick the direction to move towards the food
        tempx = closestFood[0]
        tempy = closestFood[1]

        xdist = abs(ax-tempx)
        ydist = abs(ay-tempy)

        if(xdist < ydist):
            #choose xdist
            if((ax-tempx) < 0):
                return 4
            else:
                return 0
        elif(ydist < xdist):
            #choose ydist
            if ((ay-tempy) < 0):
                return 6
            else:
                return 2
        else:
            if (((ax-tempx) < 0) and ((ay-tempy) < 0)):
                return 3
            if (((ax-tempx) < 0) and ((ay-tempy) > 0)):
                return 5
            if (((ax-tempx) > 0) and ((ay-tempy) < 0)):
                return 1
            if (((ax-tempx) > 0) and ((ay-tempy) > 0)):
                return 7

#########################################################################################################
# Rabbit class used in ecosystem -----------------------------------------------------------------------#
#########################################################################################################
class Rabbit(Animal):

    lifeSpan = 84 # 7 years
    probRepro = 0.5
    avgLitter = 5
    maxLitter = 14
    species = 'Rabbit'
    eatMush = False

    def step(self, foodArray = None):
        if self.mated == True:
            # 2 steps need to have occurred before mating again
            if self.steps - self.matedLast == 2:
                self.mated = False
        if(foodArray != None):
            super().step(self.hunt(foodArray))
        else:
            super().step()

    def interactMushroom(self, mushroom):
        together = False
        if not mushroom.eaten:
            together = self.vicinityCheck(mushroom)
        if together:
            mushroom.eaten = True
            self.hunger = self.hunger / 1.25       # Edit this value?
            return True
        return False

    def reproduce(self, animalArray, rabbit):
        x = self.location[0]
        y = self.location[1]
        baby = Rabbit(self.mapSize, location=[x,y], maxHunger=self.maxHunger)
        minAge = 7 # need to be 8 months to reproduce
        return super().reproduce(animalArray, rabbit, minAge, baby)

#########################################################################################################
# Fox class used in ecosystem --------------------------------------------------------------------------#
#########################################################################################################
class Fox(Animal):

    lifeSpan = 168 # 14 years
    probRepro = 0.3
    avgLitter = 4
    maxLitter = 11
    species = 'Fox'

    def step(self, foodArray = None):
        if self.mated == True:
            # 12 steps need to have occurred before mating again
            if self.steps - self.matedLast == 12:
                self.mated = False
        if(foodArray != None):
            super().step(self.hunt(foodArray))
        else:
            super().step()

    def interactRabbit(self, rabbit):
        together = False
        if not rabbit.beStill:
            together = self.vicinityCheck(rabbit)
        if (together):
            rabbit.beStill = True
            self.hunger = self.hunger / 1.25 # Edit this value?
            return True
        return False

    #add interact mushroom to allow for omnivourism
    """Suggested edit to alter how much hunger a mushrooms satisfies to be less than a rabbit"""
    def interactMushroom(self, mushroom):
        together = False
        if not mushroom.eaten:
            together = self.vicinityCheck(mushroom)
        if together:
            mushroom.eaten = True
            self.hunger = self.hunger / 1.25
            return True
        return False

    def reproduce(self, animalArray, fox):
        x = self.location[0]
        y = self.location[1]
        baby = Fox(self.mapSize, location=[x,y], maxHunger=self.maxHunger)
        minAge = 9 # need to be 10 months to reproduce
        return super().reproduce(animalArray, fox, minAge, baby)
