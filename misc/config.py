import json
import os
import sys

from attrdict import AttrDict

config_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), 'config.json')
base_config = {
    'core': {
        'debug': False
    },
    'trakt': {
        'api_key': ''
    },
    'sonarr': {
        'url': 'http://localhost:8989',
        'api_key': '',
        'profile': 'HD-1080p',
        'root_folder': '/tv/',
        'tags': {
        }
    },
    'radarr': {
        'url': 'http://localhost:7878',
        'api_key': '',
        'profile': 'HD-1080p',
        'root_folder': '/movies/'
    },
    'filters': {
        'shows': {
            'blacklisted_genres': ['animation', 'game-show', 'talk-show', 'home-and-garden', 'children', 'reality',
                                   'anime', 'news', 'documentary', 'special-interest'],
            'blacklisted_networks': ['twitch', 'youtube', 'nickelodeon', 'hallmark', 'reelzchannel', 'disney',
                                     'cnn', 'cbbc', 'the movie network', 'teletoon', 'cartoon network', 'espn',
                                     'yahoo!',
                                     'fox sports'],
            'allowed_countries': ['us', 'gb', 'ca'],
            'blacklisted_min_runtime': 15,
            'blacklisted_min_year': 2000,
            'blacklisted_max_year': 2019
        },
        'movies': {
            'blacklisted_genres': ['documentary', 'music'],
            'blacklisted_min_runtime': 60,
            'blacklisted_min_year': 2000,
            'blacklisted_max_year': 2019,
            'blacklist_title_keywords': ['untitled', 'barbie'],
            'allowed_countries': ['us', 'gb', 'ca']
        }
    },
    'automatic': {
        'movies': {
            'interval': 24,
            'anticipated': 10,
            'trending': 2,
            'popular': 3,
            'boxoffice': 10
        },
        'shows': {
            'interval': 72,
            'anticipated': 100,
            'trending': 2,
            'popular': 1
        }
    },
    'notifications': {
        'verbose': True
    }
}
cfg = None


class AttrConfig(AttrDict):
    """
    Simple AttrDict subclass to return None when requested attribute does not exist
    """

    def __init__(self, config):
        super().__init__(config)

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            pass
        # Default behaviour
        return None


def build_config():
    if not os.path.exists(config_path):
        print("Dumping default config to: %s" % config_path)
        with open(config_path, 'w') as fp:
            json.dump(base_config, fp, sort_keys=True, indent=2)
        return True
    else:
        return False


def dump_config():
    if os.path.exists(config_path):
        with open(config_path, 'w') as fp:
            json.dump(cfg, fp, sort_keys=True, indent=2)
        return True
    else:
        return False


def load_config():
    with open(config_path, 'r') as fp:
        return AttrConfig(json.load(fp))


def upgrade_settings(defaults, current):
    upgraded = False
    res = current.copy()
    for k, v in defaults.items():
        if k not in current:
            res[k] = v
            upgraded = True
            print("Added config option: %s" % k)

        if hasattr(v, 'items'):
            if k in current:
                sub_upgrade, res[k] = upgrade_settings(v, current[k])
                if sub_upgrade:
                    upgraded = True
            else:
                res[k] = v
                upgraded = True

    return upgraded, AttrConfig(res)


############################################################
# LOAD CFG
############################################################

# dump/load config
if build_config():
    print("Please edit the default configuration before running again!")
    sys.exit(0)
else:
    tmp = load_config()
    upgraded, cfg = upgrade_settings(base_config, tmp)
    if upgraded:
        dump_config()
        print("New config options were added, adjust and restart!")
        sys.exit(0)
