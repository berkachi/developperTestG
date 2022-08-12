import logging
from typing import Dict, List, Tuple

from converters import MissionDetails, PlanetGraph

logging.getLogger().addHandler(logging.StreamHandler())

class PredictionService:

    def __init__(self, missionDetails):
        self.autonomy= missionDetails.autonomy
        self.departure = missionDetails.departure
        self.destination = missionDetails.arrival
        self.planetGraph = missionDetails.routes
        self.paths =[]


    def successProbability(self, countdown, hunterSchedule):
        #calculate probability of successfully reaching planet in %
        self.generateAllPathsBetweenTwoPlanets(departurePlanet=self.departure, destinationPlanet=self.destination, timeLimit=countdown)
        
        if not self.paths:
            logging.info("No path were found")
            return 0

        detailedTravelPlan = [self.getDetailedTravelPlan(plan) for plan in self.paths]
        optimizedPaths = [self.optimizePath(plan, hunterSchedule, countdown=countdown) for plan in detailedTravelPlan]
        captureAttemptCount = PredictionService.getLowestCaptureCount(hunterSchedule=hunterSchedule,optimizedPaths=optimizedPaths)
        probabilityOfCapture = PredictionService.getProbabilityOfCapture(captureAttemptCount=captureAttemptCount)
        
        return PredictionService.convertCaptureProbabilityToSuccessRate(probabilityOfCapture=probabilityOfCapture)


    def generateAllPathsBetweenTwoPlanets(self,departurePlanet,destinationPlanet, timeLimit):
        #generate list of paths between 2planets

        self.paths=[]
        path=[]
        visited = {planet:False for planet in self.planetGraph.planets}
        self.generateAllPaths(departurePlanet,destinationPlanet,visited, path, timeLimit)


    def generateAllPAths(self,currentPlanet, destinationPlanet, visited, path, timeLimit):
        #generate list of all paths between planets

        visited[currentPlanet] = True
        path.append(currentPlanet)

        travelTime= self.getTravelDays(path)

        if travelTime> timeLimit:
            logging.info(path+" excceeded the time limit.")
        elif currentPlanet == destinationPlanet:
            logging.info("Fount path: "+path)
            self.paths.append(path.copy())

        else:
            for neighbourPlanet in self.planetGraph.routes[currentPlanet]:
                if not visited[neighbourPlanet]:
                    self.generateAllPAths(neighbourPlanet,destinationPlanet,visited,path,timeLimit)

            path.pop()
            visited[currentPlanet]=False


    def getDetailedTravelPlan(self, path):
        #get a detailed travel plan

        travelPlan=[]
        total=0
        currentFuel= self.autonomy
        refuellingDay =1

        if not path:
            return travelPlan
        
        for i in range(0,len(path)-1):
            travelPlan.append((path[i],total))
            nextHopInDays = self.planetGraph.distances[(path[i]),path[i+1]]

            if currentFuel < nextHopInDays:
                total+= refuellingDay
                currentFuel += self.autonomy
                travelPlan.append((path[i], total))

            total+=nextHopInDays
            currentFuel -= nextHopInDays

        travelPlan.append(path[-1],total)
        return travelPlan

    def getTravelInDays(self, path):
        #get travel time in days

        total=0
        currentFuel = self.autonomy
        refuellingDay =1

        for i in range(0,len(path)-1):
            nextHopInDays = self.planetGraph.distances[(path[i], path[i + 1])]

            if currentFuel < nextHopInDays:
                total += nextHopInDays + refuellingDay
                currentFuel += self.autonomy - nextHopInDays

            else:
                total+=nextHopInDays
                currentFuel -=nextHopInDays

        return total


    def getLowestCaptureCount(hunterSchedule, optimizedPaths):
         lowestCaptureCount = None

         for path in optimizedPaths:
            captureAttemptCount = PredictionService.getCaptureAttemptCount(route=path, hunterSchedule=hunterSchedule)

            if lowestCaptureCount ==0:
                break

            elif (lowestCaptureCount is None or captureAttemptCount<lowestCaptureCount):
                lowestCaptureCount=captureAttemptCount

            return lowestCaptureCount

    def adjustFuellingNeeds(route, autonomy):
        # adjust route for fuelling needs

        newRoute=[]
        deviation =0
        lastPlanet = route[-1]
        currentFuel= autonomy

        for i in range(len(route)):
            currentRoute = route[i]
            newRoute.append((currentRoute[0],currentRoute[1]+deviation))

            if currentRoute != lastPlanet:
                nextRoute = route[i+1]
                nextFlightDistance = nextRoute[1] - currentRoute[1]
                if nextFlightDistance > currentFuel:
                    deviation+=1
                    currentFuel=autonomy
                    newRoute.append(currentRoute[0], currentRoute[1] + deviation)
                currentFuel = currentFuel - nextFlightDistance

        return newRoute
        

    def getCaptureAttemptCount(route, hunterSchedule):
        #get number of capture attempts having shortest route and hunter schedule

        captureAttempts=0
        for stop in route:
            if stop in hunterSchedule:
                captureAttempts+=1
       
        return captureAttempts

    def getProbabilityOfCapture(captureAttemptCount):
        #calculate probability of getting captured dpedning on number of attempts

        result = 0.0

        if captureAttemptCount ==0:
            return result

        for i in range(captureAttemptCount):
            result+= (9**i) / (10**(i+1))

        return result

    def convertCaptureProbabilityToSuccessRate(probabilityOfCapture):
        # convert prob of capture to success rate

        return int(round(1-probabilityOfCapture,2)*100)

    def avoidBountyHunters(stop, delay, hunterSchedule):
        #check if we can skip hunters

        for day in range(delay +1):
            if (stop[0],stop[1]+day) not in hunterSchedule:
                return True
        return False

    def optimizePath(path, hunterSchedule, countdown):
        #optimize travel path to be shortest and most efficient against the hunters schedule


        arrivalDay = path[-1][1]
        delayBudget = countdown - arrivalDay
        waitingDay = 1

        newPath =[]
        delay = 0
        previousStop = None

        if delayBudget == 0:
            return path

        for stop in path:
            if previousStop is not None and stop[0] == previousStop[0]:
                newPath.append((stop[0],stop[1]+delay))
            
            elif(newPath and stop in hunterSchedule and PredictionService.avoidBountyHunters(stop, delayBudget, hunterSchedule)and delayBudget!=0):
                lastStop = newPath[-1]
                newStop = (lastStop[0], lastStop[1]+ waitingDay)
                newPath.append(newStop)
                delayBudget -= waitingDay
                delay += waitingDay
                stop = (stop[0], stop[1] + delay)

                while stop in hunterSchedule and delayBudget != 0:
                    lastStop = newPath[-1]
                    newStop = (lastStop[0],lastStop[1] + waitingDay)
                    newPath.append(newStop)
                    delayBudget -= waitingDay
                    delay+=waitingDay

                newPath.append((stop[0],stop[1]))

            else:
                newPath.append((stop[0],stop[1]+delay))
            
            previousStop = stop
           
        return newPath


