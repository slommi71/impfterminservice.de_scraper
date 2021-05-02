import sys
from time import sleep
from typing import Dict

# from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from colorama import Fore, Back, Style

from utils.string_utils import normalize_string

# load_dotenv()


class TerminScraper:
    """
    Class to scrape impfterminservice.de
    """

    def __init__(
        self,
        impfzentrum: Dict,
        driver_path: str,
        vermittlungscode: str = None,
        headless: bool = False,
        timeout: int = 600,
    ) -> None:
        self.vermittlungscode = vermittlungscode
        self.impfzentrum = impfzentrum

        self.timeout = timeout

        # scraper options
        self.options = Options()
        self.options.add_argument("--log-level=3")
        if headless:
            self.options.add_argument("--headless")

        # setup webdriver
        self.driver = webdriver.Chrome(driver_path, options=self.options)

    def check_in(self):
        """
        Check in based on your selected vaccination center
        """
        self.driver.get("https://www.impfterminservice.de/impftermine")
        sleep(2)

        # accept cookies
        try:
            self.driver.find_element_by_xpath(
                "/html/body/app-root/div/div/div/div[2]/div[2]/div/div[1]/a"
            ).click()
            sleep(1)
        except NoSuchElementException as exc:
            pass

        # Select bundesland
        self.driver.find_element_by_xpath(
            "/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[3]/app-corona-vaccination-center/div[1]/label/span[2]/span[1]"
        ).click()

        bundeslaender = self.driver.find_elements_by_class_name(
            "select2-results__option"
        )
        for option in bundeslaender:
            if normalize_string(self.impfzentrum["bundesland"]) in normalize_string(
                option.text
            ):
                option.click()
                break

        # Select zentrum
        self.driver.find_elements_by_class_name("selection")[
            1
        ].click()  # a bit hacky but it should work for now

        zentren = self.driver.find_elements_by_class_name("select2-results__option")
        for option in zentren:
            if normalize_string(self.impfzentrum["address"]) in normalize_string(
                option.text
            ):
                option.click()
                break

        # Submit:
        self.driver.find_element_by_xpath(
            "/html/body/app-root/div/app-page-its-center/div/div[2]/div/div/div/div/form/div[4]/button"
        ).click()
        sleep(2)

        # Waitingroom:
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(
                    (By.NAME, "vaccination-approval-checked")
                )
            )
        except TimeoutException as exc:
            # TODO
            raise TimeoutError from exc

        # Vermittlungscode ?
        elements = self.driver.find_elements_by_class_name("ets-radio-control")
        if self.vermittlungscode:
            elements[0].click()
            self.search_appointment()

        else:
            elements[1].click()
            self.create_vermittlungscode()

    def search_appointment(self):
        """
        - insert vermittlungscode
        - check for appointment
        """
        sleep(2)

        # Fill in Vermittlungscode
        self.vermittlungscode = normalize_string(self.vermittlungscode)
        input_field = self.driver.find_element_by_name("ets-input-code-0")
        input_field.send_keys(self.vermittlungscode)
        input_field.submit()

        # Submit
        sleep(2)
        self.driver.find_element_by_xpath(
            "/html/body/app-root/div/app-page-its-search/div/div/div[2]/div/div/div[5]/div/div[1]/div[2]/div[2]/button"
        ).click()

        sleep(5)

        try:
            # TODO
            WebDriverWait(self.driver, 99999999).until_not(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "its-slot-pair-search-no-results")
                )
            )

            # TODO notify or create appointment
            print("there sould be an appointment")

            # keep window up 10 min for now
            sleep(600)

        except TimeoutException as exc:
            # TODO
            raise TimeoutError from exc

    def create_vermittlungscode(self):
        """
        TODO
        """
        sleep(4)
        no_date_avail = self.driver.find_elements_by_class_name("alert-danger")
        if no_date_avail:
            print(Back.RED +Fore.YELLOW + no_date_avail[0].text)
            print(Style.RESET_ALL)
            sleep(1)
            self.driver.quit()
            sys.exit(0)
        raise NotImplementedError("create_vermittlungscode not fully implemented")
