from selenium_driver.product_parser import SMMParser
from multiprocessing import Process, Pool
from time import sleep
from flask import Flask, jsonify
import re

app = Flask(__name__)
def start(page_url: str):
    parser = SMMParser()
    html = parser.get(url=page_url)
    return html
    # product_links = parser.get_product_links()
    # print(product_links)
    # for product_link in product_links:
    #     slug = re.search("slug=(.*)&merchantId",
    #             product_link,
    #             ).group(1)
    #     product_link = f"https://megamarket.ru/catalog/details/{slug}/#?details_block=prices"
    #     html = parser.get_page_html(product_url=product_link)
    #     parser.parse_page_html(html=html)
    
    parser.quit_()

@app.route("/hello", methods=["GET"])
def main():
    # category_urls = ["https://megamarket.ru/shop/tehnic/catalog/elektronika/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/kompyutery-i-komplektuyushie/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/bytovaya-tehnika/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/tovary-dlya-geymerov/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/stroitelstvo-i-remont/",
    #                  "https://megamarket.ru/shop/tehnic/catalog/sport-i-aktivnyy-otdyh/"]
    page_urls = [f"https://megamarket.ru/shop/tehnic/catalog/elektronika/#?page={i}" for i in range(1, 19 + 1)]
    #p = Pool(processes=1)
    # p.map(start, page_urls)
    start(page_urls[0])


if __name__ == "__main__":
    app.run(debug=True)
