#!/usr/bin/env python3
import os.path
import sys
import time

import click
import schedule

############################################################
# INIT
############################################################
cfg = None
log = None
notify = None


# Click
@click.group(help='Add new shows & movies to Sonarr/Radarr from Trakt lists.')
@click.version_option('1.1.3', prog_name='traktarr')
@click.option(
    '--config',
    envvar='TRAKTARR_CONFIG',
    type=click.Path(file_okay=True, dir_okay=False),
    help='Configuration file',
    show_default=True,
    default=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "config.json")
)
@click.option(
    '--logfile',
    envvar='TRAKTARR_LOGFILE',
    type=click.Path(file_okay=True, dir_okay=False),
    help='Log file',
    show_default=True,
    default=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "activity.log")
)
def app(config, logfile):
    # Setup global variables
    global cfg, log, notify

    # Load config
    from misc.config import Config
    cfg = Config(config_path=config, logfile=logfile).cfg

    # Load logger
    from misc.log import logger
    log = logger.get_logger('traktarr')

    # Load notifications
    from notifications import Notifications
    notify = Notifications()

    # Notifications
    init_notifications()


############################################################
# SHOWS
############################################################

@app.command(help='Add new shows to Sonarr.')
@click.option('--list-type', '-t', type=click.Choice(['anticipated', 'trending', 'popular']),
              help='Trakt list to process.', required=True)
@click.option('--add-limit', '-l', default=0, help='Limit number of shows added to Sonarr.', show_default=True)
@click.option('--add-delay', '-d', default=2.5, help='Seconds between each add request to Sonarr.', show_default=True)
@click.option('--genre', '-g', default=None, help='Only add shows from this genre to Sonarr.')
@click.option('--folder', '-f', default=None, help='Add shows with this root folder to Sonarr.')
@click.option('--no-search', is_flag=True, help='Disable search when adding shows to Sonarr.')
@click.option('--notifications', is_flag=True, help='Send notifications.')
def shows(list_type, add_limit=0, add_delay=2.5, genre=None, folder=None, no_search=False, notifications=False):
    from media.sonarr import Sonarr
    from media.trakt import Trakt
    from misc import helpers

    added_shows = 0

    # remove genre from shows blacklisted_genres if supplied
    if genre and genre in cfg.filters.shows.blacklisted_genres:
        cfg['filters']['shows']['blacklisted_genres'].remove(genre)

    # replace sonarr root_folder if folder is supplied
    if folder:
        cfg['sonarr']['root_folder'] = folder

    # validate trakt api_key
    trakt = Trakt(cfg.trakt.api_key)
    if not trakt.validate_api_key():
        log.error("Aborting due to failure to validate Trakt API Key")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': 'Failure to validate Trakt API Key'})
        return None
    else:
        log.info("Validated Trakt API Key")

    # validate sonarr url & api_key
    sonarr = Sonarr(cfg.sonarr.url, cfg.sonarr.api_key)
    if not sonarr.validate_api_key():
        log.error("Aborting due to failure to validate Sonarr URL / API Key")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': 'Failure to validate Sonarr URL / API Key'})
        return None
    else:
        log.info("Validated Sonarr URL & API Key")

    # retrieve profile id for requested profile
    profile_id = sonarr.get_profile_id(cfg.sonarr.profile)
    if not profile_id or not profile_id > 0:
        log.error("Aborting due to failure to retrieve Profile ID for: %s", cfg.sonarr.profile)
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': 'Failure to retrieve Sonarr Profile ID of %s' % cfg.sonarr.profile})
        return None
    else:
        log.info("Retrieved Profile ID for %s: %d", cfg.sonarr.profile, profile_id)

    # retrieve profile tags
    profile_tags = sonarr.get_tags()
    if profile_tags is None:
        log.error("Aborting due to failure to retrieve Tag ID's")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': "Failure to retrieve Sonarr Tag ID's"})
        return None
    else:
        log.info("Retrieved %d Tag ID's", len(profile_tags))

    # get sonarr series list
    sonarr_series_list = sonarr.get_series()
    if not sonarr_series_list:
        log.error("Aborting due to failure to retrieve Sonarr shows list")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': 'Failure to retrieve Sonarr shows list'})
        return None
    else:
        log.info("Retrieved Sonarr shows list, shows found: %d", len(sonarr_series_list))

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
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': 'Failure to determine Trakt list type'})
        return None
    if not trakt_series_list:
        log.error("Aborting due to failure to retrieve Trakt %s shows list", list_type)
        if notifications:
            callback_notify(
                {'event': 'abort', 'type': 'shows', 'list_type': list_type,
                 'reason': 'Failure to retrieve Trakt %s shows list' % list_type})
        return None
    else:
        log.info("Retrieved Trakt %s shows list, shows found: %d", list_type, len(trakt_series_list))

    # build filtered series list without series that exist in sonarr
    processed_series_list = helpers.sonarr_remove_existing_series(sonarr_series_list, trakt_series_list)
    if processed_series_list is None:
        log.error("Aborting due to failure to remove existing Sonarr shows from retrieved Trakt shows list")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'shows', 'list_type': list_type,
                             'reason': 'Failure to remove existing Sonarr shows from retrieved Trakt %s shows list' % list_type
                             })
        return None
    else:
        log.info("Removed existing Sonarr shows from Trakt shows list, shows left to process: %d",
                 len(processed_series_list))

    # sort filtered series list by highest votes
    sorted_series_list = sorted(processed_series_list, key=lambda k: k['show']['votes'], reverse=True)
    log.info("Sorted shows list to process by highest votes")

    # loop series_list
    log.info("Processing list now...")
    for series in sorted_series_list:
        try:
            # check if genre matches genre supplied via argument
            if genre and genre.lower() not in series['show']['genres']:
                log.debug("Skipping: %s because it was not from %s genre", series['show']['title'], genre.lower())
                continue

            # check if series passes out blacklist criteria inspection
            if not helpers.trakt_is_show_blacklisted(series, cfg.filters.shows):
                log.info("Adding: %s | Genres: %s | Network: %s | Country: %s", series['show']['title'],
                         ', '.join(series['show']['genres']), series['show']['network'],
                         series['show']['country'].upper())

                # determine which tags to use when adding this series
                use_tags = helpers.sonarr_series_tag_id_from_network(profile_tags, cfg.sonarr.tags,
                                                                     series['show']['network'])
                # add show to sonarr
                if sonarr.add_series(series['show']['ids']['tvdb'], series['show']['title'],
                                     series['show']['ids']['slug'], profile_id, cfg.sonarr.root_folder, use_tags,
                                     not no_search):
                    log.info("ADDED %s (%d) with tags: %s", series['show']['title'], series['show']['year'],
                             helpers.sonarr_readable_tag_from_ids(profile_tags, use_tags))
                    if notifications:
                        callback_notify({'event': 'add_show', 'list_type': list_type, 'show': series['show']})
                    added_shows += 1
                else:
                    log.error("FAILED adding %s (%d) with tags: %s", series['show']['title'], series['show']['year'],
                              helpers.sonarr_readable_tag_from_ids(profile_tags, use_tags))

                # stop adding shows, if added_shows >= add_limit
                if add_limit and added_shows >= add_limit:
                    break

                # sleep before adding any more
                time.sleep(add_delay)

        except Exception:
            log.exception("Exception while processing show %s: ", series['show']['title'])

    log.info("Added %d new show(s) to Sonarr", added_shows)

    # send notification
    if notifications:
        notify.send(message="Added %d shows from Trakt's %s list" % (added_shows, list_type))

    return added_shows


############################################################
# MOVIES
############################################################

@app.command(help='Add new movies to Radarr.')
@click.option('--list-type', '-t', type=click.Choice(['anticipated', 'trending', 'popular', 'boxoffice']),
              help='Trakt list to process.', required=True)
@click.option('--add-limit', '-l', default=0, help='Limit number of movies added to Radarr.', show_default=True)
@click.option('--add-delay', '-d', default=2.5, help='Seconds between each add request to Radarr.', show_default=True)
@click.option('--genre', '-g', default=None, help='Only add movies from this genre to Radarr.')
@click.option('--folder', '-f', default=None, help='Add movies with this root folder to Radarr.')
@click.option('--no-search', is_flag=True, help='Disable search when adding movies to Radarr.')
@click.option('--notifications', is_flag=True, help='Send notifications.')
def movies(list_type, add_limit=0, add_delay=2.5, genre=None, folder=None, no_search=False, notifications=False):
    from media.radarr import Radarr
    from media.trakt import Trakt
    from misc import helpers

    added_movies = 0

    # remove genre from movies blacklisted_genres if supplied
    if genre and genre in cfg.filters.movies.blacklisted_genres:
        cfg['filters']['movies']['blacklisted_genres'].remove(genre)

    # replace radarr root_folder if folder is supplied
    if folder:
        cfg['radarr']['root_folder'] = folder

    # validate trakt api_key
    trakt = Trakt(cfg.trakt.api_key)
    if not trakt.validate_api_key():
        log.error("Aborting due to failure to validate Trakt API Key")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'movies', 'list_type': list_type,
                             'reason': 'Failure to validate Trakt API Key'})
        return None
    else:
        log.info("Validated Trakt API Key")

    # validate radarr url & api_key
    radarr = Radarr(cfg.radarr.url, cfg.radarr.api_key)
    if not radarr.validate_api_key():
        log.error("Aborting due to failure to validate Radarr URL / API Key")
        if notifications:
            callback_notify(
                {'event': 'abort', 'type': 'movies', 'list_type': list_type,
                 'reason': 'Failure to validate Radarr URL / API Key'})
        return None
    else:
        log.info("Validated Radarr URL & API Key")

    # retrieve profile id for requested profile
    profile_id = radarr.get_profile_id(cfg.radarr.profile)
    if not profile_id or not profile_id > 0:
        log.error("Aborting due to failure to retrieve Profile ID for: %s", cfg.radarr.profile)
        if notifications:
            callback_notify({'event': 'abort', 'type': 'movies', 'list_type': list_type,
                             'reason': 'Failure to retrieve Radarr Profile ID of %s' % cfg.radarr.profile})
        return None
    else:
        log.info("Retrieved Profile ID for %s: %d", cfg.radarr.profile, profile_id)

    # get radarr movies list
    radarr_movie_list = radarr.get_movies()
    if not radarr_movie_list:
        log.error("Aborting due to failure to retrieve Radarr movies list")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'movies', 'list_type': list_type,
                             'reason': 'Failure to retrieve Radarr movies list'})
        return None
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
    elif list_type.lower() == 'boxoffice':
        trakt_movies_list = trakt.get_boxoffice_movies()
    else:
        log.error("Aborting due to unknown Trakt list type")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'movies', 'list_type': list_type,
                             'reason': 'Failure to determine Trakt list type'})
        return None
    if not trakt_movies_list:
        log.error("Aborting due to failure to retrieve Trakt %s movies list", list_type)
        if notifications:
            callback_notify(
                {'event': 'abort', 'type': 'movies', 'list_type': list_type,
                 'reason': 'Failure to retrieve Trakt %s movies list' % list_type})
        return None
    else:
        log.info("Retrieved Trakt %s movies list, movies found: %d", list_type, len(trakt_movies_list))

    # build filtered movie list without movies that exist in radarr
    processed_movies_list = helpers.radarr_remove_existing_movies(radarr_movie_list, trakt_movies_list)
    if processed_movies_list is None:
        log.error("Aborting due to failure to remove existing Radarr movies from retrieved Trakt movies list")
        if notifications:
            callback_notify({'event': 'abort', 'type': 'movies', 'list_type': list_type,
                             'reason': 'Failure to remove existing Radarr movies from retrieved '
                                       'Trakt %s movies list' % list_type})
        return None
    else:
        log.info("Removed existing Radarr movies from Trakt movies list, movies left to process: %d",
                 len(processed_movies_list))

    # sort filtered movie list by highest votes
    sorted_movies_list = sorted(processed_movies_list, key=lambda k: k['movie']['votes'], reverse=True)
    log.info("Sorted movie list to process by highest votes")

    # loop movies
    log.info("Processing list now...")
    for movie in sorted_movies_list:
        try:
            # check if genre matches genre supplied via argument
            if genre and genre.lower() not in movie['movie']['genres']:
                log.debug("Skipping: %s because it was not from %s genre", movie['movie']['title'], genre.lower())
                continue

            # check if movie passes out blacklist criteria inspection
            if not helpers.trakt_is_movie_blacklisted(movie, cfg.filters.movies):
                log.info("Adding: %s (%d) | Genres: %s | Country: %s", movie['movie']['title'], movie['movie']['year'],
                         ', '.join(movie['movie']['genres']), movie['movie']['country'].upper())
                # add movie to radarr
                if radarr.add_movie(movie['movie']['ids']['tmdb'], movie['movie']['title'], movie['movie']['year'],
                                    movie['movie']['ids']['slug'], profile_id, cfg.radarr.root_folder, not no_search):
                    log.info("ADDED %s (%d)", movie['movie']['title'], movie['movie']['year'])
                    if notifications:
                        callback_notify({'event': 'add_movie', 'list_type': list_type, 'movie': movie['movie']})
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

    log.info("Added %d new movie(s) to Radarr", added_movies)

    # send notification
    if notifications:
        notify.send(message="Added %d movies from Trakt's %s list" % (added_movies, list_type))

    return added_movies


############################################################
# AUTOMATIC
############################################################

def callback_notify(data):
    log.debug("Received callback data: %s", data)

    # handle event
    if data['event'] == 'add_movie':
        if cfg.notifications.verbose:
            notify.send(
                message="Added %s movie: %s (%d)" % (data['list_type'], data['movie']['title'], data['movie']['year']))
        return
    elif data['event'] == 'add_show':
        if cfg.notifications.verbose:
            notify.send(
                message="Added %s show: %s (%d)" % (data['list_type'], data['show']['title'], data['show']['year']))
        return
    elif data['event'] == 'abort':
        notify.send(message="Aborted adding Trakt %s %s due to: %s" % (data['list_type'], data['type'], data['reason']))
        return
    else:
        log.error("Unexpected callback: %s", data)
    return


def automatic_shows(add_delay=2.5, no_search=False, notifications=False):
    total_shows_added = 0
    try:
        log.info("Started")

        for list_type, type_amount in cfg.automatic.shows.items():
            if list_type.lower() == 'interval':
                continue
            elif type_amount <= 0:
                log.info("Skipped Trakt's %s shows list", list_type)
                continue
            else:
                log.info("Adding %d shows from Trakt's %s list", type_amount, list_type)

            # run shows
            added_shows = shows.callback(list_type=list_type, add_limit=type_amount,
                                         add_delay=add_delay, no_search=no_search,
                                         notifications=notifications)
            if added_shows is None:
                log.error("Failed adding shows from Trakt's %s list", list_type)
                time.sleep(10)
                continue
            total_shows_added += added_shows

            # sleep
            time.sleep(10)

        log.info("Finished, added %d shows total to Sonarr!", total_shows_added)
        # send notification
        if notifications:
            notify.send(message="Added %d shows total to Sonarr!" % total_shows_added)

    except Exception:
        log.exception("Exception while automatically adding shows: ")
    return


def automatic_movies(add_delay=2.5, no_search=False, notifications=False):
    total_movies_added = 0
    try:
        log.info("Started")

        for list_type, type_amount in cfg.automatic.movies.items():
            if list_type.lower() == 'interval':
                continue
            elif type_amount <= 0:
                log.info("Skipped Trakt's %s movies list", list_type)
                continue
            else:
                log.info("Adding %d movies from Trakt's %s list", type_amount, list_type)

            # run movies
            added_movies = movies.callback(list_type=list_type, add_limit=type_amount,
                                           add_delay=add_delay, no_search=no_search,
                                           notifications=notifications)
            if added_movies is None:
                log.error("Failed adding movies from Trakt's %s list", list_type)
                time.sleep(10)
                continue
            total_movies_added += added_movies

            # sleep
            time.sleep(10)

        log.info("Finished, added %d movies total to Radarr!", total_movies_added)
        # send notification
        if notifications:
            notify.send(message="Added %d movies total to Radarr!" % total_movies_added)

    except Exception:
        log.exception("Exception while automatically adding movies: ")
    return


@app.command(help='Run in automatic mode.')
@click.option('--add-delay', '-d', default=2.5, help='Seconds between each add request to Sonarr / Radarr.',
              show_default=True)
@click.option('--no-search', is_flag=True, help='Disable search when adding to Sonarr / Radarr.')
@click.option('--no-notifications', is_flag=True, help="Disable notifications.")
def run(add_delay=2.5, no_search=False, no_notifications=False):
    log.info("Automatic mode is now running...")

    # Add tasks to schedule and do first run
    if cfg.automatic.movies.interval:
        schedule.every(cfg.automatic.movies.interval).hours.do(
            automatic_movies,
            add_delay,
            no_search,
            not no_notifications
        ).run()
        # Sleep between tasks
        time.sleep(add_delay)

    if cfg.automatic.shows.interval:
        schedule.every(cfg.automatic.shows.interval).hours.do(
            automatic_shows,
            add_delay,
            no_search,
            not no_notifications
        ).run()

    # Enter running schedule
    while True:
        try:
            # Sleep until next run
            log.info("Next job at %s", schedule.next_run())
            time.sleep(schedule.idle_seconds() or 0)
            # Check jobs to run
            schedule.run_pending()

        except Exception as e:
            log.exception("Unhandled exception occurred while processing scheduled tasks: %s", e)
            time.sleep(1)


############################################################
# MISC
############################################################

def init_notifications():
    try:
        for notification_name, notification_config in cfg.notifications.items():
            if notification_name.lower() == 'verbose':
                continue

            notify.load(**notification_config)
    except Exception:
        log.exception("Exception initializing notification agents: ")
    return


############################################################
# MAIN
############################################################

if __name__ == "__main__":
    app()
