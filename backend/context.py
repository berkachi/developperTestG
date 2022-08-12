import os
from typing import Dict

from converters import (InterceptedData, InterceptedDataConverter, MissionConverter, MissionDetails)
from file_reader import FileReader

class ContextLoader:
    
    @staticmethod
    def loadMissionDetails(fileName):
        #load mission details from input file

        missionDetails = FileReader.readFile(fileName)
        directory = os.path.dirname(fileName)
        return MissionConverter.missionDetails(missionDetails,directory)

    @staticmethod
    def loadInterceptedDataFile(fileName):
        #load intercepted data from input file

        interceptedData = FileReader.readFile(fileName)
        return InterceptedDataConverter.mapInterceptedData(data=interceptedData)


    @staticmethod
    def loadInterceptedData(interceptedData):
        #loads intercepted data from json compatible data

        return InterceptedDataConverter.mapInterceptedData(data=interceptedData)
