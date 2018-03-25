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
            'blacklisted_genres': [],
            'blacklisted_networks': [],
            'allowed_countries': [],
            'blacklisted_min_runtime': 15,
            'blacklisted_min_year': 2000,
            'blacklisted_max_year': 2019,
            'blacklisted_tvdb_ids': [],
        },
        'movies': {
            'blacklisted_genres': [],
            'blacklisted_min_runtime': 60,
            'blacklisted_min_year': 2000,
            'blacklisted_max_year': 2019,
            'blacklist_title_keywords': [],
            'blacklisted_tmdb_ids': [],
            'allowed_countries': []
        }
    },
    'automatic': {
        'movies': {
            'interval': 20,
            'anticipated': 3,
            'trending': 3,
            'popular': 3,
            'boxoffice': 10
        },
        'shows': {
            'interval': 48,
            'anticipated': 10,
            'trending': 1,
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


def upgrade_settings(defaults, currents):
    upgraded = False

    def inner_upgrade(default, current, key=None):
        sub_upgraded = False
        merged = current.copy()
        if isinstance(default, dict):
            for k, v in default.items():
                # missing k
                if k not in current:
                    merged[k] = v
                    sub_upgraded = True
                    if not key:
                        print("Added %r config option: %s" % (str(k), str(v)))
                    else:
                        print("Added %r to config option %r: %s" % (str(k), str(key), str(v)))
                    continue
                # iterate children
                if isinstance(v, dict) or isinstance(v, list):
                    did_upgrade, merged[k] = inner_upgrade(default[k], current[k], key=k)
                    sub_upgraded = did_upgrade if did_upgrade else sub_upgraded

        elif isinstance(default, list) and key:
            for v in default:
                if v not in current:
                    merged.append(v)
                    sub_upgraded = True
                    print("Added to config option %r: %s" % (str(key), str(v)))
                    continue
        return sub_upgraded, merged

    upgraded, upgraded_settings = inner_upgrade(defaults, currents)
    return upgraded, AttrConfig(upgraded_settings)


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
