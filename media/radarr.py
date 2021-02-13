import backoff

from helpers.misc import backoff_handler, dict_merge
from media.pvr import PVR
from misc.log import logger

log = logger.get_logger(__name__)


class Radarr(PVR):
    def get_objects(self):
        return self._get_objects('api/movie')

    def get_exclusions(self):
        return self._get_objects('api/exclusions')

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def add_movie(self, movie_tmdb_id, movie_title, movie_year, movie_title_slug, quality_profile_id, root_folder,
                  min_availability_temp, search_missing=False):
        payload = self._prepare_add_object_payload(movie_title, movie_title_slug, quality_profile_id, root_folder)

        # replace radarr minimum_availability if supplied
        if min_availability_temp == 'announced':
            minimum_availability = 'announced'
        elif min_availability_temp == 'in_cinemas':
            minimum_availability = 'inCinemas'
        elif min_availability_temp == 'predb':
            minimum_availability = 'preDB'
        else:
            minimum_availability = 'released'

        payload = dict_merge(payload, {
            'tmdbId': movie_tmdb_id,
            'year': int(movie_year),
            'minimumAvailability': minimum_availability,
            'addOptions': {
                'searchForMovie': search_missing
            }
        })

        return self._add_object('api/movie', payload, identifier_field='tmdbId', identifier=movie_tmdb_id)
