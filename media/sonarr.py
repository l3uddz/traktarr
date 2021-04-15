import os.path

import backoff
import requests
from helpers.misc import backoff_handler, dict_merge

from helpers import str as misc_str
from media.pvr import PVR
from misc.log import logger

log = logger.get_logger(__name__)


class Sonarr(PVR):
    def get_objects(self):
        return self._get_objects('api/series')

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_tags(self):
        tags = {}
        try:
            # make request
            req = requests.get(
                os.path.join(misc_str.ensure_endswith(self.server_url, "/"), 'api/tag'),
                headers=self.headers,
                timeout=60,
                allow_redirects=False
            )
            log.debug("Request URL: %s", req.url)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                resp_json = req.json()
                log.debug("Found Sonarr Tags: %d", len(resp_json))
                for tag in resp_json:
                    tags[tag['label']] = tag['id']
                return tags
            else:
                log.error("Failed to retrieve all tags, request response: %d", req.status_code)
        except Exception:
            log.exception("Exception retrieving tags: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def add_series(self, series_tvdb_id, series_title, series_title_slug, quality_profile_id, language_profile_id,
                   root_folder, season_folder=True, tag_ids=None, search_missing=False, series_type='standard'):
        payload = self._prepare_add_object_payload(series_title, series_title_slug, quality_profile_id, root_folder)

        payload = dict_merge(payload, {
            'tvdbId': series_tvdb_id,
            'tags': [] if not tag_ids or not isinstance(tag_ids, list) else tag_ids,
            'seasons': [],
            'seasonFolder': season_folder,
            'seriesType': series_type,
            'addOptions': {
                'searchForMissingEpisodes': search_missing
            }
        })

        if language_profile_id:
            payload['languageProfileId'] = language_profile_id
            endpoint = 'api/v3/series'
        else:
            endpoint = 'api/series'

        return self._add_object(endpoint, payload, identifier_field='tvdbId', identifier=series_tvdb_id)
