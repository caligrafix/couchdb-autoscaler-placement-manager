# External libraries
import sys
import time
import logging

# Internal code
from src.scenarios import *
from src.scripts import *
from src.envs import *


def main():
    args = sys.argv[1:]

    if len(args) == 1 and args[0] == '--placement-manager':
        tag_zone_nodes(couchdb_url, namespace)

    else:
        raise Exception(
            "You must provide --placement-manager as first argument")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger('faker').setLevel(logging.ERROR)
    logging.getLogger('kubernetes').setLevel(logging.ERROR)
    logging.getLogger("PIL.Image").setLevel(logging.CRITICAL + 1)
    main()
