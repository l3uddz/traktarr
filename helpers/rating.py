from misc.log import logger
import json
import requests

log = logger.get_logger(__name__)

def get_rating(apikey,imdbID):
    log.debug("Requesting ratings from omdb for imdbID: %s".format(imdbID))
    r = requests.get('http://www.omdbapi.com/?i=' + imdbID + '&apikey=' + apikey)
    if(r.status_code == 200):
        log.debug("Successfully requested ratings from OMDB")
        for source in json.loads(r.text)["Ratings"]:
            if(source['Source'] == 'Rotten Tomatoes'):
                log.debug("Rotten Tomatoes shows rating: %s for imdbID: %s".format(source['Value'],imdbID))
                return int(source['Value'].split('%')[0])
    else:
        log.error("ERROR encountered while requesting rating for imdbID: %s Status Code: %d".format(imdbID,r.status_code))
    return -1
