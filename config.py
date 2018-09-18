from os.path import join, dirname
from os import environ
import yaml


default_relative_path = join(dirname(__file__), 'config.yml')
yml_path = environ.get('INSTIGATOR_DETECTION_CONFIG_PATH', default_relative_path)
with open(yml_path, "r", encoding='utf-8') as yml_file:
    CONFIG = yaml.safe_load(yml_file)
