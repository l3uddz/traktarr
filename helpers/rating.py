from misc.log import logger
import json
import requests

log = logger.get_logger(__name__)


def get_rating(apikey, movie):

    ratings_exist = False
    imdb_id = movie['movie']['ids']['imdb']
    if imdb_id:
        log.debug("Requesting info from OMDb for: \'%s (%s)\' | IMDb ID: %s",
                  movie['movie']['title'],
                  str(movie['movie']['year']) if movie['movie']['year'] else '????',
                  imdb_id)
        r = requests.get('http://www.omdbapi.com/?i=' + imdb_id + '&apikey=' + apikey)
        if r.status_code == 200 and json.loads(r.text)["Response"] == 'True':
            log.debug("Successfully requested ratings from OMDB for \'%s (%s)\' | IMDb ID: %s",
                      movie['movie']['title'],
                      str(movie['movie']['year']) if movie['movie']['year'] else '????',
                      imdb_id)
            for source in json.loads(r.text)["Ratings"]:
                if source['Source'] == 'Rotten Tomatoes':
                    # noinspection PyUnusedLocal
                    ratings_exist = True
                    log.debug("Rotten Tomatoes score of %s for: \'%s (%s)\' | IMDb ID: %s ",
                              source['Value'],
                              movie['movie']['title'],
                              str(movie['movie']['year']) if movie['movie']['year'] else '????',
                              imdb_id)
                    return int(source['Value'].split('%')[0])
            if not ratings_exist:
                log.debug("No Rotten Tomatoes score found for: \'%s (%s)\' | IMDb ID: %s",
                          movie['movie']['title'],
                          str(movie['movie']['year']) if movie['movie']['year'] else '????',
                          imdb_id)
        else:
            log.debug("Error encountered when requesting ratings from OMDb for: \'%s (%s)\' | IMDb ID: %s",
                      movie['movie']['title'],
                      str(movie['movie']['year']) if movie['movie']['year'] else '????',
                      imdb_id)
    else:
        log.debug("Skipping OMDb ratings lookup because no IMDb ID was found for: \'%s (%s)\'",
                  movie['movie']['title'],
                  str(movie['movie']['year']) if movie['movie']['year'] else '????')

    return -1