import backoff
import requests
from plexapi.server import PlexServer

from helpers.misc import backoff_handler, dict_merge
from helpers.trakt import extract_list_user_and_key_from_url
from misc.log import logger

log = logger.get_logger(__name__)


class Plex:

    def __init__(self, cfg):
        self.cfg = cfg

    def _get_library(self):
        plex = PlexServer(self.cfg.plex.url, self.cfg.plex.token)
        movie_library = plex.library.section(self.cfg.plex.movies_library)
        return movie_library

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_movies(self):
        movie_library = self._get_library()
        all_movies = movie_library.all()
        return all_movies

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def add_collection(self,  rating_key, collection_name):
        log.debug("Adding collection %s to %s", collection_name, rating_key)
        movie_library = self._get_library()
        library_key = movie_library.key
        params = {
                  "type": 1,
                  "id": rating_key,
                  "collection[0].tag.tag": collection_name,
                  "collection.locked": 1
                  }
        headers = {"X-Plex-Token": self.cfg.plex.token}

        url = "{base_url}/library/sections/{library}/all".format(
                base_url=self.cfg.plex.url,
                library=library_key)

        r = requests.put(url, headers=headers, params=params)
        if r.status_code == 200:
            return True
        return None

