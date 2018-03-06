#!/usr/bin/env python3
import time

import click

from media.radarr import Radarr
from media.sonarr import Sonarr
from media.trakt import Trakt
from misc import helpers
from misc.config import cfg
from misc.log import logger

############################################################
# INIT
############################################################

# Logging
log = logger.get_logger('traktarr')


# Click
@click.group(help='Add new series/movies to Sonarr & Radarr from Trakt.')
def app():
    pass


############################################################
# SHOWS
############################################################

@app.command(help='Add new series to Sonarr.')
@click.option('--list-type', '-t', type=click.Choice(['anticipated', 'trending', 'popular']),
              help='Trakt list to process.', required=True)
@click.option('--add-limit', '-l', default=0, help='Limit number of series added to Sonarr.', show_default=True)
@click.option('--add-delay', '-d', default=2.5, help='Seconds between each add request to Sonarr.', show_default=True)
@click.option('--no-search', is_flag=True, help='Disable search when adding series to Sonarr.')
def shows(list_type, add_limit=0, add_delay=2.5, no_search=False):
    added_shows = 0

    # validate trakt api_key
    trakt = Trakt(cfg.trakt.api_key)
    if not trakt.validate_api_key():
        log.error("Aborting due to failure to validate Trakt API Key")
        return
    else:
        log.info("Validated Trakt API Key")

    # validate sonarr url & api_key
    sonarr = Sonarr(cfg.sonarr.url, cfg.sonarr.api_key)
    if not sonarr.validate_api_key():
        log.error("Aborting due to failure to validate Sonarr URL / API Key")
        return
    else:
        log.info("Validated Sonarr URL & API Key")

    # retrieve profile id for requested profile
    profile_id = sonarr.get_profile_id(cfg.sonarr.profile)
    if not profile_id or not profile_id > 0:
        log.error("Aborting due to failure to retrieve Profile ID for: %s", cfg.sonarr.profile)
        return
    else:
        log.info("Retrieved Profile ID for %s: %d", cfg.sonarr.profile, profile_id)

    # get sonarr series list
    sonarr_series_list = sonarr.get_series()
    if not sonarr_series_list:
        log.error("Aborting due to failure to retrieve Sonarr series list")
        return
    else:
        log.info("Retrieved Sonarr series list, series found: %d", len(sonarr_series_list))

    # get trakt series list
    trakt_series_list = None
    if list_type.lower() == 'anticipated':
        trakt_series_list = trakt.get_anticipated_shows()
    elif list_type.lower() == 'trending':
        trakt_series_list = trakt.get_trending_shows()
    elif list_type.lower() == 'popular':
        trakt_series_list = trakt.get_popular_shows()
    else:
        log.error("Aborting due to unknown Trakt list type")
        return
    if not trakt_series_list:
        log.error("Aborting due to failure to retrieve Trakt %s series list", list_type)
        return
    else:
        log.info("Retrieved Trakt %s series list, series found: %d", list_type, len(trakt_series_list))

    # build filtered series list without series that exist in sonarr
    processed_series_list = helpers.sonarr_remove_existing_series(sonarr_series_list, trakt_series_list)
    if not processed_series_list:
        log.error("Aborting due to failure to remove existing Sonarr series from retrieved Trakt series list")
        return
    else:
        log.info("Removed existing Sonarr series from Trakt series list, series left to process: %d",
                 len(processed_series_list))

    # loop series_list
    log.info("Processing list now...")
    for series in processed_series_list:
        try:
            # check if series passes out blacklist criteria inspection
            if not helpers.trakt_is_show_blacklisted(series, cfg.filters.shows):
                log.info("Adding: %s | Genres: %s | Network: %s | Country: %s", series['show']['title'],
                         ', '.join(series['show']['genres']), series['show']['network'],
                         series['show']['country'].upper())

                # add show to sonarr
                if sonarr.add_series(series['show']['ids']['tvdb'], series['show']['title'], profile_id,
                                     cfg.sonarr.root_folder,
                                     not no_search):
                    log.info("ADDED %s (%d)", series['show']['title'], series['show']['year'])
                    added_shows += 1
                else:
                    log.error("FAILED adding %s (%d)", series['show']['title'], series['show']['year'])

                # stop adding shows, if added_shows >= add_limit
                if add_limit and added_shows >= add_limit:
                    break

                # sleep before adding any more
                time.sleep(add_delay)

        except Exception:
            log.exception("Exception while processing series %s: ", series['show']['title'])

    log.info("Added %d new shows to Sonarr", added_shows)


@app.command(help='Add new movies to Radarr.')
@click.option('--list-type', '-t', type=click.Choice(['anticipated', 'trending', 'popular']),
              help='Trakt list to process.', required=True)
@click.option('--add-limit', '-l', default=0, help='Limit number of movies added to Radarr.', show_default=True)
@click.option('--add-delay', '-d', default=2.5, help='Seconds between each add request to Radarr.', show_default=True)
@click.option('--no-search', is_flag=True, help='Disable search when adding movies to Radarr.')
def movies(list_type, add_limit=0, add_delay=2.5, no_search=False):
    added_movies = 0

    # validate trakt api_key
    trakt = Trakt(cfg.trakt.api_key)
    if not trakt.validate_api_key():
        log.error("Aborting due to failure to validate Trakt API Key")
        return
    else:
        log.info("Validated Trakt API Key")

    # validate radarr url & api_key
    radarr = Radarr(cfg.radarr.url, cfg.radarr.api_key)
    if not radarr.validate_api_key():
        log.error("Aborting due to failure to validate Radarr URL / API Key")
        return
    else:
        log.info("Validated Radarr URL & API Key")

    # retrieve profile id for requested profile
    profile_id = radarr.get_profile_id(cfg.radarr.profile)
    if not profile_id or not profile_id > 0:
        log.error("Aborting due to failure to retrieve Profile ID for: %s", cfg.radarr.profile)
        return
    else:
        log.info("Retrieved Profile ID for %s: %d", cfg.radarr.profile, profile_id)

    # get radarr movies list
    radarr_movie_list = radarr.get_movies()
    if not radarr_movie_list:
        log.error("Aborting due to failure to retrieve Radarr movies list")
        return
    else:
        log.info("Retrieved Radarr movies list, movies found: %d", len(radarr_movie_list))

    # get trakt movies list
    trakt_movies_list = None
    if list_type.lower() == 'anticipated':
        trakt_movies_list = trakt.get_anticipated_movies()
    elif list_type.lower() == 'trending':
        trakt_movies_list = trakt.get_trending_movies()
    elif list_type.lower() == 'popular':
        trakt_movies_list = trakt.get_popular_movies()
    else:
        log.error("Aborting due to unknown Trakt list type")
        return
    if not trakt_movies_list:
        log.error("Aborting due to failure to retrieve Trakt %s movies list", list_type)
        return
    else:
        log.info("Retrieved Trakt %s movies list, movies found: %d", list_type, len(trakt_movies_list))

    # build filtered series list without series that exist in sonarr
    processed_movies_list = helpers.radarr_remove_existing_movies(radarr_movie_list, trakt_movies_list)
    if not processed_movies_list:
        log.error("Aborting due to failure to remove existing Radarr movies from retrieved Trakt movies list")
        return
    else:
        log.info("Removed existing Radarr movies from Trakt movies list, movies left to process: %d",
                 len(processed_movies_list))

    # loop movies
    log.info("Processing list now...")
    for movie in processed_movies_list:
        try:
            # check if movie passes out blacklist criteria inspection
            if not helpers.trakt_is_movie_blacklisted(movie, cfg.filters.movies):
                log.info("Adding: %s (%d) | Genres: %s | Country: %s", movie['movie']['title'], movie['movie']['year'],
                         ', '.join(movie['movie']['genres']), movie['movie']['country'].upper())
                # add movie to radarr
                if radarr.add_movie(movie['movie']['ids']['tmdb'], movie['movie']['title'], movie['movie']['year'],
                                    profile_id, cfg.radarr.root_folder, not no_search):
                    log.info("ADDED %s (%d)", movie['movie']['title'], movie['movie']['year'])
                    added_movies += 1
                else:
                    log.error("FAILED adding %s (%d)", movie['movie']['title'], movie['movie']['year'])

                # stop adding movies, if added_movies >= add_limit
                if add_limit and added_movies >= add_limit:
                    break

                # sleep before adding any more
                time.sleep(add_delay)

        except Exception:
            log.exception("Exception while processing movie %s: ", movie['movie']['title'])

    log.info("Added %d new movies to Radarr", added_movies)


############################################################
# MAIN
############################################################

if __name__ == "__main__":
    app()
