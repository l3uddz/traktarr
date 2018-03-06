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
    "profile": "Remux",
    "root_folder": "/movies/",
    "url": "http://localhost:8989"
  },
  "sonarr": {
    "api_key": "",
    "profile": "WEBDL-1080p",
    "root_folder": "/tv/",
    "url": "http://localhost:8989"
  },
  "trakt": {
    "api_key": ""
  }
}
```
