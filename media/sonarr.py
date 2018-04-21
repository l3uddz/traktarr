import os.path

import backoff
import requests

from misc import helpers
from misc import str as misc_str
from misc.log import logger

log = logger.get_logger(__name__)


def backoff_handler(details):
    log.warning("Backing off {wait:0.1f} seconds afters {tries} tries "
                "calling function {target} with args {args} and kwargs "
                "{kwargs}".format(**details))


class Sonarr:
    def __init__(self, server_url, api_key):
        self.server_url = server_url
        self.api_key = api_key
        self.headers = {
            'X-Api-Key': self.api_key,
        }

    def validate_api_key(self):
        try:
            # request system status to validate api_key
            req = requests.get(os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/system/status'),
                               headers=self.headers, timeout=60)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200 and 'version' in req.json():
                return True
            return False
        except Exception:
            log.exception("Exception validating api_key: ")
        return False

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_series(self):
        try:
            # make request
            req = requests.get(
                os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/series'),
                headers=self.headers,
                timeout=60
            )
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                log.debug("Found %d shows", len(resp_json))
                return resp_json
            else:
                log.error("Failed to retrieve all shows, request response: %d", req.status_code)
        except Exception:
            log.exception("Exception retrieving show: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_profile_id(self, profile_name):
        try:
            # make request
            req = requests.get(
                os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/profile'),
                headers=self.headers,
                timeout=60
            )
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                log.debug("Found %d quality profiles", len(resp_json))
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
    def get_tag_id(self, tag_name):
        try:
            # make request
            req = requests.get(
                os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/tag'),
                headers=self.headers,
                timeout=60
            )
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                log.debug("Found %d tags", len(resp_json))
                for tag in resp_json:
                    if tag['label'].lower() == tag_name.lower():
                        log.debug("Found id of %s tag: %d", tag_name, tag['id'])
                        return tag['id']
                    log.debug("Tag %s with id %d did not match %s", tag['label'], tag['id'], tag_name)
            else:
                log.error("Failed to retrieve all tags, request response: %d", req.status_code)
        except Exception:
            log.exception("Exception retrieving id of tag %s: ", tag_name)
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_tags(self):
        tags = {}
        try:
            # make request
            req = requests.get(
                os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/tag'),
                headers=self.headers,
                timeout=60
            )
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                log.debug("Found %d tags", len(resp_json))
                for tag in resp_json:
                    tags[tag['label']] = tag['id']
                return tags
            else:
                log.error("Failed to retrieve all tags, request response: %d", req.status_code)
        except Exception:
            log.exception("Exception retrieving tags: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def add_series(self, series_tvdbid, series_title, series_title_slug, profile_id, root_folder, tag_ids=None,
                   search_missing=False):
        try:
            # generate payload
            payload = {
                'tvdbId': series_tvdbid,
                'title': series_title,
                'titleSlug': series_title_slug,
                'qualityProfileId': profile_id,
                'tags': [] if not tag_ids or not isinstance(tag_ids, list) else tag_ids,
                'images': [],
                'seasons': [],
                'seasonFolder': True,
                'monitored': True,
                'rootFolderPath': root_folder,
                'addOptions': {
                    'ignoreEpisodesWithFiles': False,
                    'ignoreEpisodesWithoutFiles': False,
                    'searchForMissingEpisodes': search_missing
                }
            }

            # make request
            req = requests.post(
                os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/series'),
                headers=self.headers,
                json=payload,
                timeout=60
            )
            log.debug("Request URL: %s", req.url)
            log.debug("Request Payload: %s", payload)
            log.debug("Request Response Code: %d", req.status_code)
            log.debug("Request Response Text:\n%s", req.text)

            response_json = None
            if 'json' in req.headers['Content-Type'].lower():
                response_json = helpers.get_response_dict(req.json(), 'tvdbId', series_tvdbid)

            if (req.status_code == 201 or req.status_code == 200) and (response_json and 'tvdbId' in response_json) \
                    and response_json['tvdbId'] == series_tvdbid:
                log.debug("Successfully added %s (%d)", series_title, series_tvdbid)
                return True
            elif response_json and 'errorMessage' in response_json:
                log.error("Failed to add %s (%d) - status_code: %d, reason: %s", series_title, series_tvdbid,
                          req.status_code, response_json['errorMessage'])
                return False
            else:
                log.error("Failed to add %s (%d), unexpected response:\n%s", series_title, series_tvdbid, req.text)
                return False
        except Exception:
            log.exception("Exception adding show %s (%d): ", series_title, series_tvdbid)
        return None
