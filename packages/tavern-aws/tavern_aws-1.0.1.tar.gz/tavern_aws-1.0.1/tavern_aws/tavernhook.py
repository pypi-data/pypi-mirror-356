import logging
from os.path import abspath, dirname, join

import yaml
from tavern._plugins.rest.tavernhook import TavernRestPlugin

from .session import AWSSession

logger = logging.getLogger(__name__)


def load_plugin_schema():
    schema_path = join(abspath(dirname(__file__)), "schema.yaml")
    with open(schema_path, "r") as schema_file:
        return yaml.load(schema_file, Loader=yaml.SafeLoader)


class TavernAwsPlugin(TavernRestPlugin):
    session_type = AWSSession
    schema = load_plugin_schema()
