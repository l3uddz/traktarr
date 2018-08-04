from misc.log import logger
import json
import requests

log = logger.get_logger(__name__)

def get_movie_rating(imdbID,source=None):
    r = requests.get('http://www.omdbapi.com/?i=' + imdbID + '&apikey=a7f5bf93')
    if(r.status_code == 200):
        for source in json.loads(r.text)["Ratings"]:
            if(source['Source'] == 'Rotten Tomatoes'):
                return int(source['Value'].split('%')[0])
    return -1
