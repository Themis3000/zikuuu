import json
import os

# todo:Themi fix set_current so it adds values to an array
# todo:Themi make a way to remove items in a array

global options

config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
defaults_path = os.path.join(os.path.dirname(__file__), 'default_config.json')

if os.path.exists(config_path):
    with open(config_path, 'r') as config:
        options = json.load(config)
else:
    with open(config_path, 'w+', encoding='utf8') as config:
        with open(defaults_path, encoding='utf8') as defaults:
            options = json.load(defaults)
            json.dump(options, config, indent=3)


def check_options(setting=False):
    if setting:
        return [*options[setting]][1]['options']
    else:
        return [*options]


def check_current(setting):
    return [*options[setting]][0]['current']


def set_current(setting, value):
    with open(config_path, 'r+', encoding='utf8') as config:
        data = json.load(config)
        data[setting][0]['current'] = value
        config.seek(0)
        json.dump(data, config, indent=3)
        options = data
