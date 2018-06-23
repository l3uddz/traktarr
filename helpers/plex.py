from helpers import str as misc_str
from misc.log import logger

log = logger.get_logger(__name__)


def plex_movies_to_imdb_dict(plex_movies):
    """
    Given a list of plex movies, returns a dict where the key is the imdb id
    and the value is the plex movie object
    """
    imdb = {}
    try:
        for m in plex_movies:
            if 'imdb://' in m.guid:
                imdb_id = m.guid.split('imdb://')[1].split('?')[0]
            elif 'themoviedb://' in m.guid:
                # TODO if the user uses the movie db metadata agent
                # we will need to special case that, and lookup the imdb id
                log.warn("SKIPPING tmdb ids not supported: s %s ",  m.name)
                imdb_id = None
            else:
                imdb_id = None
            imdb[imdb_id] = m
        return imdb
    except Exception as e:
        log.exception("Exception processing Radarr movies to TMDB dict: %s", e)
    return None


def match_plex_to_trakt_movies(plex_movies, trakt_movies):
    """
    Given a list of plex movies and trakt movies, returns a list containing
    only the plex movies that exist in the trakt list. Matching is done via
    imdb id.
    """
    if not plex_movies or not trakt_movies:
        log.error("Inappropriate parameters were supplied")
        return None

    try:
        plex_by_imdbs = plex_movies_to_imdb_dict(plex_movies)
        if not plex_by_imdbs:
            return None
        trakt_imdbs = [m['movie']['ids']['imdb'] for m in trakt_movies]
        matched_movies = [plex_by_imdbs[imdb]
                          for imdb in trakt_imdbs if imdb in plex_by_imdbs]
        log.info("Matched %d Plex to %d Trakt movies",
                 len(plex_movies), len(matched_movies))
        return matched_movies
    except Exception as e:
        log.exception("Exception matching Plex to Trakt list: %s", e)
    return None


def is_movie_in_collection(movie, col_name):
    return any(col.tag == col_name for col in movie.collections)

