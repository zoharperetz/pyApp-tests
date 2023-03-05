import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://flask:5000")

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        input_field = self.driver.find_element(By.NAME, "City")
        input_field.send_keys("New York")
        self.driver.find_element(By.XPATH, "/html/body/center/form/label/p[2]/input").send_keys(Keys.ENTER)
        output_field = self.driver.find_element(By.XPATH, "/html/body/center/form/label/h3")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/center/form/label/h3"), ""))
        assert output_field.text != ""
        
    def test_invalid_input(self):
        input_field = self.driver.find_element(By.NAME, "City")
        input_field.send_keys("")
        self.driver.find_element(By.XPATH, "/html/body/center/form/label/p[2]/input").send_keys(Keys.ENTER)
        output_field = self.driver.find_element(By.XPATH, "/html/body/center/form/label")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/center/form/label"), ""))
        assert output_field.text != ""



if __name__ == "__main__":
    unittest.main()

