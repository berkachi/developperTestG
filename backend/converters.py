import logging
from collections import defaultdict
from typing import Dict, List
from turtle import distance #provides a default value for the key that does not exists
from db_connector import DBConnector


class PlanetGraph:

    def __init__(self):
        self.planets = set()
        self.routes = defaultdict(list)
        self.distance = {}

    def addRoute(self,departure, destination,distance):
        #add route to planet graph
        
        #adding planets to the set to have a set of unique different planets
        self.planets.add(departure)
        self.planets.add(destination)

        #creating route between planets
        self.routes[departure].append(destination)
        self.routes[destination].append(departure)

        #adding distance for routes
        self.distance[departure,destination] = distance
        self.distance[destination,departure] = distance

    def __eq__(self, other):
        #indicate if 2 parcour are the same
        if isinstance(other,PlanetGraph):
            return self.planets==other.planets and self.routes==other.routes and self.distance==other.distance



class MissionDetails:

    def __init__(self, autonomy, departure, arrival,routes):
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        self.routes = routes

    def __eq__(self, other):
        if isinstance(other, MissionDetails):
            return self.autonomy == other.autonomy and self.departure == other.departure and self.arrival == other.arrival and self.routes == other.routes
        return False


class FieldConverter:

    def getField(details, fieldName):
        #check if field is present

        field = details.get(fieldName)
        if not field:
            logging.exception(fieldName+" Field must be provided")
            raise MissingFieldException
        return field

    def validateField(field, fieldName):
        #validate if field have a positive integer

        if not isinstance(field, int):
            logging.exception(fieldName+" must be an int, but was: {type(field)}")
            raise ValidateFieldException()

        elif (field<=0):
            logging.exception(fieldName+" must be greater than 0,but was: {type(field)}")
            raise ValidateFieldException()

class MissingFieldException(Exception):
    #field not found

    def __init__(self, fieldName):
        self.message = fieldName+" field must be provided !"
        super().__init__(self.message)


class ValidateFieldException(Exception):
   #field doesn't meet expectations

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MissionConverter(FieldConverter):

    def missionDetails(details, directory):
        #define mission details parameters

        autonomy = MissionConverter.getField(details=details, fieldName="autonomy")
        departure = MissionConverter.getField(details=details, fieldName="departure")
        arrival = MissionConverter.getField(details=details, fieldName="arrival")
        planetDB = MissionConverter.getField(details=details, fieldName="routes_db")

        MissionConverter.validateField(field=autonomy,fieldName="autonomy")
        #planetDbFile = directory+"/"+planetDB
        planetGraph = MissionConverter.loadRoutes(planetDB)

        return MissionDetails(autonomy=autonomy, departure=departure, arrival=arrival, routes=planetGraph)


    def loadRoutes(dbFile):
        #create graph for routes from db

        routes = MissionConverter.getRoutes(dbFile)
        planetGraph = PlanetGraph()
        
        for route in routes:
            planetGraph.addRoute(departure=route[0],destination=route[1],distance=route[2])

        return planetGraph

    
    def getRoutes(dbFile):
        #get routes between planets from db

        routeQuery = "SELECT origin, destination, travelTime from routes"
        return DBConnector.iterator(dbFile=dbFile, query=routeQuery)

class InterceptedData:

    def __init__(self,countdown, bountyHunterSchedule):
        self.countdown=countdown
        self.bountyHunterSchedule = bountyHunterSchedule

    def __eq__(self, other):
        if isinstance(other, InterceptedData):
            return self.countdown == other.countdown and self.bountyHunterSchedule == other.bountyHunterSchedule
        return False


class InterceptedDataConverter(FieldConverter):

    def mapInterceptedData(data):
        #map intercepted data

        countdown = InterceptedDataConverter.getField(details=data,fieldName="countdown")

        InterceptedDataConverter.validateField(field=countdown, fieldName="countdown")

        schedule = InterceptedDataConverter.getField(details=data,fieldName="bounty_hunters")
        
        bountyHunterSchedule = [(i["planet"],i["day"]) for i in schedule]

        return InterceptedData(countdown=countdown, bountyHunterSchedule=bountyHunterSchedule)

