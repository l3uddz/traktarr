from misc.log import logger

log = logger.get_logger(__name__)


def get_year_from_timestamp(timestamp):
    year = 0
    try:
        if not timestamp:
            return 0

        year = timestamp[:timestamp.index('-')]
    except Exception:
        log.exception("Exception parsing year from %s: ", timestamp)
    return int(year) if str(year).isdigit() else 0
