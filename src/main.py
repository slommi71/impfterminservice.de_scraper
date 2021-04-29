import os

from dotenv.main import load_dotenv

from utils.scraper import TerminScraper

load_dotenv()

if __name__ == "__main__":
    # TODO: this should be input ?
    # TODO chromedriver.exe path etc
    trial_zentrum = {"bundesland": "Baden-Württemberg", "address": "Ludwigsburg"}

    a = TerminScraper(
        driver_path="chromedriver.exe",
        impfzentrum=trial_zentrum,
        vermittlungscode=os.getenv("VERMITTLUNGSCODE"),
    )
    a.check_in()
