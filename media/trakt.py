import backoff
import requests

from misc.log import logger

log = logger.get_logger(__name__)


def backoff_handler(details):
    log.warning("Backing off {wait:0.1f} seconds afters {tries} tries "
                "calling function {target} with args {args} and kwargs "
                "{kwargs}".format(**details))


class Trakt:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'trakt-api-version': '2',
            'trakt-api-key': self.api_key
        }

    def validate_api_key(self):
        try:
            # request trending shows to determine if api_key is valid
            payload = {'extended': 'full', 'limit': 1000}

            # make request
            req = requests.get('https://api.trakt.tv/shows/anticipated', params=payload, headers=self.headers,
                               timeout=30)
            log.debug("Request Response: %d", req.status_code)

            if req.status_code == 200:
                return True
            return False
        except Exception:
            log.exception("Exception validating api_key: ")
        return False

    ############################################################
    # Shows
    ############################################################

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_anticipated_shows(self, limit=1000, languages=None):
        try:
            processed_shows = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/shows/anticipated', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    for show in resp_json:
                        if show not in processed_shows:
                            processed_shows.append(show)

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve anticipated shows, request response: %d", req.status_code)
                    break

            if len(processed_shows):
                log.debug("Found %d anticipated shows", len(processed_shows))
                return processed_shows
            return None
        except Exception:
            log.exception("Exception retrieving anticipated shows: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_trending_shows(self, limit=1000, languages=None):
        try:
            processed_shows = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/shows/trending', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    for show in resp_json:
                        if show not in processed_shows:
                            processed_shows.append(show)

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve trending shows, request response: %d", req.status_code)
                    break

            if len(processed_shows):
                log.debug("Found %d trending shows", len(processed_shows))
                return processed_shows
            return None
        except Exception:
            log.exception("Exception retrieving trending shows: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_popular_shows(self, limit=1000, languages=None):
        try:
            processed_shows = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/shows/popular', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    # process list so it conforms to standard we expect ( e.g. {"show": {.....}} )
                    for show in resp_json:
                        if show not in processed_shows:
                            processed_shows.append({'show': show})

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve popular shows, request response: %d", req.status_code)
                    break

            if len(processed_shows):
                log.debug("Found %d popular shows", len(processed_shows))
                return processed_shows
            return None
        except Exception:
            log.exception("Exception retrieving popular shows: ")
        return None

    ############################################################
    # Movies
    ############################################################

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_anticipated_movies(self, limit=1000, languages=None):
        try:
            processed_movies = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/movies/anticipated', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    for movie in resp_json:
                        if movie not in processed_movies:
                            processed_movies.append(movie)

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve anticipated movies, request response: %d", req.status_code)
                    break

            if len(processed_movies):
                log.debug("Found %d anticipated movies", len(processed_movies))
                return processed_movies
            return None
        except Exception:
            log.exception("Exception retrieving anticipated movies: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_trending_movies(self, limit=1000, languages=None):
        try:
            processed_movies = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/movies/trending', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    for movie in resp_json:
                        if movie not in processed_movies:
                            processed_movies.append(movie)

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve trending movies, request response: %d", req.status_code)
                    break

            if len(processed_movies):
                log.debug("Found %d trending movies", len(processed_movies))
                return processed_movies
            return None
        except Exception:
            log.exception("Exception retrieving trending movies: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_popular_movies(self, limit=1000, languages=None):
        try:
            processed_movies = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/movies/popular', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    # process list so it conforms to standard we expect ( e.g. {"movie": {.....}} )
                    for movie in resp_json:
                        if movie not in processed_movies:
                            processed_movies.append({'movie': movie})

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve popular movies, request response: %d", req.status_code)
                    break

            if len(processed_movies):
                log.debug("Found %d popular movies", len(processed_movies))
                return processed_movies
            return None
        except Exception:
            log.exception("Exception retrieving popular movies: ")
        return None

    @backoff.on_predicate(backoff.expo, lambda x: x is None, max_tries=4, on_backoff=backoff_handler)
    def get_boxoffice_movies(self, limit=1000, languages=None):
        try:
            processed_movies = []

            if languages is None:
                languages = ['en']

            # generate payload
            payload = {'extended': 'full', 'limit': limit, 'page': 1}
            if languages:
                payload['languages'] = ','.join(languages)

            # make request
            while True:
                req = requests.get('https://api.trakt.tv/movies/boxoffice', params=payload, headers=self.headers,
                                   timeout=30)
                log.debug("Request URL: %s", req.url)
                log.debug("Request Payload: %s", payload)
                log.debug("Response Code: %d", req.status_code)
                log.debug("Response Page: %d of %d", payload['page'],
                          0 if 'X-Pagination-Page-Count' not in req.headers else int(
                              req.headers['X-Pagination-Page-Count']))

                if req.status_code == 200:
                    resp_json = req.json()

                    for movie in resp_json:
                        if movie not in processed_movies:
                            processed_movies.append(movie)

                    # check if we have fetched the last page, break if so
                    if 'X-Pagination-Page-Count' not in req.headers or not int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There was no more pages to retrieve")
                        break
                    elif payload['page'] >= int(req.headers['X-Pagination-Page-Count']):
                        log.debug("There are no more pages to retrieve results from")
                        break
                    else:
                        log.info("There are %d pages left to retrieve results from",
                                 int(req.headers['X-Pagination-Page-Count']) - payload['page'])
                        payload['page'] += 1

                else:
                    log.error("Failed to retrieve boxoffice movies, request response: %d", req.status_code)
                    break

            if len(processed_movies):
                log.debug("Found %d boxoffice movies", len(processed_movies))
                return processed_movies
            return None
        except Exception:
            log.exception("Exception retrieving boxoffice movies: ")
        return None
