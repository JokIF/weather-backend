import ujson
from django.conf import settings

from GisMeteoImage.core.gismeteoParser import GismeteoParser
from GisMeteoImage.core.classes import GismeteoResponse


def get_test_data():
    with open("gisemteo-response-test.json", "r") as file: #settings.GISMETEO_DATA_JSON
        return ujson.loads(file.read())
    
def gismeteo_response_from_raw_data(raw_data, many=True):
    if many:
        return GismeteoResponse(
            raw=raw_data, 
            parsed=[GismeteoParser(data) for data in raw_data["response"]]
            )
    
    return GismeteoResponse(
        raw=raw_data, 
        parsed=GismeteoParser(raw_data)
        )
