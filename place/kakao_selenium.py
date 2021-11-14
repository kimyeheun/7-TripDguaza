import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import os.path

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]


class kakaoCrawler():
    def __init__(self):
        # 드라이버 자동 설치
        chromedriver_autoinstaller.install(True)
        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(
            os.getcwd() + f'\{chrome_ver}\chromedriver.exe', options=option)
        self.driver.implicitly_wait(5)

    # Get place info

    def place_detail_crawl(self, id):
        # access
        url = 'https://place.map.kakao.com/'
        self.driver.get(url + str(id))
        kakao_place_id = id
        title = self.driver.find_elements_by_class_name("tit_location")[1].text

        # category
        try:
            category = self.driver.find_element_by_class_name(
                "txt_location").text
        except:
            category = ""
        # location
        try:
            location = self.driver.find_element_by_class_name(
                "txt_address").text
        except:
            location = ""
        # businessHours
        try:
            businessHours = self.driver.find_element_by_class_name(
                "txt_operation").text
        except:
            businessHours = ""
        # menu
        try:
            menu = []
            try:
                self.driver.find_element_by_class_name("open_txt").click()
            except:
                pass
            menuName = self.driver.find_elements_by_class_name("loss_word")
            menuName = [i.text for i in menuName]
            priceData = self.driver.find_elements_by_class_name("price_menu")
            price = [i.text for i in priceData]
            for m, p in zip(menuName, price):
                menu.append({"name": m, "price": p})
        except:
            menu = []

        res = {
            'kakao_place_id': kakao_place_id,
            'title': title,
            'category': category,
            'location': location,
            'businessHours': businessHours,
            # 'description': description,
            # 'imageSrc': imageSrc,
            'menu': menu,
        }
        return res
