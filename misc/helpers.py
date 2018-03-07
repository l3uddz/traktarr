from misc import str as misc_str
from misc.log import logger

log = logger.get_logger(__name__)


############################################################
# SONARR
############################################################

def sonarr_series_tag_id_from_network(profile_tags, network_tags, network):
    try:
        for tag_name, tag_networks in network_tags.items():
            for tag_network in tag_networks:
                if tag_network.lower() in network.lower() and tag_name.lower() in profile_tags:
                    log.debug("Using %s tag for network: %s", tag_name, network)
                    return [profile_tags[tag_name.lower()]]
    except Exception:
        log.exception("Exception determining tag to use for network %s: ", network)
    return None


def sonarr_series_to_tvdb_dict(sonarr_series):
    series = {}
    try:
        for tmp in sonarr_series:
            if 'tvdbId' not in tmp:
                log.debug("Could not handle show: %s", tmp['title'])
                continue
            series[tmp['tvdbId']] = tmp
        return series
    except Exception:
        log.exception("Exception processing Sonarr shows to TVDB dict: ")
    return None


def sonarr_remove_existing_series(sonarr_series, trakt_series):
    new_series_list = []

    if not sonarr_series or not trakt_series:
        log.error("Inappropriate parameters were supplied")
        return None

    try:
        # turn sonarr series result into a dict with tvdb id as keys
        processed_series = sonarr_series_to_tvdb_dict(sonarr_series)
        if not processed_series:
            return None

        # loop list adding to series that do not already exist
        for tmp in trakt_series:
            if 'show' not in tmp or 'ids' not in tmp['show'] or 'tvdb' not in tmp['show']['ids']:
                log.debug("Skipping show because it did not have required fields: %s", tmp)
                continue
            # check if show exists in processed_series
            if tmp['show']['ids']['tvdb'] in processed_series:
                log.debug("Removing existing show: %s", tmp['show']['title'])
                continue

            new_series_list.append(tmp)

        log.debug("Filtered %d Trakt shows to %d shows that weren't already in Sonarr", len(trakt_series),
                  len(new_series_list))
        return new_series_list
    except Exception:
        log.exception("Exception removing existing shows from Trakt list: ")
    return None


def trakt_blacklisted_show_genre(show, genres):
    blacklisted = False
    try:
        if not show['show']['genres']:
            log.debug("%s was blacklisted because it had no genres", show['show']['title'])
            blacklisted = True
        else:
            for genre in genres:
                if genre.lower() in show['show']['genres']:
                    log.debug("%s was blacklisted because it has genre: %s", show['show']['title'], genre)
                    blacklisted = True
                    break

    except Exception:
        log.exception("Exception determining if show has a blacklisted genre %s: ", show)
    return blacklisted


def trakt_blacklisted_show_year(show, earliest_year):
    blacklisted = False
    try:
        year = misc_str.get_year_from_timestamp(show['show']['first_aired'])
        if not year:
            log.debug("%s was blacklisted due to having an unknown first_aired date", show['show']['title'])
            blacklisted = True
        else:
            if year < earliest_year:
                log.debug("%s was blacklisted because it first aired in: %d", show['show']['title'], year)
                blacklisted = True
    except Exception:
        log.exception("Exception determining if show is before earliest_year %s:", show)
    return blacklisted


def trakt_blacklisted_show_country(show, allowed_countries):
    blacklisted = False
    try:
        if not show['show']['country']:
            log.debug("%s was blacklisted because it had no country", show['show']['title'])
            blacklisted = True
        else:
            if show['show']['country'].lower() not in allowed_countries:
                log.debug("%s was blacklisted because it's from country: %s", show['show']['title'],
                          show['show']['country'])
                blacklisted = True

    except Exception:
        log.exception("Exception determining if show was from an allowed country %s: ", show)
    return blacklisted


def trakt_blacklisted_show_network(show, networks):
    blacklisted = False
    try:
        if not show['show']['network']:
            log.debug("%s was blacklisted because it had no network", show['show']['title'])
            blacklisted = True
        else:
            for network in networks:
                if network.lower() in show['show']['network'].lower():
                    log.debug("%s was blacklisted because it's from network: %s", show['show']['title'],
                              show['show']['network'])
                    blacklisted = True
                    break

    except Exception:
        log.exception("Exception determining if show is from a blacklisted network %s: ", show)
    return blacklisted


def trakt_blacklisted_show_runtime(show, lowest_runtime):
    blacklisted = False
    try:
        if not show['show']['runtime'] or not isinstance(show['show']['runtime'], int):
            log.debug("%s was blacklisted because it had no runtime", show['show']['title'])
            blacklisted = True
        elif int(show['show']['runtime']) < lowest_runtime:
            log.debug("%s was blacklisted because it had a runtime of: %d", show['show']['title'],
                      show['show']['runtime'])
            blacklisted = True

    except Exception:
        log.exception("Exception determining if show had sufficient runtime %s: ", show)
    return blacklisted


def trakt_is_show_blacklisted(show, blacklist_settings):
    blacklisted = False
    try:
        if trakt_blacklisted_show_year(show, blacklist_settings.blacklisted_min_year):
            blacklisted = True
        if trakt_blacklisted_show_country(show, blacklist_settings.allowed_countries):
            blacklisted = True
        if trakt_blacklisted_show_genre(show, blacklist_settings.blacklisted_genres):
            blacklisted = True
        if trakt_blacklisted_show_network(show, blacklist_settings.blacklisted_networks):
            blacklisted = True
        if trakt_blacklisted_show_runtime(show, blacklist_settings.blacklisted_min_runtime):
            blacklisted = True
    except Exception:
        log.exception("Exception determining if show was blacklisted %s: ", show)
    return blacklisted


############################################################
# RADARR
############################################################

def radarr_movies_to_tmdb_dict(radarr_movies):
    movies = {}
    try:
        for tmp in radarr_movies:
            if 'tmdbId' not in tmp:
                log.debug("Could not handle movie: %s", tmp['title'])
                continue
            movies[tmp['tmdbId']] = tmp
        return movies
    except Exception:
        log.exception("Exception processing Radarr movies to TMDB dict: ")
    return None


def radarr_remove_existing_movies(radarr_movies, trakt_movies):
    new_movies_list = []

    if not radarr_movies or not trakt_movies:
        log.error("Inappropriate parameters were supplied")
        return None

    try:
        # turn radarr movies result into a dict with tmdb id as keys
        processed_movies = radarr_movies_to_tmdb_dict(radarr_movies)
        if not processed_movies:
            return None

        # loop list adding to movies that do not already exist
        for tmp in trakt_movies:
            if 'movie' not in tmp or 'ids' not in tmp['movie'] or 'tmdb' not in tmp['movie']['ids']:
                log.debug("Skipping movie because it did not have required fields: %s", tmp)
                continue
            # check if movie exists in processed_movies
            if tmp['movie']['ids']['tmdb'] in processed_movies:
                log.debug("Removing existing movie: %s", tmp['movie']['title'])
                continue

            new_movies_list.append(tmp)

        log.debug("Filtered %d Trakt movies to %d movies that weren't already in Radarr", len(trakt_movies),
                  len(new_movies_list))
        return new_movies_list
    except Exception:
        log.exception("Exception removing existing movies from Trakt list: ")
    return None


def trakt_blacklisted_movie_genre(movie, genres):
    blacklisted = False
    try:
        if not movie['movie']['genres']:
            log.debug("%s was blacklisted because it had no genres", movie['movie']['title'])
            blacklisted = True
        else:
            for genre in genres:
                if genre.lower() in movie['movie']['genres']:
                    log.debug("%s was blacklisted because it has genre: %s", movie['movie']['title'], genre)
                    blacklisted = True
                    break

    except Exception:
        log.exception("Exception determining if movie has a blacklisted genre %s: ", movie)
    return blacklisted


def trakt_blacklisted_movie_year(movie, earliest_year):
    blacklisted = False
    try:
        year = movie['movie']['year']
        if year is None or not isinstance(year, int):
            log.debug("%s was blacklisted due to having an unknown year", movie['movie']['title'])
            blacklisted = True
        else:
            if int(year) < earliest_year:
                log.debug("%s was blacklisted because it's year is: %d", movie['movie']['title'], int(year))
                blacklisted = True
    except Exception:
        log.exception("Exception determining if movie is before earliest_year %s:", movie)
    return blacklisted


def trakt_blacklisted_movie_country(movie, allowed_countries):
    blacklisted = False
    try:
        if not movie['movie']['country']:
            log.debug("%s was blacklisted because it had no country", movie['movie']['title'])
            blacklisted = True
        else:
            if movie['movie']['country'].lower() not in allowed_countries:
                log.debug("%s was blacklisted because it's from country: %s", movie['movie']['title'],
                          movie['movie']['country'])
                blacklisted = True

    except Exception:
        log.exception("Exception determining if movie was from an allowed country %s: ", movie)
    return blacklisted


def trakt_blacklisted_movie_title(movie, blacklisted_keywords):
    blacklisted = False
    try:
        if not movie['movie']['title']:
            log.debug("Blacklisted movie because it had no title: %s", movie)
            blacklisted = True
        else:
            for keyword in blacklisted_keywords:
                if keyword.lower() in movie['movie']['title'].lower():
                    log.debug("%s was blacklisted because it had title keyword: %s", movie['movie']['title'], keyword)
                    blacklisted = True
                    break

    except Exception:
        log.exception("Exception determining if movie had a blacklisted title %s: ", movie)
    return blacklisted


def trakt_blacklisted_movie_runtime(movie, lowest_runtime):
    blacklisted = False
    try:
        if not movie['movie']['runtime'] or not isinstance(movie['movie']['runtime'], int):
            log.debug("%s was blacklisted because it had no runtime", movie['movie']['title'])
            blacklisted = True
        elif int(movie['movie']['runtime']) < lowest_runtime:
            log.debug("%s was blacklisted because it had a runtime of: %d", movie['movie']['title'],
                      movie['movie']['runtime'])
            blacklisted = True

    except Exception:
        log.exception("Exception determining if movie had sufficient runtime %s: ", movie)
    return blacklisted


def trakt_is_movie_blacklisted(movie, blacklist_settings):
    blacklisted = False
    try:
        if trakt_blacklisted_movie_title(movie, blacklist_settings.blacklist_title_keywords):
            blacklisted = True
        if trakt_blacklisted_movie_year(movie, blacklist_settings.blacklisted_min_year):
            blacklisted = True
        if trakt_blacklisted_movie_country(movie, blacklist_settings.allowed_countries):
            blacklisted = True
        if trakt_blacklisted_movie_genre(movie, blacklist_settings.blacklisted_genres):
            blacklisted = True
        if trakt_blacklisted_movie_runtime(movie, blacklist_settings.blacklisted_min_runtime):
            blacklisted = True
    except Exception:
        log.exception("Exception determining if movie was blacklisted %s: ", movie)
    return blacklisted
