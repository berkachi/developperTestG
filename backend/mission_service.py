from pathlib import Path

from context import ContextLoader
from prediction import PredictionService


class MissionService:

    def __init__(self,missionDetailsFilePath):
        missionDetails = ContextLoader.loadMissionDetails(fileName= str(missionDetailsFilePath))
        self.predictionServices = PredictionService(missionDetails=missionDetails)


    def getMissionSuccessOdds(self, interceptedData):
        # calculate the probability of success reaching the destination without being captured by bounty hunters

        if isinstance(interceptedData, Path):
            interceptedData = ContextLoader.loadInterceptedDataFromFile(filePath=str(interceptedData))

            return self.predictionService.getProbabilityOfSuccess(countdown=interceptedData.countdown,hunterSchedule=interceptedData.bountyHunterSchedule)

        else:
            interceptedData = ContextLoader.loadInterceptedData(rawInterceptedData=interceptedData)

        return self.predictionService.getProbabilityOfSuccess(countdown=interceptedData.countdown,hunterSchedule=interceptedData.bountyHunterSchedule)
