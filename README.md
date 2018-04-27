# Traktarr
Script to add new shows & movies to Sonarr/Radarr based on Trakt lists.

Trakt lists currently supported:
- anticipated
- boxoffice
- interval
- popular
- trending

Furthermore, watchlists and custom list from multiple users are supported.

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

## 2. Create app authentication

1. Create an Trakt application by going [here](https://trakt.tv/oauth/applications/new)
2. Enter a name for your application; for example `Traktarr`
3. Enter `urn:ietf:wg:oauth:2.0:oob` in the Redirecht uri field.
4. Click "Save app"
5. Open the Traktarr configuration file `config.json` and insert the
Client ID in the api_key and the Client Secret in the api_secret. Like this:
```
    {
        "trakt": {
            "api_key": "my_client_id",
            "api_secret": "my_client_secret_key"
        }
    }
```

## 3. Authenticate users (optional)

If you want to be able to access private lists, you have to authentcate that user.

Repeat the following steps for every user you want to authenticate:
1. Run `traktarr trakt_authenticate` (from the installation path)
2. Go to https://trakt.tv/activate.
3. Enter the code you see in your terminal
4. Click continue
5. If you're not loggedin to Trakt, login noe
6. Accept

You've now authenticated the user.
You can repeat this process for as many users as you want.

## 4. Setup Schedule

To have Traktarr get Movies and Shows for you automatically, on set interval.

1. `sudo cp /opt/traktarr/systemd/traktarr.service /etc/systemd/system/`
2. `sudo systemctl daemon-reload`
3. `sudo systemctl enable traktarr.service`
4. `sudo systemctl start traktarr.service`



# Configuration

Here is some default configuration you can use.

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
        "barbie",
        "ufc"
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
    "api_key": "",
    "api_secret": ""
  }
}
```


## Watchlist

Traktarr can fetch the watchlist for as many users as you like.
You'll have to authenticate every user from whome you want to fetch the watchlist,
by following the steps described [here]((#authenticate-users-optional)).

When all users are authenticated you can fetch their watchlist either
with the automatic task or with the manual commands (see examples below).

## Other custom user lists

Traktarr can also fetch any number of other custom lists.

If the custom list is private, you'll have to authenticate a user that is allowed to
access that list by following the steps described [here]((#authenticate-users-optional)).

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
    "trending": 2,
    "watchlist": {},
    "lists": {}
  },
  "shows": {
    "anticipated": 10,
    "interval": 48,
    "popular": 1,
    "trending": 2,
    "watchlist": {},
    "lists": {}
  }
},
```

`interval` - specify how often (in hours) to run Traktarr task.

`anticipated`, `popular`, `trending`, `boxoffice` (movies only) - specify how many items from each Trakt list to find.

`watchlist` - specify which watchlists to fetch (see explanation below)

`lists` - specify which custom lists to fetch (see explanation below)

### Watchlist

The watchlist task can be scheduled with a differtent item limit for every user.
For every user you've to add: `"username": limit` to the watchlist key. For example:

```json
"automatic": {
  "movies": {
    "watchlist": {
        "user1": 10,
        "user2": 5
    }
  },
  "shows": {
    "watchlist": {
        "user1": 2,
        "user3": 1
    }
  }
},
```

Of course you can combine this with running the other list types as well.

_Please note that every user from whome you fetch the watchlist should be authenticated._

### Custom lists

You can also schedule any number of public or private custom lists.
For both public and private lsits you'll need the url to that list.
You can copy this url from the address bar in you browser when viewing
the list on Trakt.

Public lists can be added by specifying the url and the item limit like this:

```json
"automatic": {
  "movies": {
    "lists": {
        "https://trakt.tv/users/rkerwin/lists/top-100-movies": 10
    }
  },
  "shows": {
    "lists": {
        "https://trakt.tv/users/claireaa/lists/top-100-tv-shows-of-all-time-ign": 10
    }
  }
},
```

Private lists can be added in two ways:

1. If there is only one authenticated user to Traktarr, you can add
the private list just like any other public list:

```json
"automatic": {
  "movies": {
    "lists": {
        "https://trakt.tv/users/user/lists/my-private-movies-list": 10
    }
  },
  "shows": {
    "lists": {
        "https://trakt.tv/users/user/lists/my-private-shows-list": 10
    }
  }
},
```

2. If there are multiple authenticated users to Traktarr, you'll need
to specify with which user Traktarr should authenticate when fetching
the list. The user should have acces to the list (either own the list,
or friends with the owner of the list and the list is specified to be
shared with friends)
_Note that the specified user has to be authenticated_

```json
"automatic": {
  "movies": {
    "lists": {
        "https://trakt.tv/users/user/lists/my-private-movies-list": {
            "authenticate_as": "user2",
            "limit": 10
        }
    }
  },
  "shows": {
    "lists": {
        "https://trakt.tv/users/user/lists/my-private-shows-list": {
            "authenticate_as": "user2",
            "limit": 10
        }
    }
  }
},
```


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
  "api_key": "",
  "api_scret": ""
}
```

`api_key` - Fill in your Trakt API key (_Client ID_).

`api_secret` - Fill in your Trakt Secret key (_Client Scret_)

_Note that when users authenticate to Traktarr, their token information
will be added to this._

# Usage


## General

```
traktarr
```

```
Usage: traktarr [OPTIONS] COMMAND [ARGS]...

  Add new shows & movies to Sonarr/Radarr from Trakt lists.

Options:
  --version       Show the version and exit.
  --config PATH   Configuration file  [default: /opt/traktarr/config.json]
  --logfile PATH  Log file  [default: /opt/traktarr/activity.log]
  --help          Show this message and exit.

Commands:
  movies                Add new movies to Radarr.
  run                   Run in automatic mode.
  shows                 Add new shows to Sonarr.
  trakt_authentication  Authenticate Traktrarr to index your personal...
  ```


## Movies

```
traktarr movies --help
```


```
Usage: traktarr movies [OPTIONS]

  Add new movies to Radarr.

Options:
  -t, --list-type TEXT            Trakt list to process. For example, anticipated,
                                  trending, popular, boxoffice, watchlist or any
                                  URL to a list  [required]
  -l, --add-limit INTEGER         Limit number of movies added to Radarr.
                                  [default: 0]
  -d, --add-delay FLOAT           Seconds between each add request to Radarr.
                                  [default: 2.5]
  -g, --genre TEXT                Only add movies from this genre to Radarr.
  -f, --folder TEXT               Add movies with this root folder to Radarr.
  --no-search                     Disable search when adding movies to Radarr.
  --notifications                 Send notifications.
  --authencate-user TEXT          Specify which user to authenticate with to
                                  retrieve Trakt lists. Default: first user in the
                                  config
```


## Shows

```
Usage: traktarr shows [OPTIONS]

  Add new shows to Sonarr.

Options:
  -t, --list-type TEXT            Trakt list to process. For example, anticipated,
                                  trending, popular, watchlist or any URL to a
                                  list  [required]
  -l, --add-limit INTEGER         Limit number of shows added to Sonarr.
                                  [default: 0]
  -d, --add-delay FLOAT           Seconds between each add request to Sonarr.
                                  [default: 2.5]
  -g, --genre TEXT                Only add shows from this genre to Sonarr.
  -f, --folder TEXT               Add shows with this root folder to Sonarr.
  --no-search                     Disable search when adding shows to Sonarr.
  --notifications                 Send notifications.
  --authencate-user TEXT          Specify which user to authenticate with to
                                  retrieve Trakt lists. Default: first user in the
                                  config
  --help                          Show this message and exit.
```

## Examples

- Fetch boxoffice movies labeld with the comedy genere, limit to 10 items and send notifications
```
traktarr movies -t boxoffice -g comedy -l 10 --notifications
```


- Fetch popular shows, limit to 2 items and don't start the search in Sonarr
```
traktarr shows -t popular -l 2 --no-search
```

- Fetch all shows from the watchlist from user1

```
traktarr shows -t watchlist --authenticate-user user1
```

- Fetch all movies from the public https://trakt.tv/users/rkerwin/lists/top-100-movies list

```
traktarr shows -t https://trakt.tv/users/rkerwin/lists/top-100-movies
```

- Fetch all movies from the private https://trakt.tv/users/user1/lists/private-movies-list list

```
traktarr shows -t https://trakt.tv/users/user1/lists/private-movies-list --authenticate-user=user1
```