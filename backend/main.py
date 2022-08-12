import logging
import os
from pathlib import Path
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from mission_service import MissionService

from pydantic import BaseModel
from starlette.responses import RedirectResponse

logging.getLogger().addHandler(logging.StreamHandler())

description = """
Give Me The Odds API lets you get the odds of successfully reaching the destination planet.
You can read more about the challenge [here](https://github.com/dataiku/millenium-falcon-challenge).
"""

app = FastAPI(title="Give Me The Odds", description=description)


@app.on_event("startup")
def get_mission_service():
    file_path= os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    #missionDetailsFilePath = os.path.join(file_path, "millennium-falcon.json")
    missionDetailsFilePath = ("millennium-falcon.json")
    return MissionService(missionDetailsFilePath=Path(missionDetailsFilePath))


mission_service= get_mission_service()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url=f"/docs/", status_code=303)


class InterceptedDataModel(BaseModel):
    countdown: int = 6
    bounty_hunters: List[dict] = [
        {"planet": "Tatooine", "day": 4},
        {"planet": "Dagobah", "day": 5},
    ]


@app.post("/v1/mission-success/")
async def calculate_mission_success_odds(item):
    intercepted_data = jsonable_encoder(item)
    return mission_service.getMissionSuccessOdds(intercepted_data=intercepted_data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
