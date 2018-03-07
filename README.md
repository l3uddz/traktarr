# Traktarr
Script to add new TV series & movies to Sonarr/Radarr based on Trakt lists.

# Requirements
1. Python 3.5 or higher (`sudo apt install python3 python3-pip`).
2. requirements.txt modules (see below).

# Installation on Ubuntu/Debian

1. `cd /opt`
3. `sudo git clone https://github.com/l3uddz/traktarr`
4. `sudo chown -R user:group traktarr` (run `id` to find your user / group)
5. `cd traktarr`
6. `sudo python3 -m pip install -r requirements.txt`
7. `python3 traktarr.py` to generate a default a config.json file.
8. Edit `config.json` to your preference.


# Configuration

```
{
  "core": {
    "debug": false
  },
  "filters": {
    "movies": {
      "allowed_countries": [
        "us",
        "gb",
        "ca"
      ],
      "blacklist_title_keywords": [
        "untitled",
        "barbie"
      ],
      "blacklisted_genres": [
        "documentary",
        "music"
      ],
      "blacklisted_min_runtime": 60,
      "blacklisted_min_year": 2000
    },
    "shows": {
      "allowed_countries": [
        "us",
        "gb",
        "ca"
      ],
      "blacklisted_genres": [
        "animation",
        "game-show",
        "talk-show",
        "home-and-garden",
        "children",
        "reality",
        "anime",
        "news",
        "documentary",
        "special-interest"
      ],
      "blacklisted_min_runtime": 15,
      "blacklisted_min_year": 2000,
      "blacklisted_networks": [
        "twitch",
        "youtube",
        "nickelodeon",
        "hallmark",
        "reelzchannel",
        "disney",
        "cnn",
        "cbbc",
        "the movie network",
        "teletoon",
        "cartoon network",
        "espn",
        "yahoo!",
        "fox sports"
      ]
    }
  },
  "radarr": {
    "api_key": "",
    "profile": "HD-1080p",
    "root_folder": "/movies/",
    "url": "http://localhost:7878"
  },
  "sonarr": {
    "api_key": "",
    "profile": "HD-1080p",
    "root_folder": "/tv/",
    "url": "http://localhost:8989"
  },
  "trakt": {
    "api_key": ""
  }
}
```


# Usage

## Help

```
Usage: python3 traktarr.py movies --help
Usage: python3 traktarr.py shows --help
```


## Movies

```
Usage: python3 traktarr.py movies [OPTIONS]

  Add new movies to Radarr.

Options:
  -t, --list-type [anticipated|trending|popular]
                                  Trakt list to process.  [required]
  -l, --add-limit INTEGER         Limit number of movies added to Radarr.
                                  [default: 0]
  -d, --add-delay FLOAT           Seconds between each add request to Radarr.
                                  [default: 2.5]
  --no-search                     Disable search when adding movies to Radarr.
  --help                          Show this message and exit.
```


## TV Shows

```
Usage: python3 traktarr.py shows [OPTIONS]

  Add new series to Sonarr.

Options:
  -t, --list-type [anticipated|trending|popular]
                                  Trakt list to process.  [required]
  -l, --add-limit INTEGER         Limit number of series added to Sonarr.
                                  [default: 0]
  -d, --add-delay FLOAT           Seconds between each add request to Sonarr.
                                  [default: 2.5]
  --no-search                     Disable search when adding series to Sonarr.
  --help                          Show this message and exit.
```

## Example

```
python3 traktarr.py movies -t anticipated -l 10

```

```
python3 traktarr.py movies -t popular -l 2
```
