import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)


    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8081")
        self.assertIn("Ma boutique", driver.title)
        elem = driver.find_element_by_name("s")
        elem.send_keys("pull")
        elem.send_keys(Keys.RETURN)
        assert "Veuillez nous excuser pour le désagrément." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()