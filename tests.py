import HtmlTestRunner
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PrestashopSearch(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)

    def test_search_in_prestashop(self):
        driver = self.driver
        driver.get("http://127.0.0.1:808" + os.environ["DEPLOY_ENV"])
        self.assertIn("Ma boutique", driver.title)
        elem = driver.find_element_by_name("s")
        elem.send_keys("pull")
        elem.send_keys(Keys.RETURN)
        assert "Veuillez nous excuser pour le désagrément." not in driver.page_source

    def test_search_unknow_prestashop(self):
        driver = self.driver
        driver.get("http://127.0.0.1:808" + os.environ["DEPLOY_ENV"])
        self.assertIn("Ma boutique", driver.title)
        elem = driver.find_element_by_name("s")
        elem.send_keys("lyufytdhrtsdtr")
        elem.send_keys(Keys.RETURN)
        assert "Veuillez nous excuser pour le désagrément." in driver.page_source
        
    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(combine_reports=True, report_name="MyReport-ENV-" + os.environ["DEPLOY_ENV"], add_timestamp=False))
