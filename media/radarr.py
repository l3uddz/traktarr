from urllib.parse import urljoin

import backoff
import requests

from misc.log import logger

log = logger.get_logger(__name__)


def backoff_handler(details):
    log.warning("Backing off {wait:0.1f} seconds afters {tries} tries "
                "calling function {target} with args {args} and kwargs "
                "{kwargs}".format(**details))


class Radarr:
    def __init__(self, server_url, api_key):
        self.server_url = server_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
        }

    def validate_api_key(self):
        try:
            # request system status to validate api_key
            req = requests.get(urljoin(self.server_url, 'api/system/status'), headers=self.headers, timeout=30)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200 and 'version' in req.json():
                return True
            return False
        except Exception:
            log.exception("Exception validating api_key: ")
        return False

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_movies(self):
        try:
            # make request
            req = requests.get(urljoin(self.server_url, 'api/movie'), headers=self.headers, timeout=30)
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                log.debug("Found %d movies", len(resp_json))
                return resp_json
            else:
                log.error("Failed to retrieve all movies, request response: %d", req.status_code)
        except Exception:
            log.exception("Exception retrieving movies: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_profile_id(self, profile_name):
        try:
            # make request
            req = requests.get(urljoin(self.server_url, 'api/profile'), headers=self.headers, timeout=30)
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                for profile in resp_json:
                    if profile['name'].lower() == profile_name.lower():
                        log.debug("Found id of %s profile: %d", profile_name, profile['id'])
                        return profile['id']
                    log.debug("Profile %s with id %d did not match %s", profile['name'], profile['id'], profile_name)
            else:
                log.error("Failed to retrieve all quality profiles, request response: %d", req.status_code)
        except Exception:
            log.exception("Exception retrieving id of profile %s: ", profile_name)
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def add_movie(self, movie_tmdbid, movie_title, movie_year, movie_title_slug, profile_id, root_folder,
                  search_missing=False):
        try:
            # generate payload
            payload = {
                'tmdbId': movie_tmdbid, 'title': movie_title, 'year': movie_year,
                'qualityProfileId': profile_id, 'images': [],
                'monitored': True, 'rootFolderPath': root_folder,
                'minimumAvailability': 'released', 'titleSlug': movie_title_slug,
                'addOptions': {'ignoreEpisodesWithFiles': False, 'ignoreEpisodesWithoutFiles': False,
                               'searchForMovie': search_missing}
            }

            # make request
            req = requests.post(urljoin(self.server_url, 'api/movie'), json=payload, headers=self.headers, timeout=30)
            log.debug("Request URL: %s", req.url)
            log.debug("Request Payload: %s", payload)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 201 and req.json()['tmdbId'] == movie_tmdbid:
                log.debug("Successfully added %s (%d)", movie_title, movie_tmdbid)
                return True
            elif 'json' in req.headers['Content-Type'].lower() and 'message' in req.text:
                log.error("Failed to add %s (%d) - status_code: %d, reason: %s", movie_title, movie_tmdbid,
                          req.status_code, req.json()['message'])
                return False
            else:
                log.error("Failed to add %s (%d), unexpected response:\n%s", movie_title, movie_tmdbid, req.text)
                return False
        except Exception:
            log.exception("Exception adding movie %s (%d): ", movie_title, movie_tmdbid)
        return None
