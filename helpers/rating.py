from misc.log import logger
import json
import requests

log = logger.get_logger(__name__)


def get_rating(omdb_apikey, movie):
    """
    Lookup movie ratings via OMDb

    :param omdb_apikey: OMDb api key
    :param movie: sorted_movie item
    :return: rating or false if no rating found
    """

    ratings_exist = False
    movie_imdbid = movie['movie']['ids']['imdb']
    movie_year = str(movie['movie']['year']) if movie['movie']['year'] else '????'

    if movie_imdbid:
        log.debug("Requesting info from OMDb for: \'%s (%s)\' [IMDb ID: %s]",
                  movie['movie']['title'],
                  movie_year,
                  movie_imdbid)
        r = requests.get('http://www.omdbapi.com/?i=' + movie_imdbid + '&apikey=' + omdb_apikey)
        if r.status_code == 200 and json.loads(r.text)["Response"] == 'True':
            log.debug("Successfully requested ratings from OMDB for \'%s (%s)\' [IMDb ID: %s]",
                      movie['movie']['title'],
                      movie_year,
                      movie_imdbid)
            for source in json.loads(r.text)["Ratings"]:
                if source['Source'] == 'Rotten Tomatoes':
                    # noinspection PyUnusedLocal
                    ratings_exist = True
                    log.debug("Rotten Tomatoes score of %s for: \'%s (%s)\' [IMDb ID: %s]",
                              source['Value'],
                              movie['movie']['title'],
                              movie_year,
                              movie_imdbid)
                    return int(source['Value'].split('%')[0])
            if not ratings_exist:
                log.debug("No Rotten Tomatoes score found for: \'%s (%s)\' [IMDb ID: %s]",
                          movie['movie']['title'],
                          movie_year,
                          movie_imdbid)
        else:
            log.debug("Error encountered when requesting ratings from OMDb for: \'%s (%s)\' [IMDb ID: %s]",
                      movie['movie']['title'],
                      movie_year,
                      movie_imdbid)
    else:
        log.debug("Skipping OMDb ratings lookup because no IMDb ID was found for: \'%s (%s)\'",
                  movie['movie']['title'],
                  movie_year)

    return False


def does_movie_have_min_req_rating(api_key, sorted_movie, rating):

    # pull RT score
    movie_rating = get_rating(api_key, sorted_movie)

    # convert movie year to string
    movie_year = str(sorted_movie['movie']['year']) \
        if sorted_movie['movie']['year'] else '????'

    if not movie_rating:
        log.info("SKIPPING: \'%s (%s)\' because a Rotten Tomatoes score could not be found.", sorted_movie['movie']['title'],
                 movie_year)
        return False
    elif movie_rating < rating:
        log.info("SKIPPING: \'%s (%s)\' because its Rotten Tomatoes score of %d%% is below the required score of %d%%.",
                 sorted_movie['movie']['title'], movie_year, movie_rating, rating)
        return False
    elif movie_rating >= rating:
        log.info("ADDING: \'%s (%s)\' because its Rotten Tomatoes score of %d%% is above the required score of %d%%.",
                 sorted_movie['movie']['title'], movie_year, movie_rating, rating)
        return True
