import datetime
import json
import time
from json import JSONDecodeError
from pathlib import Path
from typing import List
from redis import Redis


def convert_str_datetime_to_ts(str_datetime: str):
    res = time.mktime(datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S,%f").timetuple())
    return res


def get_redis():
    r = Redis(host=get_option_from_config(['redis_host'], 'localhost'),
              port=get_option_from_config(['redis_port'], 6379),
              password=get_option_from_config(['redis_password'], ''))
    return r


def load_json(file):
    file = Path(file)
    try:
        with file.open() as f:
            d = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        d = dict()

    return d


def get_config():
    config = load_json(Path(__file__).parent / '..' / 'config.json')
    return config


def get_option_from_config(option_path: List[str], default_value=None, config=None):
    config = get_config() if config is None else config
    if isinstance(option_path, str):
        option_path = [option_path]

    d = config
    for k in option_path:
        try:
            d = d[k]
        except KeyError:
            return default_value

    return d
