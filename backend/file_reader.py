import json
import logging 
import pathlib
from sys import path_hooks

from typing import Dict


class FileReader:

    def readFile(fileName):
        #Read json file and return Dictionnary of data in json file

        fileExtension = pathlib.Path(fileName).suffix
       
        if fileExtension == ".json":
            try:
                with open(fileName) as d:
                    return json.load(d)

            except Exception:
                logging.error("Error occured while loading "+fileName)
                raise FileError()
        
        else:
            logging.error("Error occured while loading "+fileName)
            raise FileError()


class FileError(Exception):
    #File is incorrect format"

    def __init__(self,message = " Input file should have .json format"):
        self.message = message
        super().__init__(self.messages)

