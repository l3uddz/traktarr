<img src="assets/logo.svg" width="600" alt="Traktarr">

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-blue.svg?style=flat-square)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%203-blue.svg?style=flat-square)](https://github.com/l3uddz/traktarr/blob/master/LICENSE.md)
[![last commit (develop)](https://img.shields.io/github/last-commit/l3uddz/traktarr/develop.svg?colorB=177DC1&label=Last%20Commit&style=flat-square)](https://github.com/l3uddz/traktarr/commits/develop)
[![Discord](https://img.shields.io/discord/381077432285003776.svg?colorB=177DC1&label=Discord&style=flat-square)](https://discord.io/cloudbox)
[![Contributing](https://img.shields.io/badge/Contributing-gray.svg?style=flat-square)](CONTRIBUTING.md)
[![Donate](https://img.shields.io/badge/Donate-gray.svg?style=flat-square)](#donate)


---

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Introduction](#introduction)
- [Demo](#demo)
- [Requirements](#requirements)
- [Installation](#installation)
  - [1. Base Install](#1-base-install)
  - [2. Create a Trakt Application](#2-create-a-trakt-application)
  - [3. Authenticate User(s) (optional)](#3-authenticate-users-optional)
- [Configuration](#configuration)
  - [Sample Configuration](#sample-configuration)
  - [Core](#core)
  - [Automatic](#automatic)
    - [Personal Watchlists](#personal-watchlists)
    - [Custom Lists](#custom-lists)
      - [Public Lists](#public-lists)
      - [Private Lists](#private-lists)
  - [Filters](#filters)
    - [Movies](#movies)
    - [Shows](#shows)
  - [Notifications](#notifications)
    - [Apprise](#apprise)
    - [Pushover](#pushover)
    - [Slack](#slack)
  - [Radarr](#radarr)
  - [Sonarr](#sonarr)
    - [Tags](#tags)
  - [Trakt](#trakt)
  - [OMDb](#omdb)
- [Usage](#usage)
  - [Automatic (Scheduled)](#automatic-scheduled)
    - [Setup](#setup)
    - [Customize](#customize)
  - [Manual (CLI)](#manual-cli)
    - [General](#general)
    - [Movie (Single Movie)](#movie-single-movie)
    - [Movies (Multiple Movies)](#movies-multiple-movies)
    - [Show (Single Show)](#show-single-show)
    - [Shows (Multiple Shows)](#shows-multiple-shows)
  - [Examples (CLI)](#examples-cli)
    - [Movies](#movies-1)
    - [Shows](#shows-1)
- [Donate](#donate)

<!-- /TOC -->

---

# Introduction

Traktarr uses Trakt.tv to find shows and movies to add in to Sonarr and Radarr, respectively.

Types of Trakt lists supported:

- Official Trakt Lists

  - Trending

  - Popular

  - Anticipated

  - Box Office

  - Most Watched

  - Most Played

- Public Lists

- Private Lists*

  - Watchlist

  - Custom List(s)

\* Support for multiple (authenticated) users.

# Demo

Click to enlarge.

[![asciicast](assets/demo.gif)](https://asciinema.org/a/180044)


# Requirements

1. Debian OS (can work in other operating systems as well).

2. Python 3.5+

3. Required Python modules.


# Installation

## 1. Base Install

Installs Traktarr to the system so that it can be ran with the `traktarr` command.


1. Clone the Traktarr repo.

   ```
   sudo git clone https://github.com/l3uddz/traktarr /opt/traktarr
   ```

1. Fix permissions of the `traktarr` folder (replace `user`/`group` with your info; run `id` to check).

   ```
   sudo chown -R user:group /opt/traktarr
   ```

1. Go into the `traktarr` folder.

   ```
   cd /opt/traktarr
   ```

1. Install Python and PIP.

   ```
   sudo apt-get install python3 python3-pip
   ```

1. Install the required python modules.

   ```
   sudo python3 -m pip install -r requirements.txt
   ```

1. Create a shortcut for `traktarr`.

   ```
   sudo ln -s /opt/traktarr/traktarr.py /usr/local/bin/traktarr
   ```

1. Generate a basic `config.json` file.

   ```
   traktarr run
   ```

1. Configure the `config.json` file.

   ```
   nano config.json
   ```

## 2. Create a Trakt Application

1. Create a Trakt application by going [here](https://trakt.tv/oauth/applications/new)

2. Enter a name for your application; for example `traktarr`

3. Enter `urn:ietf:wg:oauth:2.0:oob` in the `Redirect uri` field.

4. Click "SAVE APP".

5. Open the Traktarr configuration file `config.json` and insert your Trakt Client ID in the `client_id` and your Trakt Client Secret in the `client_secret`, like this:

   ```json
   "trakt": {
       "client_id": "your_trakt_client_id",
       "client_secret": "your_trakt_client_secret"
   }
   ```

## 3. Authenticate User(s) (optional)

For each user you want to access the private lists for (i.e. watchlist and/or custom lists), you will need to to authenticate that user.

Repeat the following steps for every user you want to authenticate:

1. Run the following command:

   ```
   traktarr trakt_authentication
   ```


2. You will get the following prompt:

   ```
   - We're talking to Trakt to get your verification code. Please wait a moment...
   - Go to: https://trakt.tv/activate on any device and enter A0XXXXXX. We'll be polling Trakt every 5 seconds for a reply
   ```
3. Go to https://trakt.tv/activate.

4. Enter the code you see in your terminal.

5. Click **Continue**.

6. If you are not logged in to Trakt.tv, login now.

7. Click **Accept**.

8. You will get the message: "Woohoo! Your device is now connected and will automatically refresh in a few seconds.".

You've now authenticated the user.

You can repeat this process for as many users as you like.


# Configuration

## Sample Configuration

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
      "disabled_for": [],
      "allowed_countries": [
        "us",
        "gb",
        "ca"
      ],
      "allowed_languages": [
        "en"
      ],
      "blacklisted_genres": [
        "documentary",
        "music",
        "animation"
      ],
      "blacklisted_max_runtime": 0,
      "blacklisted_min_runtime": 60,
      "blacklisted_min_year": 2000,
      "blacklisted_max_year": 2019,
      "blacklisted_title_keywords": [
        "untitled",
        "barbie",
        "ufc"
      ],
      "blacklisted_tmdb_ids": [],
      "rotten_tomatoes": ""
    },
    "shows": {
      "disabled_for": [],
      "allowed_countries": [
        "us",
        "gb",
        "ca"
      ],
      "allowed_languages": [],
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
      "blacklisted_max_runtime": 0,
      "blacklisted_min_runtime": 15,
      "blacklisted_min_year": 2000,
      "blacklisted_max_year": 2019,
      "blacklisted_title_keywords": [],
      "blacklisted_tvdb_ids": []
    }
  },
  "notifications": {
    "pushover": {
      "service": "pushover",
      "app_token": "",
      "user_token": "",
      "priority": 0
    },
    "slack": {
      "service": "slack",
      "webhook_url": ""
    },
    "verbose": true
  },
  "radarr": {
    "api_key": "",
    "minimum_availability": "released",
    "quality": "HD-1080p",
    "root_folder": "/movies/",
    "url": "http://localhost:7878/"
  },
  "sonarr": {
    "api_key": "",
    "language": "English",
    "quality": "HD-1080p",
    "root_folder": "/tv/",
    "tags": {},
    "url": "http://localhost:8989/"
  },
  "trakt": {
    "client_id": "",
    "client_secret": ""
  },
  "omdb": {
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

`debug` - Toggle debug messages in the log. Default is `false`.

  - Set to `true`, if you are having issues and want to diagnose why.


## Automatic

```json
"automatic": {
  "movies": {
    "anticipated": 3,
    "boxoffice": 10,
    "interval": 24,
    "popular": 3,
    "trending": 0,
    "watched": 2,
    "played_all": 2,
    "watchlist": {},
    "lists": {},
  },
  "shows": {
    "anticipated": 10,
    "interval": 48,
    "popular": 1,
    "trending": 2,
    "watched_monthly": 2,
    "played": 2,
    "watchlist": {},
    "lists": {}
  }
},
```
Used for automatic / scheduled Traktarr tasks.

Movies can be run on a separate schedule then from Shows.

_Note: These settings are only needed if you plan to use Traktarr on a schedule (vs just using it as a CLI command only; see [Usage](#usage))._

Format:

 - "List Name": # of items to add into Radarr/Sonarr.

_Note: The number specified is the number of items that will be added into Radarr/Sonarr. It is not a Trakt list limit, i.e. this is not going to lookup Top X items._

### Interval

`interval` - Specify how often (in hours) to run Traktarr task.

  - Setting `interval` to `0`, will skip the schedule for that task.

  - For example, if you only want to add movies and not TV shows, you can set show's `interval` to `0`.

### Official Trakt Lists

`anticipated` - Trakt Anticipated List.

- Most anticipated movies/shows based on the number of lists a movie/show appears on.

`popular` - Trakt Popular List.

-  Most popular movies/shows. Popularity is calculated using the rating percentage and the number of ratings.

`trending` - Trakt Trending List.

- All movies/shows being watched right now. Movies with the most users are returned first.

`boxoffice` - Trakt Box Office List. Movies only.

- Top 10 grossing movies in the U.S. box office last weekend. Updated every Monday morning.

`watched` - Most watched (unique users) movies in the specified time period.

  - `watched` / `watched_weekly` - Most watched in the week.

  - `watched_monthly` - Most watched in the month.

  - `watched_yearly` - Most watched in the year.

  - `watched_all` - Most watched of all time.

`played` - Most played (a single user can watch multiple times) items in the specified time period.

  - `played` / `played_weekly` - Most played in the week.

  - `played_monthly` - Most played in the month.

  - `played_yearly` - Most played in the year.

  - `played_all` Most played of all time.

`watchlist` - Specify which watchlists to fetch (see explanation below).

### Custom Lists

`lists` - Specify which custom lists to fetch (see explanation below).

You can also schedule any number of public or private custom lists.

For both public and private lists you'll need the url to that list. When viewing the list on Trakt, simply copy the url from the address bar of the your browser.

_Note: These are for non-watchlist lists. If you want to add a watchlist list, use the next section below._

#### Public Lists

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


#### Private Lists

Private lists can be added in two ways:

1. If there is only one authenticated user, you can add the private list just like any other public list:

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

2. If there are multiple authenticated users you want to fetch the lists from, you'll need to specify the username under `authenticate_as`.

   _Note: The user should have access to the list (either own the list or a list that was shared to them by a friend)._

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
### Personal Trakt Watchlists

The watchlist task can be scheduled with a different item limit for every (authenticated) user.

So for every user, you will add: `"username": limit` to the watchlist key. For example:

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


## Filters

Use filters to specify the movie/shows's country of origin or blacklist (i.e. filter-out) certain keywords, genres, years, runtime, or specific movies/shows.

### Movies

```json
  "movies": {
    "disabled_for": [],
    "allowed_countries": [
      "us",
      "gb",
      "ca"
    ],
    "allowed_languages": [],
    "blacklisted_genres": [
      "documentary",
      "music",
      "animation"
    ],
    "blacklisted_max_runtime": 0,
    "blacklisted_min_runtime": 60,
    "blacklisted_min_year": 2000,
    "blacklisted_max_year": 2019,
    "blacklisted_title_keywords": [
      "untitled",
      "barbie"
    ],
    "blacklisted_tmdb_ids": [],
    "rotten_tomatoes": ""
  },
```

`disabled_for` - Specify for which lists the blacklist is disabled for, when running in automatic mode.

- This is similar to running `--ignore-blacklist` via the CLI command.

- Example:

  ```json
  "disabled_for": [
      "anticipated",
      "watchlist:user1",
      "list:http://url-to-list"
  ],
  ```

`allowed_countries` - Only add movies from these countries. Listed as two-letter country codes.

- [List of available country codes](assets/list_of_country_codes.md).

- Special keywords:

  - Blank list (i.e. `[]`) - Add movies from any country.

  - `ignore` (i.e. `["ignore"]`) Add movies from any country, including ones with no country specified.

`allowed_languages` - Only add movies with these languages. Listed as two-letter language codes.

- Languages are in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format (e.g. `ja` for Japanese.)

- [List of available language codes](assets/list_of_language_codes.md).

- Special keywords:

  - Blank list (i.e. `[]`) - Only add shows that are in English (`en`).

`blacklisted_genres` - Blacklist certain genres.

- [List of available movie genres](assets/list_of_movie_genres.md).

- For an updated list, visit [here](https://trakt.docs.apiary.io/#reference/genres/list/get-genres).

- Special Keywords:

  - Blank list (i.e. `[]`) - Add movies from any genre.

  - `ignore` (i.e. `["ignore"]`) - Add movies from any genre, including ones with no genre specified.

`blacklisted_min_runtime` - Blacklist runtime duration shorter than specified time (in minutes).

`blacklisted_max_runtime` - Blacklist runtime duration longer than specified time (in minutes).

  - Has to be longer than `blacklisted_min_runtime` or else it will be ignored.

`blacklisted_min_year` - Blacklist release dates before specified year.

`blacklisted_max_year` - Blacklist release dates after specified year.

`blacklisted_title_keywords` - Blacklist certain words in titles.

`blacklisted_tmdb_ids` - Blacklist certain movies with their TMDB IDs.

  - Example:

    ```json
    "blacklisted_tmdb_ids": [
      140607,
      181808
    ],
    ```

`rotten_tomatoes` - Only add movies that are equal to or above this Rotten Tomatoes score. Requires an OMDb API Key (see [below](#omdb)).

### Shows

```json
"shows": {
  "allowed_countries": [
    "us",
    "gb",
    "ca"
  ],
  "allowed_languages": [],
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
  "blacklisted_max_runtime": 0,
  "blacklisted_min_runtime": 15,
  "blacklisted_min_year": 2000,
  "blacklisted_max_year": 2019,
  "blacklisted_title_keywords": [],
  "blacklisted_tvdb_ids": []
}
```

`disabled_for` - Specify for which lists the blacklist is disabled for, when running in automatic mode.

- This is similar to running `--ignore-blacklist` via the CLI command.

- Example:

  ```json
  "disabled_for": [
      "anticipated",
      "watchlist:user1",
      "list:http://url-to-list"
  ],
  ```

`allowed_countries` - Only add shows from these countries. Listed as two-letter country codes.

- [List of available country codes](assets/list_of_country_codes.md).

- Special keywords:

  - Blank list (i.e. `[]`) - Add shows from any country.

  - `ignore` (i.e. `["ignore"]`) Add shows from any country, including ones with no country specified.

`allowed_languages` - Only add shows with these languages.

- Languages are in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format (e.g. `ja` for Japanese.)

- [List of available language codes](assets/list_of_language_codes.md).

- Special keywords:

  - Blank list (i.e. `[]`) - Only add shows that are in English (`en`).

`blacklisted_genres` - Blacklist certain genres.

- [List of available TV show genres](assets/list_of_tv_show_genres.md).

- For an updated list, visit [here](https://trakt.docs.apiary.io/#reference/genres/list/get-genres).

- Special Keywords:

  - Blank list (i.e. `[]`) - Add shows from any genre.

  - `ignore` (i.e. `["ignore"]`) - Add shows from any genre, including ones with no genre specified.

`blacklisted_networks` - Blacklist certain network.

`blacklisted_min_runtime` - Blacklist runtime duration shorter than specified time (in minutes).

`blacklisted_max_runtime` - Blacklist runtime duration longer than specified time (in minutes).

  - Has to be longer than `blacklisted_min_runtime` or else it will be ignored.

`blacklisted_min_year` - Blacklist release dates before specified year.

`blacklisted_max_year` - Blacklist release dates after specified year.

`blacklisted_title_keywords` - Blacklist certain words in titles.

`blacklisted_tvdb_ids` - Blacklist certain shows with their TVDB IDs.

  - Example:

    ```json
    "blacklisted_tvdb_ids": [
      79274,
      85287,
      71256,
      194751,
      76733,
      336238
    ],
    ```


## Notifications


```json
"notifications": {
  "Apprise": {
    "service": "apprise",
    "url": "",
    "title": ""
  },
  "verbose": false
},
```

Notification alerts for Traktarr tasks.

For auto (i.e. scheduled) runs, notifications are enabled automatically when notification services are listed in this section.

For manual (i.e. CLI) commands, you need to add the  `--notifications` flag.

Supported `services`:
 - `apprise`
 - `pushover`
 - `slack`

_Note: The key name can be anything, but the `service` key must be must be the exact service name (e.g. `pushover`). See below for example._


```json
"notifications": {
  "anyname": {
    "service": "pushover",
  }
},
```


### General

`verbose` - Toggle detailed notifications.

  - Default is `true`.

  - Set to `false` if you want to reduce the amount of detailed notifications (e.g. just the total vs the names of the movies/shows added).

```json
"notifications": {
  "verbose": true
},
```

### Apprise

```json
"notifications": {
  "Apprise": {
    "service": "apprise",
    "url": "",
    "title": ""
  },
  "verbose": false
},
```

`url` - Apprise service URL (see [here](https://github.com/caronc/apprise)).

 - Required.

`title` - Notification Title.

 - Optional.

 - Default is `Traktarr`.


### Pushover

```json
"notifications": {
  "pushover": {
    "service": "pushover",
    "app_token": "",
    "user_token": "",
    "priority": 0
  },
  "verbose": false
},
```

`app_token`  - App Token from [Pushover.net](https://pushover.net).

 - Required.

`user_token` - User Token from [Pushover.net](https://pushover.net).

 - Required.

`priority` - [Priority](https://pushover.net/api#priority) of the notifications.

 - Optional.

 - Choices are: `-2`, `-1`, `0`, `1`, `2`.

 - Values are not quoted.

 - Default is `0`.


### Slack

```json
"notifications": {
  "slack": {
    "service": "slack",
    "webhook_url": "",
    "channel": "",
    "sender_name": "Traktarr",
    "sender_icon": ":movie_camera:"
  },
  "verbose": false
},
```

`webhook_url` - [Webhook URL](https://my.slack.com/services/new/incoming-webhook/).

 - Required.

`channel` - Slack channel to send the notifications to.

 - Optional.

 - Default is blank.

`sender_name` - Sender's name for the notifications.

 - Optional.

 - Default is `Traktarr`.

`sender_icon` - Icon to use for the notifications.

 - Optional.

 - Default is `:movie_camera:`



## Radarr

Radarr configuration.

```json
"radarr": {
  "api_key": "",
  "minimum_availability": "released",
  "quality": "HD-1080p",
  "root_folder": "/movies/",
  "url": "http://localhost:7878"
},
```
`api_key` - Radarr's API Key.

`quality` - Quality Profile that movies are assigned to.

`minimum_availability` - The minimum availability the movies are set to.

  - Choices are `announced`, `in_cinemas`, `released` (Physical/Web), or `predb`.

  - Default is `released` (Physical/Web).

`root_folder` - Root folder for movies.

  - Note: If you need the root folder to be a Windows share replace each \ with \\\\. \
Example: `C:\Path\To\Movies` will be `C:\\Path\\To\\Movies` and `\\Server\Path\To\Movies` will be `\\\\Server\\Path\\To\\Movies`

`url` - Radarr's URL.

  - Note: If you have URL Base enabled in Radarr's settings, you will need to add that into the URL as well.

## Sonarr

Sonarr configuration.


```json
"sonarr": {
  "api_key": "",
  "language": "English",
  "quality": "HD-1080p",
  "root_folder": "/tv/",
  "tags": {},
  "url": "http://localhost:8989"
},
```

`api_key` - Sonarr's API Key.

`language` - Language Profile that TV shows are assigned to. Only applies to Sonarr v3.

`quality` - Quality Profile that TV shows are assigned to.

`root_folder` - Root folder for TV shows.

  - Note: If you need the root folder to be a Windows share replace each \ with \\\\. \
Example: `C:\Path\To\TV Shows` will be `C:\\Path\\To\\TV Shows` and `\\Server\Path\To\TV Shows` will be `\\\\Server\\Path\\To\\TV Shows`

`tags` - Assign tags to shows based the network it airs on. More details on this below.

`url` - Sonarr's URL.

  - Note: If you have URL Base enabled in Sonarr's settings, you will need to add that into the URL as well.

### Tags

The `tags` option allows Sonarr to assign tags to shows from specific television networks, so that Sonarr can filter in/out certain keywords from releases.

**Example:**

To show how tags work, we will create a tag `AMZN` and assign it to certain television networks that usually have AMZN releases.

1. First, we will create a tag in Sonarr (Settings > Indexers > Restrictions).

   ```
   Must contain: BluRay, Amazon, AMZN
   Must not contain:
   Tags: AMZN
   ```

2. And, finally, we will edit the Traktarr config and assign the `AMZN` tag to some networks.

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

Trakt Authentication info:

```json
"trakt": {
  "client_id": "",
  "client_secret": ""
}
```

`client_id` - Your Trakt API Key (_Client ID_).

`client_secret` - Your Trakt Secret Key (_Client Secret_).

## OMDb

[OMDb](https://www.omdbapi.com/) Authentication info.

```json
"omdb": {
  "api_key":""
}
```

`api_key` - Your [OMDb](https://www.omdbapi.com/) API Key.

- This is only needed if you wish to use a minimum Rotten Tomatoes score to filter out movies.  

- Use `rotten_tomatoes` in config for automatic scheduling or `--rotten_tomatoes` as an argument for CLI.

# Usage

## Automatic (Scheduled)

### Setup

To have Traktarr get Movies and Shows for you automatically, on set interval, do the following:

1. `sudo cp /opt/traktarr/systemd/traktarr.service /etc/systemd/system/`

2. `sudo nano /etc/systemd/system/traktarr.service` and edit user/group to match yours' (run `id` to check).

3. `sudo systemctl daemon-reload`

4. `sudo systemctl enable traktarr.service`

5. `sudo systemctl start traktarr.service`

### Customize

You can customize how the scheduled Traktarr is ran by editing the `traktarr.service` file and adding any of the following options:

\* Remember, other configuration options need to go into the `config.json` file under the `Automatic` section.

```
traktarr run --help
```

```
Usage: traktarr run [OPTIONS]

  Run in automatic mode.

Options:
  -d, --add-delay FLOAT           Seconds between each add request to Sonarr /
                                  Radarr.  [default: 2.5]
  -s, --sort [votes|rating|release]
                                  Sort list to process.
  --no-search                     Disable search when adding to Sonarr /
                                  Radarr.
  --run-now                       Do a first run immediately without waiting.
  --no-notifications              Disable notifications.
  --ignore-blacklist              Ignores the blacklist when running the
                                  command.
  --help                          Show this message and exit.
```


`-d`, `--add-delay` - Add seconds delay between each add request to Sonarr / Radarr. Default is `2.5` seconds.

 - Example: `-d 5`

`-s`, `--sort` - Sort list by highest `votes`, highest `rating`, or the latest `release` dates. Default is highest `votes`.

 - Example: `-s release`

`--no-search` - Tells Sonarr / Radarr to not automatically search for added shows / movies.

`--run-now` - Traktarr will run first automated search on start, without waiting for next interval.

`--no-notifications` - Disable notifications. Default is `enabled`.

`--ignore-blacklist` - Ignores blacklist filtering. Equivalent of `disabled_for` in config.json.


Example of a modified line from the `traktarr.service` file that will always add from the most recent releases matched:

```
ExecStart=/usr/bin/python3 /opt/traktarr/traktarr.py run -s release
```

## Manual (CLI)

### General

```
traktarr
```

```
Usage: traktarr [OPTIONS] COMMAND [ARGS]...

  Add new shows & movies to Sonarr/Radarr from Trakt.

Options:
  --version         Show the version and exit.
  --config PATH     Configuration file  [default: /Users/macuser/Documents/Git
                    Hub/l3uddz/traktarr/config.json]
  --cachefile PATH  Cache file  [default:
                    /Users/macuser/Documents/GitHub/l3uddz/traktarr/cache.db]
  --logfile PATH    Log file  [default: /Users/macuser/Documents/GitHub/l3uddz
                    /traktarr/activity.log]
  --help            Show this message and exit.

Commands:
  movie                 Add a single movie to Radarr.
  movies                Add multiple movies to Radarr.
  run                   Run Traktarr in automatic mode.
  show                  Add a single show to Sonarr.
  shows                 Add multiple shows to Sonarr.
  trakt_authentication  Authenticate Traktarr.
  ```

### Movie (Single Movie)

```
traktarr movie --help
```

```
Usage: traktarr movie [OPTIONS]

  Add a single movie to Radarr.

Options:
  -id, --movie-id TEXT  Trakt Movie ID.  [required]
  -f, --folder TEXT     Add movie with this root folder to Radarr.
  -ma, --minimum-availability [announced|in_cinemas|released|predb]
                        Add movies with this minimum availability to Radarr.
  --no-search           Disable search when adding movie to Radarr.
  --help                Show this message and exit.
```

`-id`, `--movie-id` -  ID/slug of the movie to add to Radarr. Supports both Trakt and IMDB IDs. This arguent is required.

`-f`, `--folder` -  Add movie to a specific root folder in Radarr.

 - Example: `-f /mnt/unionfs/Media/Movies/Movies-Kids/`

`minimum_availability` - The minimum availability the movies are set to.

   - Choices are `announced`, `in_cinemas`, `released` (Physical/Web), or `predb`.

   - Default is `released` (Physical/Web).

`--no-search` - Tells Radarr to not automatically search for added movies.


### Movies (Multiple Movies)

```
traktarr movies --help
```


```
Usage: traktarr movies [OPTIONS]

  Add multiple movies to Radarr.

Options:
  -t, --list-type TEXT            Trakt list to process. For example, 'anticipated', 'trending',
                                  'popular', 'person', 'watched', 'played', 'recommended',
                                  'watchlist', or any URL to a list.  [required]
  -l, --add-limit INTEGER         Limit number of movies added to Radarr.
  -d, --add-delay FLOAT           Seconds between each add request to Radarr.  [default: 2.5]
  -s, --sort [rating|release|votes]
                                  Sort list to process.  [default: votes]
  -rt, --rotten_tomatoes INTEGER  Set a minimum Rotten Tomatoes score.
  -g, --genres TEXT               Only add movies from this genre to Radarr. Multiple genres are
                                  specified as a comma-separated list. Use 'ignore' to add movies
                                  from any genre, including ones with no genre specified.
  -f, --folder TEXT               Add movies with this root folder to Radarr.
  -ma, --minimum-availability [announced|in_cinemas|released|predb]
                                  Add movies with this minimum availability to Radarr. Default is
                                  'released'.
  -a, --actor TEXT                Only add movies from this actor to Radarr.Only one actor can be
                                  specified.Requires the 'person' list.
  --include-non-acting-roles      Include non-acting roles such as 'As Himself', 'Narrator', etc.
                                  Requires the 'person' list option with the 'actor' argument.
  --no-search                     Disable search when adding movies to Radarr.
  --notifications                 Send notifications.
  --authenticate-user TEXT        Specify which user to authenticate with to retrieve Trakt lists.
                                  Defaults to first user in the config.
  --ignore-blacklist              Ignores the blacklist when running the command.
  --remove-rejected-from-recommended
                                  Removes rejected/existing movies from recommended.
  --help                          Show this message and exit.
```

`-t`, `--list-type` - Trakt list to process.

Choices are: `anticipated`, `trending`, `popular`, `boxoffice`, `watched`, `played`, `URL` (Trakt list), or `person` (used with `-a`/`--actor` argument).

- Top Watched List options:

  - `watched` / `watched_weekly` - Most watched in the week.

  - `watched_monthly` - Most watched in the month.

  - `watched_yearly` - Most watched in the year.

  - `watched_all` - Most watched of all time.

- Top Played List options:

  - `played` / `played_weekly` - Most played in the week.

  - `played_monthly` - Most played in the month.

  - `played_yearly` - Most played in the year.

  - `played_all` Most played of all time.

`-l`, `--add-limit` - Limit number of movies added to Radarr.

 - Note: This is a limit on how many items are added into Radarr. Not a limit on how many items to retrieve from Trakt.

`-d`, `--add-delay` - Add seconds delay between each add request to Radarr. Default is 2.5 seconds.

 - Example: `-d 5`

`-s`, `--sort` - Sort list by highest `votes`, highest `rating`, or the latest `release` dates. Default is highest `votes`.

 - Example: `-s release`

`-rt`, `--rotten_tomatoes` -  Only add movies equal to or above this Rotten Tomatoes score.

 - Example: `-rt 75`

`-g`, `--genres` - Only add movies from these genre(s) to Radarr.

- Multiple genres are passed as comma-separated lists. The effect of this is equivalent of boolean OR. (ie. include items from any of these genres).

- Can find a list [here](assets/list_of_movie_genres.md).

`-f`, `--folder` -  Add movies to a specific root folder in Radarr.

 - Example: `-f /mnt/unionfs/Media/Movies/Movies-Kids/`

`minimum_availability` - The minimum availability the movies are set to.

  - Choices are `announced`, `in_cinemas`, `released` (Physical/Web), or `predb`.

  - Default is `released` (Physical/Web).

`-a`, `--actor` - Only add movies with a specific actor to Radarr.

  - Requires the list type `person`.

`--include-non-acting-roles` - Include non-acting roles of the specified actor.

  - Requires the list type `person` used with the `-a`/`--actor` option.

`--no-search` - Tells Radarr to not automatically search for added movies.

`--notifications` - To enable notifications. Default is `disabled`.

`--authenticate-user` - Specify which authenticated user to retrieve Trakt lists as. Default is the first user in the config.

`--ignore-blacklist` - Ignores blacklist filtering.

 - Equivalent of `disabled_for` in `config.json`.

`--remove-rejected-from-recommended` - Removes rejected/existing shows from the recommended list, so that it will be removed from further recommendations.


### Show (Single Show)

```
traktarr show --help
```


```
Usage: traktarr show [OPTIONS]

  Add a single show to Sonarr.

Options:
  -id, --show-id TEXT  Trakt Show ID.  [required]
  -f, --folder TEXT    Add show with this root folder to Sonarr.
  --no-search          Disable search when adding show to Sonarr.
  --help               Show this message and exit.
```

`-id`, `--show-id` -  ID/slug of the show to add to Sonarr. Supports both Trakt and IMDB IDs. This argument is required.


### Shows (Multiple Shows)

```
traktarr shows --help
```


```
Usage: traktarr shows [OPTIONS]

  Add multiple shows to Sonarr.

Options:
  -t, --list-type TEXT            Trakt list to process.
                                  For example, 'anticipated', 'trending',
                                  'popular', 'person', 'watched', 'played', 'recommended',
                                  'watchlist', or any URL to a list.  [required]
  -l, --add-limit INTEGER         Limit number of shows added to Sonarr.
  -d, --add-delay FLOAT           Seconds between each add request to Sonarr.  [default: 2.5]
  -s, --sort [rating|release|votes]
                                  Sort list to process.  [default: votes]
  -g, --genres TEXT               Only add shows from this genre to Sonarr. Multiple genres are
                                  specified as a comma-separated list.
                                  Use 'ignore' to add shows
                                  from any genre, including ones with no genre specified.
  -f, --folder TEXT               Add shows with this root folder to Sonarr.
  -a, --actor TEXT                Only add movies from this actor to Radarr. Only one actor can be
                                  specified.
                                  Requires the 'person' list option.
  --include-non-acting-roles      Include non-acting roles such as 'As Himself', 'Narrator', etc.
                                  Requires the 'person' list option with the 'actor' argument.
  --no-search                     Disable search when adding shows to Sonarr.
  --notifications                 Send notifications.
  --authenticate-user TEXT        Specify which user to authenticate with to retrieve Trakt lists.
                                  Defaults to first user in the config
  --ignore-blacklist              Ignores the blacklist when running the command.
  --remove-rejected-from-recommended
                                  Removes rejected/existing shows from recommended.
  --help                          Show this message and exit.
```


`-t`, `--list-type` - Trakt list to process.

Choices are: `anticipated`, `trending`, `popular`, `watched`, `played`, `URL` (Trakt list), or `person` (used with `-a`/`--actor` argument).

- Top Watched List options:

  - `watched` / `watched_weekly` - Most watched in the week.

  - `watched_monthly` - Most watched in the month.

  - `watched_yearly` - Most watched in the year.

  - `watched_all` - Most watched of all time.

- Top Played List options:

  - `played` / `played_weekly` - Most played in the week.

  - `played_monthly` - Most played in the month.

  - `played_yearly` - Most played in the year.

  - `played_all` Most played of all time.

`-l`, `--add-limit` - Limit number of shows added to Sonarr.

 - Note: This is a limit on how many items are added into Sonarr. Not a limit on how many items to retrieve from Trakt.

`-d`, `--add-delay` - Add seconds delay between each add request to Sonarr. Default is 2.5 seconds.

 - Example: `-d 5`

`-s`, `--sort` - Sort list by highest `votes`, highest `rating`, or the latest `release` dates. Default is highest `votes`.

 - Example: `-s release`

`-g`, `--genres` - Only add shows from this genre(s) to Sonarr.

- Multiple genres are passed as comma-separated lists. The effect of this is equivalent of boolean OR. (ie. include items from any of these genres).

- Can find a list [here](assets/list_of_tv_show_genres.md).

`-f`, `--folder` -  Add shows to a specific root folder in Sonarr.

 - Example: `-f /mnt/unionfs/Media/Shows/Shows-Kids/`

`-a`, `--actor` - Only add shows with a specific actor to Sonarr.

   - Requires the list type `person`.

`--include-non-acting-roles` - Include non-acting roles of the specified actor.

  - Requires the list type `person` used with the `-a`/`--actor` option.

`--no-search` - Tells Sonarr to not automatically search for added shows.

`--notifications` - To enable notifications. Default is `disabled`.

`--authenticate-user` - Specify which authenticated user to retrieve Trakt lists as. Default is the first user in the config.

`--ignore-blacklist` - Ignores blacklist filtering. Equivalent of `disabled_for` in `config.json`.

`--remove-rejected-from-recommended` - Removes rejected/existing shows from the recommended list, so that it will be removed from further recommendations.


## Examples (CLI)

### Movies

- Add the movie "Black Panther (2018)":

  ```
  traktarr movie -id black-panther-2018
  ```

- Add movies, from the popular list, labeled with the thriller genre, limited to 5 items, and sorted by latest release date.

  ```
  traktarr movies -t popular -g thriller -l 5 -s release
  ```

- Add movies, from the Box Office list, labeled with the comedy genre, limited to 10 items, and send notifications:

  ```
  traktarr movies -t boxoffice -g comedy -l 10 --notifications
  ```

- Add movies, from a list of most watched played this week, and limited to 5 items.

  ```
  traktarr movies -t watched -l 5
  ```

- Add movies, from a list of most played movies this month, and limited to 5 items.

  ```
  traktarr movies -t played_monthly -l 5
  ```

- Add (all) movies from the public list `https://trakt.tv/users/rkerwin/lists/top-100-movies`:

  ```
  traktarr movies -t https://trakt.tv/users/rkerwin/lists/top-100-movies
  ```

- Add (all) movies from the private list `https://trakt.tv/users/user1/lists/private-movies-list` of `user1`:

  ```
  traktarr movies -t https://trakt.tv/users/user1/lists/private-movies-list --authenticate-user=user1
  ```

- Add movies, from the trending list, with a minimum Rotten Tomatoes score of 80%.

  ```
  traktarr movies -t trending -rt 80
  ```

- Add movies, with actor 'Keanu Reeves', limited to 10 items.

  ```
  traktarr movies -t person -a 'keanu reeves' -l 10
  ```

- Add movies, with actor 'Tom Cruise', including movies where he has non-acting roles, limited to 10 items.

  ```
  traktarr movies -t person -a 'tom cruise' --include-non-acting-roles -l 10
  ```

### Shows

- Add the show "The 100":

  ```
  traktarr show -id the-100
  ```

- Add shows, from the popular list, limited to 5 items, and sorted by highest ratings.

  ```
  traktarr shows -t popular -l 5 -s rating
  ```

- Add shows, from the popular list, limited to 2 items, and add them but don't search for episodes in Sonarr:

  ```
  traktarr shows -t popular -l 2 --no-search
  ```

- Add shows, from a list of most watched shows this year, and limited to 5 items.

  ```
  traktarr shows -t watched_yearly -l 5
  ```

- Add shows, from a list of most played shows this week, and limited to 5 items.

  ```
  traktarr shows -t played -l 5
  ```

- Add shows, from a list of most played shows of all time, and limited to 5 items.

  ```
  traktarr shows -t played_all -l 5
  ```

- Add (all) shows from the watchlist of `user1`:

  ```
  traktarr shows -t watchlist --authenticate-user user1
  ```

***

# Donate

If you find this project helpful, feel free to make a small donation to the developer:

  - [Monzo](https://monzo.me/jamesbayliss9): Credit Cards, Apple Pay, Google Pay

  - [Beerpay](https://beerpay.io/l3uddz/traktarr): Credit Cards

  - [Paypal: l3uddz@gmail.com](https://www.paypal.me/l3uddz)

  - BTC: 3CiHME1HZQsNNcDL6BArG7PbZLa8zUUgjL
