from helpers import str as misc_str
from misc.log import logger

import requests

log = logger.get_logger(__name__)


def does_movie_exist_on_tmdb(sorted_movie):
    try:
        movie_title = sorted_movie['movie']['title']
        movie_year = str(sorted_movie['movie']['year']) \
            if sorted_movie['movie']['year'] else '????'
        movie_tmdbid = sorted_movie['movie']['ids']['tmdb']

        req = requests.get('https://www.themoviedb.org/movie/%s' % movie_tmdbid)

        if req.status_code == 200:
            log.debug("\'%s (%s)\' [TMDb ID: %s] exists on TMDb.", movie_title, movie_year, movie_tmdbid)
            return True

        log.debug("SKIPPING: \'%s (%s)\' [TMDb ID: %s] because it does not exist on TMDb.", movie_title, movie_year,
                  movie_tmdbid)
        return False

    except Exception:
        log.exception("Exception validating TMDb ID: ")

    return False
