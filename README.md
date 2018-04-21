# Traktarr
Script to add new shows & movies to Sonarr/Radarr based on Trakt lists.

Trakt lists currently supported:
- anticipated
- boxoffice
- interval
- popular
- trending

# Requirements

1. Python 3.5 or higher (`sudo apt install python3 python3-pip`).
2. requirements.txt modules (see below).

# Installation

## 1. Base Install

Install Traktarr to be run with `traktarr` command.

1. `cd /opt`
2. `sudo git clone https://github.com/l3uddz/traktarr`
3. `sudo chown -R user:group traktarr` (run `id` to find your user / group)
4. `cd traktarr`
5. `sudo python3 -m pip install -r requirements.txt`
6. `sudo ln -s /opt/traktarr/traktarr.py /usr/local/bin/traktarr`
7. `traktarr` - run once to generate a default a config.json file.
8. `nano config.json` - edit preferences.

## 2. Setup Schedule

To have Traktarr get Movies and Shows for you automatically, on set interval.

1. `sudo cp /opt/traktarr/systemd/traktarr.service /etc/systemd/system/`
2. `sudo systemctl daemon-reload`
3. `sudo systemctl enable traktarr.service`
4. `sudo systemctl start traktarr.service`



# Configuration

```json
{
  "core": {
    "debug": false
  },
  "automatic": {
    "movies": {
      "anticipated": 3,
      "boxoffice": 10,
      "interval": 24,
      "popular": 3,
      "trending": 2
    },
    "shows": {
      "anticipated": 10,
      "interval": 48,
      "popular": 1,
      "trending": 2
    }
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
        "music",
        "animation"
      ],
      "blacklisted_max_year": 2019,
      "blacklisted_min_runtime": 60,
      "blacklisted_min_year": 2000,
      "blacklisted_tmdb_ids": []
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
      "blacklisted_max_year": 2019,
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
      ],
      "blacklisted_tvdb_ids": []
    }
  },
  "notifications": {
    "pushover": {
      "service": "pushover",
      "app_token": "",
      "user_token": ""
    },
    "slack": {
      "service": "slack",
      "webhook_url": ""
    },
    "verbose": true,
  },
  "radarr": {
    "api_key": "",
    "profile": "HD-1080p",
    "root_folder": "/movies/",
    "url": "http://localhost:7878/"
  },
  "sonarr": {
    "api_key": "",
    "profile": "HD-1080p",
    "root_folder": "/tv/",
    "tags": {},
    "url": "http://localhost:8989/"
  },
  "trakt": {
    "api_key": ""
  }
}
```


## Core

```json
"core": {
  "debug": false
},
```

`debug` - show debug messages.
  - Default is `false` (keep it off unless your having issues).


## Automatic
Used for automatic / scheduled Traktarr tasks.

Movies can be run on a separate schedule from Shows.

```json
"automatic": {
  "movies": {
    "anticipated": 3,
    "boxoffice": 10,
    "interval": 24,
    "popular": 3,
    "trending": 2
  },
  "shows": {
    "anticipated": 10,
    "interval": 48,
    "popular": 1,
    "trending": 2
  }
},
```

`interval` - specify how often (in hours) to run Traktarr task.

`anticipated`, `popular`, `trending`, `boxoffice` (movies only) - specify how many items from each Trakt list to find.

## Filters

Use filters to specify the movie/shows's country of origin or blacklist (i.e. filter-out) certain keywords, genres, years, runtime, or specific movies/shows.

### Movies

```json
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
      "music",
      "animation"
    ],
    "blacklisted_max_year": 2019,
    "blacklisted_min_runtime": 60,
    "blacklisted_min_year": 2000,
    "blacklisted_tmdb_ids": []
  },
```

`allowed_countries` - allowed countries of origin.

`blacklist_title_keywords` - blacklist certain words in titles.

`blacklisted_genres` - blacklist certain generes.

`blacklisted_max_year` - blacklist release dates after specified year.

`blacklisted_min_runtime` - blacklist runtime duration lower than specified time (in minutes).

`blacklisted_min_year` - blacklist release dates before specified year.

`blacklisted_tmdb_ids` - blacklist certain movies with their TMDB IDs.

### Shows

```json
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
  "blacklisted_max_year": 2019,
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
  ],
  "blacklisted_tvdb_ids": []
}
```

`allowed_countries` - allowed countries of origin.

`blacklisted_genres` - blacklist certain generes.

`blacklisted_max_year` - blacklist release dates after specified year.

`blacklisted_min_runtime` - blacklist runtime duration lower than specified time (in minutes).

`blacklisted_min_year` - blacklist release dates before specified year.

`blacklisted_networks` - blacklist certain network.

`blacklisted_tvdb_ids` - blacklist certain shows with their TVDB IDs.


## Notifications

Notification alerts during tasks.

Currently, only Pushover and Slack are supported. More will abe added later.


```json
"notifications": {
  "pushover": {
    "service": "pushover",
    "app_token": "",
    "user_token": ""
  },
  "slack": {
    "service": "slack",
    "webhook_url": ""
  },
  "verbose": true,
},
```

`verbose` - toggle detailed notifications.
  - Default is `true` (keep it off unless your having issues).


### Pushover

`app_token` and `user_token` - retrieve from Pushover.net.

_Note: The key name (i.e the name right under notifications) can be anything, but the `"service":` must be exactly `"pushover"`._


### Slack

`webhook_url` - webhook URL you get after creating an "Incoming Webhook" under "Custom Integrations".

_Note: The key name (i.e the name right under notifications) can be anything, but the `"service":` must be exactly `"slack"`._


## Radarr

Radarr configuration.

```json
"radarr": {
  "api_key": "",
  "profile": "HD-1080p",
  "root_folder": "/movies/",
  "url": "http://localhost:7878"
},
```
`api_key` - Radarr's API Key.

`profile` - Profile that movies are assigned to.

`root_folder` - Root folder for movies.

`url` - Radarr's URL.


## Sonarr

Sonarr configuration.


```json
"sonarr": {
  "api_key": "",
  "profile": "HD-1080p",
  "root_folder": "/tv/",
  "tags": {},
  "url": "http://localhost:8989"
},
```

`api_key` - Sonarr's API Key.

`profile` - Profile that TV shows are assigned to.

`root_folder` - Root folder for TV shows.

`tags` - assign tags to shows based the network it airs on. More details on this below.

`url` - Sonarr's URL.


### Tags

To show how tags work, we will create a sample tag `AMZN` and assign it to certain networks.

### Sonarr

First, we will create a tag in Sonarr (Settings > Indexers > Restrictions).

```
Must contain: BluRay, Amazon, AMZN,
Must not contain:
Tags: AMZN
```

### Traktarr

Finally, we will edit the Traktarr config and assign the `AMZN` tag to certain networks.

```json
"tags": {
  "amzn": [
    "hbo",
    "amc",
    "usa network",
    "tnt",
    "starz",
    "the cw",
    "fx",
    "fox",
    "abc",
    "nbc",
    "cbs",
    "tbs",
    "amazon",
    "syfy",
    "cinemax",
    "bravo",
    "showtime",
    "paramount network"
  ]
}

```

## Trakt

```json
"trakt": {
  "api_key": ""
}
```

`api_key` - Fill in your Trakt API key (_Client ID_).


How to get a Trakt API Key:
  - Go to https://trakt.tv/oauth/applications/new
  - Fill in:
    - Name: `Traktarr`
    - Redirect uri: `https://google.com`
  - Click `Save App`
  - Retrieve the _Client ID_.

# Usage


## General

```
traktarr
```

```
Usage: traktarr [OPTIONS] COMMAND [ARGS]...

  Add new shows & movies to Sonarr/Radarr from Trakt lists.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  movies  Add new movies to Radarr.
  run     Run in automatic mode.
  shows   Add new shows to Sonarr.
  ```


## Movies

```
traktarr movies --help
```


```
Usage: traktarr movies [OPTIONS]

  Add new movies to Radarr.

Options:
  -t, --list-type [anticipated|trending|popular|boxoffice]
                                  Trakt list to process.  [required]
  -l, --add-limit INTEGER         Limit number of movies added to Radarr.
                                  [default: 0]
  -d, --add-delay FLOAT           Seconds between each add request to Radarr.
                                  [default: 2.5]
  -g, --genre TEXT                Only add movies from this genre to Radarr.
  -f, --folder TEXT               Add movies with this root folder to Radarr.
  --no-search                     Disable search when adding movies to Radarr.
  --notifications                 Send notifications.
  --help                          Show this message and exit.
```


## Shows

```
Usage: traktarr shows [OPTIONS]

  Add new shows to Sonarr.

Options:
  -t, --list-type [anticipated|trending|popular]
                                  Trakt list to process.  [required]
  -l, --add-limit INTEGER         Limit number of shows added to Sonarr.
                                  [default: 0]
  -d, --add-delay FLOAT           Seconds between each add request to Sonarr.
                                  [default: 2.5]
  -g, --genre TEXT                Only add shows from this genre to Sonarr.
  -f, --folder TEXT               Add shows with this root folder to Sonarr.
  --no-search                     Disable search when adding shows to Sonarr.
  --notifications                 Send notifications.
  --help                          Show this message and exit.
```

## Example


```
traktarr movies -t boxoffice -g comedy -l 10 --notifications

```

```
traktarr shows -t popular -l 2 --no-search
```
