import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = []
    start_urls = ['https://www.makemytrip.com/flight/search?itinerary=DEL-BLR-15/09/2024&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng']  # URL to scrape

    def __init__(self, *args, **kwargs):
        super(HotelSpider, self).__init__(*args, **kwargs)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'driver': self.driver})

    def parse(self, response):
        driver = response.meta['driver']
        driver.get(response.url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div'))
            )
        except:
            self.logger.error("Timeout waiting for page to load")
            driver.quit()
            return

        html = driver.page_source

        with open('page.html', 'w', encoding='utf-8') as file:
            file.write(html)

        driver.quit()

        self.logger.info("Page content saved successfully")
