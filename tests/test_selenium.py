import unittest
import pathlib
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
unittest.TestLoader.sortTestMethodsUsing = None

class SeleniumTests(unittest.TestCase):

    _menu_elements = None
    _price_of_first_element = None

    @classmethod
    def setUpClass(self) -> None:
        self.current_dir = str(pathlib.Path(__file__).parent.absolute())
        self.firefox_driver_path = self.current_dir+"\\..\\driver\\geckodriver.exe"
        self.driver = webdriver.Firefox(executable_path=self.firefox_driver_path)
        self.driver.implicitly_wait(5)
        self._menu_elements = []

    def test_step_01(self) -> None:
        '''
        1. Go to https://www.microsoft.com/en-us/
        '''
        print("step: 1")
        self.driver.get("https://www.microsoft.com/en-us/")
        
        '''
        2. Validate all menu items are present (Office - Windows - Surface - Xbox - Deals - Support)
        '''
        print("step: 2")
        time.sleep(0.5) # Sometimes things go too smooth, and we gotta slow down a bit.
        menu_text_1 = self.driver.find_element_by_id("shellmenu_0").text
        self.assertEqual(menu_text_1, "Microsoft 365")

        menu_text_2 = self.driver.find_element_by_id("shellmenu_1").text
        self.assertEqual(menu_text_2, "Office")

        menu_text_3 = self.driver.find_element_by_id("shellmenu_2").text
        self.assertEqual(menu_text_3, "Windows")

        menu_text_4 = self.driver.find_element_by_id("shellmenu_3").text
        self.assertEqual(menu_text_4, "Surface")

        menu_text_5 = self.driver.find_element_by_id("shellmenu_4").text
        self.assertEqual(menu_text_5, "Xbox")

        menu_text_6 = self.driver.find_element_by_id("shellmenu_5").text
        self.assertEqual(menu_text_6, "Deals")

        menu_text_7 = self.driver.find_element_by_id("l1_support").text
        self.assertEqual(menu_text_7, "Support")

        '''
        3. Go to Windows
        '''
        print("step: 3")
        self.driver.find_element_by_id("shellmenu_2").click()

        '''
        4. Once in Windows page, click on Windows 10 Menu
        '''
        print("step: 4")
        self.driver.find_element_by_id("c-shellmenu_54").click()

        '''
        5. Print all Elements in the dropdown
        '''
        print("step: 5")
        menu_elements = self.driver.find_elements_by_xpath("//*[@id=\"uhf-g-nav\"]/ul/li[2]/div/ul/li/a")
        for element in menu_elements:
            print(element.text)
        
        '''
        6. Go to Search next to the shopping cart
        '''
        print("step: 6")
        self.driver.find_element_by_id("search").click()

        '''
        7. Search for Visual Studio
        '''
        print("step: 7")
        self.driver.find_element_by_id("cli_shellHeaderSearchInput").send_keys("Visual Studio")
        self.driver.find_element_by_id("search").click()

        '''
        8. Print the price for the 3 first elements listed in Software result list
        '''
        print("step: 8")
        time.sleep(0.2) # woah, hol'up, sonic.
        self.driver.find_element_by_xpath("//*[@id=\"R1MarketRedirect-close\"]").click()
        self._menu_elements = self.driver.find_elements_by_xpath(
            "//*[@class=\"m-channel-placement-item f-wide f-full-bleed-image\"]/a/div[2]/div/div/span[3]/span[1]")

        print("Here is your search for Visual Studio")
        for i in range(3):
            print(self._menu_elements[i].get_attribute("content"))

        '''
        9. Store the price of the first one
        '''
        print("step: 9")
        self._menu_elements = self.driver.find_elements_by_xpath(
            "//*[@class=\"m-channel-placement-item f-wide f-full-bleed-image\"]/a/div[2]/div/div/span[3]/span[1]")
        self._price_of_first_element = self._menu_elements[0].get_attribute("content")

        '''
        10. Click on the first one to go to the details page
        '''
        print("step: 10")
        self.driver.find_element_by_xpath("//*[@class=\"m-channel-placement-item f-wide f-full-bleed-image\"]/a[1]").click()

        '''
        11. Once in the details page, validate both prices are the same
        '''
        print("step: 11")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.c-glyph"))).click()
        inside_price = self.driver.find_element_by_xpath("//*[@id=\"productPrice\"]/div/div/div/span")
        inside_price.click()
        self.assertEqual(inside_price.text, self._price_of_first_element)

        '''
        12. Click Add To Cart
        '''
        print("step: 12")
        # let that thing load
        time.sleep(.2)
        add_to_cart = self.driver.find_element_by_id("buttonPanel_AddToCartButton")
        actions = ActionChains(self.driver)
        actions.move_to_element(add_to_cart)
        actions.click(add_to_cart)
        actions.perform()

        '''
        13. Verify all 3 price amounts are the same
        '''
        print("step: 13")
        price_1 = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"store-cart-root\"]/div/div/div/section[1]/div/div/div/div/div/div[2]/div[2]/div[2]/div/span/span[2]/span"))).text

        price_2 = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"store-cart-root\"]/div/div/div/section[2]/div/div/div[1]/div/span[1]/span[2]/div/span/span[2]/span"))).text

        price_3 = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"store-cart-root\"]/div/div/div/section[2]/div/div/div[2]/div/span/span[2]/strong/span"))).text

        self.assertEqual(price_1, price_2)
        self.assertEqual(price_2, price_3)

        '''
        14. On the # of items dropdown select 20 and validate the Total amount is Unit Price * 20
        '''
        print("step: 14")
        select = self.driver.find_element_by_xpath("//*[@id=\"store-cart-root\"]/div/div/div/section[1]/div/div/div/div/div/div[2]/div[2]/div[1]/select")
        select.click()
        select_20 = self.driver.find_element_by_xpath(".//*/option[20]")
        select_20.click()
        total_price = WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/section/div[1]/div/div/div/div/div/section[2]/div/div/div[2]/div/span/span[2]/strong/span"), "$23,980.00"))
        # self.assertEqual("$23,980.00", total_price.text)

