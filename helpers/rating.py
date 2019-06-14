from misc.log import logger
import json
import requests

log = logger.get_logger(__name__)


def get_rating(apikey, movie):

    imdb_id = movie['movie']['ids']['imdb']
    if imdb_id:
        log.debug("Requesting info from OMDB for %s (%d) | Genres: %s | Country: %s | IMDB ID: %s",
                  movie['movie']['title'], movie['movie']['year'], ', '.join(movie['movie']['genres']),
                  (movie['movie']['country'] or 'N/A').upper(), imdb_id)
        r = requests.get('http://www.omdbapi.com/?i=' + imdb_id + '&apikey=' + apikey)
        if r.status_code == 200 and json.loads(r.text)["Response"] == 'True':
            log.debug("Successfully requested ratings from OMDB for %s (%d) | Genres: %s | Country: %s | IMDB ID: %s",
                      movie['movie']['title'], movie['movie']['year'],
                      ', '.join(movie['movie']['genres']), (movie['movie']['country'] or 'N/A').upper(), imdb_id)
            for source in json.loads(r.text)["Ratings"]:
                if source['Source'] == 'Rotten Tomatoes':
                    log.debug("Rotten Tomatoes score of %s for %s (%d) | Genres: %s | Country: %s | IMDB ID: %s ",
                              source['Value'], movie['movie']['title'], movie['movie']['year'],
                              ', '.join(movie['movie']['genres']), (movie['movie']['country'] or 'N/A').upper(),
                              imdb_id)
                    return int(source['Value'].split('%')[0])
        else:
            log.debug("Error encountered when requesting ratings from OMDB for %s (%d) | Genres: %s | Country: %s" +
                      " | IMDB ID: %s", movie['movie']['title'], movie['movie']['year'],
                      ', '.join(movie['movie']['genres']), (movie['movie']['country'] or 'N/A').upper(), imdb_id)
    else:
        log.debug("Skipping %s (%d) | Genres: %s | Country: %s as it does not have an IMDB ID",
                  movie['movie']['title'], movie['movie']['year'], ', '.join(movie['movie']['genres']),
                  (movie['movie']['country'] or 'N/A').upper())

    return -1
