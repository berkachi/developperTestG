import sys
from pathlib import Path

import typer 
from mission_service import MissionService

app = typer.Typer()

@app.command()
def get_odds(missionDetailsFilePath= typer.Argument(help="The path to the file containing the Millenium Falcon Mission details"),interceptedDataFile= typer.Argument(help="The path to the file cointaining the rebel intercepted data")):
    try:
        missionService = MissionService(missionDetailsFilePath=missionDetailsFilePath)
        odds = missionService.getMissionSuccessOdds(interceptedData = interceptedDataFile)
        typer.echo(odds)

    except:
        typer.echo("An error occured. Please make sure that the file paths and formats are correct.")
        sys.exit(1)
        

if __name__ == '__main__':
    app()
