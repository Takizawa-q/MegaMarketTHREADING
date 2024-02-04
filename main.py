from selenium_driver.product_parser import SMMParser
from multiprocessing import Process, Pool
from webdriver_manager.chrome import ChromeDriverManager

ChromeDriverManager().install()
from time import sleep
import re

def start(page_url: str):
    parser = SMMParser()
    parser.get(url=page_url)
    product_links = parser.get_product_links()
    print(product_links)
    for product_link in product_links:
        slug = re.search("slug=(.*)&merchantId",
                product_link,
                ).group(1)
        product_link = f"https://megamarket.ru/catalog/details/{slug}/#?details_block=prices"
        html = parser.get_page_html(product_url=product_link)
        parser.parse_page_html(html=html)

    parser.quit_()


def main():
    # category_urls = ["https://megamarket.ru/shop/tehnic/catalog/elektronika/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/kompyutery-i-komplektuyushie/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/bytovaya-tehnika/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/tovary-dlya-geymerov/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/stroitelstvo-i-remont/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/sport-i-aktivnyy-otdyh/"]
    page_urls = [f"https://megamarket.ru/shop/tehnic/catalog/elektronika/#?page={i}" for i in range(1, 19 + 1)]
    p = Pool(processes=1)
    p.map(start, page_urls)


if __name__ == "__main__":
    main()
