import logging.config
import yaml
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
