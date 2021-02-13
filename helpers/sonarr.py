from misc.log import logger

log = logger.get_logger(__name__)


def series_tag_ids_list_builder(profile_tags, config_tags):
    try:
        tag_ids = []
        for tag_name in config_tags:
            if tag_name.lower() in profile_tags:
                log.debug("Validated Tag: %s", tag_name)
                tag_ids.append(profile_tags[tag_name.lower()])
        if tag_ids:
            return tag_ids
    except Exception:
        log.exception("Exception building Tags IDs list")
    return None


def series_tag_names_list_builder(profile_tag_ids, chosen_tag_ids):
    try:
        if not chosen_tag_ids:
            return None

        tags = []
        for tag_name, tag_id in profile_tag_ids.items():
            if tag_id in chosen_tag_ids:
                tags.append(tag_name)
        if tags:
            return tags
    except Exception:
        log.exception("Exception building Tag Names list from Tag IDs %s: ", chosen_tag_ids)
    return None


def filter_trakt_series_list(trakt_series, callback):
    new_series_list = []
    try:
        for tmp in trakt_series:
            if 'show' not in tmp or 'ids' not in tmp['show'] or 'tvdb' not in tmp['show']['ids']:
                log.debug("Removing shows from Trakt list as it did not have the required fields: %s", tmp)
                if callback:
                    callback('movie', tmp)
                continue
            new_series_list.append(tmp)

        return new_series_list
    except Exception:
        log.exception("Exception filtering Trakt shows list: ")
    return None


def series_to_tvdb_dict(sonarr_series):
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


def remove_existing_series_from_trakt_list(sonarr_series, trakt_series, callback=None):
    new_series_list = []

    if not sonarr_series or not trakt_series:
        log.error("Inappropriate parameters were supplied.")
        return None

    try:
        # clean up trakt_series list
        trakt_series = filter_trakt_series_list(trakt_series, callback)
        if not trakt_series:
            return None

        # turn sonarr series result into a dict with tvdb id as keys
        processed_series = series_to_tvdb_dict(sonarr_series)
        if not processed_series:
            return None

        # loop list adding to series that do not already exist
        for tmp in trakt_series:
            # check if show exists in processed_series
            if tmp['show']['ids']['tvdb'] in processed_series:
                show_year = str(tmp['show']['year']) if tmp['show']['year'] else '????'
                log.debug("Removing existing show from Trakt list: \'%s (%s)\'", tmp['show']['title'], show_year)
                if callback:
                    callback('show', tmp)
                continue

            new_series_list.append(tmp)

        series_removed = len(trakt_series) - len(new_series_list)
        log.debug("Filtered %d shows from Trakt list that were already in Sonarr.", series_removed)
        log.debug("New Trakt shows list count: %d", len(new_series_list))
        return new_series_list
    except Exception:
        log.exception("Exception removing existing shows from Trakt list: ")
    return None
