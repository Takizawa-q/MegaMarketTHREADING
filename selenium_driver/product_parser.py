from .browser import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import time

class SMMParser(Driver):

    def __init__(self):
        super().__init__()

    def quit_(self):
        self.driver.close()
        self.driver.quit()
    
    def get(self, url: str):
        self.driver.get(url)
        return self.driver.page_source
    def get_product_links(self):
        html = self.driver.page_source
        soup = BeautifulSoup(str(html), "html.parser")
        product_links = []
        for pre_product_link in soup.find_all("div", class_='catalog-item catalog-item-desktop ddl_product'):
            product_links.append("https://megamarket.ru" + pre_product_link.find("a").get('href'))
        if len(product_links) == 0:
            for pre_product_link in soup.find_all("div", class_='item-title'):
                product_links.append("https://megamarket.ru" + pre_product_link.find("a").get('href'))
        print(len(product_links))
        return product_links
    
    def parse_page_html(self, html):
        soup = BeautifulSoup(str(html), "lxml")
        # buybox
        try:
            pre = soup.find(
                "div", class_="money-bonus pdp-sales-block__bonus lg pdp-sales-block__bonus_active")
            buybox_cashback = pre.find(
                "span", class_="bonus-amount").text.strip().replace("₽", "").replace(" ", "")
        except:
            try:
                pre = soup.find("div", class_="pdp-cashback-table__row")
                buybox_cashback = pre.find(
                    "span", class_="bonus-amount").text.strip().replace("₽", "").replace(" ", "")
            except:
                buybox_cashback = "-"
        try:
            buybox_seller_name = soup.find(
                "span", class_="pdp-merchant-rating-block__merchant-name").text
        except:
            try:
                buybox_seller_name = soup.find(
                    "a", class_="pdp-offer-block__merchant-link").text
            except:
                buybox_seller_name = "-"
        try:
            try:
                buybox_price = soup.find(
                    "span", class_="pdp-sales-block__price-final").text.strip().replace("₽", "").replace(" ", "")
            except:
                try:
                    buybox_price = soup.find(
                        "span", class_="sales-block-offer-price__price-final").text.strip().replace("₽", "").replace(" ", "")
                except Exception:
                    buybox_price = "-"

        except Exception:
            buybox_price = "-"

        try:
            buybox_cashback_percent = round(
                (float(buybox_cashback) / float(buybox_price)) * 100, 2)
        except:
            buybox_cashback_percent = 0
        try:
            buybox_total_price = float(buybox_price) - float(buybox_cashback)
        except:
            buybox_total_price = buybox_price

        try:
            category = soup.find(
                "span", class_="categories__category-item_title").text.strip()
        except:
            category = "-"
        try:
            name = soup.find("h1", {"itemprop": "name"}).text.strip()
        except Exception:
            name = "-"
        try:
            articul = ""
            lis = soup.find_all("li", {"itemprop": "additionalProperty"})
            for li in lis:

                if "Код" in str(li.find("span", {"itemprop": "name"})):
                    articul = li.find("span", {"itemprop": "value"}).text.replace(
                        " ", "").strip()
                    break
        except:
            articul = ""
        # SELLERS INFOS
        try:
            orders_count = soup.find(
                "span", class_="pdp-tab-inner-item__counter counter").text.strip().replace(" ", "")
        except:
            orders_count = "-"
        try:
            seller_boxes = []
            pre = soup.find(
                "div", class_="product-offers product-offers_no-border pdp-prices__offers")
            all_sellers_boxes = pre.find_all(
                "div", {"itemscope": "itemscope", "itemprop": "offers"})
            for x, seller_box in enumerate(all_sellers_boxes):
                if x > 20:
                    break

                seller_box_price, seller_box_cashback, seller_box_cashback_percent, seller_box_total_price, seller_box_name = "", "", "", "", ""
                try:
                    seller_box_name = seller_box.find(
                        "span", class_="pdp-merchant-rating-block__merchant-name").text.strip().replace(" ", "")
                except Exception as e:
                    try:
                        seller_box_name = seller_box.find("div", class_="product-offer-name__name").text.strip(
                        ).replace(" ", "").replace("₽", "").replace(r"\xa0", "")
                    except:
                        seller_box_name = ""

                try:
                    seller_box_price = int(seller_box.find(
                        "span", class_="product-offer-price__amount product-offer-price__amount_discount").text.strip().replace(" ", "").replace("₽", "").replace("\xa0", ""))
                except:
                    try:
                        seller_box_price = int(seller_box.find(
                            "span", class_="product-offer-price__amount").text.strip().replace(" ", "").replace("₽", "").replace("\xa0", ""))
                    except:
                        seller_box_price = ""
                try:
                    seller_box_cashback = seller_box.find(
                        "span", class_="bonus-amount").text.strip().replace(" ", "").replace("₽", "").replace("\xa0", "")
                except:
                    seller_box_cashback = ""
                try:
                    seller_box_cashback_percent = round(
                        (float(seller_box_cashback) / float(seller_box_price) * 100), 2)
                except:
                    seller_box_cashback_percent = 0
                try:
                    seller_box_total_price = float(
                        seller_box_price) - float(seller_box_cashback)
                except:
                    seller_box_total_price = seller_box_price
                seller_boxes.append([seller_box_name, seller_box_price, seller_box_cashback,
                                    seller_box_cashback_percent, seller_box_total_price])
        except Exception as e:
            seller_boxes = []
        print(seller_boxes, time())

    def get_page_html(self, product_url: str):
        tabs_open = self.driver.window_handles
        self.driver.get_window_position()['x'] == 0
        self.driver.get_window_position()['y'] == 0

        self.driver.get(product_url)
        self.driver.switch_to.new_window('tab')
        self.driver.close()
        self.driver.switch_to.window(tabs_open[0])

        actions = ActionChains(self.driver)
        
        self.scroll_down_()
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "pdp-cashback-table__row")))
        except Exception as e:
            try:
                wait.until(EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'money-bonus sm money-bonus_loyalty pdp-cashback-table__money-bonus')))
            except:
                pass
        return self.driver.page_source

    def scroll_down_(self):
        actions = ActionChains(self.driver)
        for _ in range(500):
            actions.send_keys(Keys.PAGE_DOWN).perform()
    
