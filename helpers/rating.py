from misc.log import logger
import json
import requests

log = logger.get_logger(__name__)

def get_rating(apikey,imdbID):
    log.debug("Requesting ratings from omdb for imdbID: %s".format(imdbID))
    r = requests.get('http://www.omdbapi.com/?i=' + imdbID + '&apikey=' + apikey)
    log.debug(r)
    if(r.status_code == 200):
        for source in json.loads(r.text)["Ratings"]:
            if(source['Source'] == 'Rotten Tomatoes'):
                return int(source['Value'].split('%')[0])
    return -1
