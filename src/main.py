""" reads from impfterminservice.de
    """
import os
import yaml

# from dotenv.main import load_dotenv

from utils.scraper import TerminScraper

# load_dotenv()


def read_config():
    with open('./etc/config.yaml', 'rt') as f:
        return yaml.safe_load(f.read())

if __name__ == "__main__":

    config = read_config()

    # trial_zentrum = {"bundesland": "Baden-Württemberg", "address": "Ludwigsburg"}

    ts = TerminScraper(
        driver_path=config['chromiumdriverpath'],
        impfzentrum=config['trial_zentrum'],
        vermittlungscode=config['VERMITTLUNGSCODE'],
    )
    ts.check_in()
