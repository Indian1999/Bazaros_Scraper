from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options = options)
#driver.get("https://bazarosonline.hu/roni-trend-hu/")
driver.get("https://bazarosonline.hu/lumea-pungilor-hu/")

"""
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
"""

results = driver.find_elements(By.CSS_SELECTOR, "div.ut2-gl__body")

print(len(results))

products = []

for result in results:
    product = {}
    product["title"] = result.find_element(By.CSS_SELECTOR, ".product-title").text
    product["price"] = result.find_element(By.CSS_SELECTOR, ".ty-price-num").text
    product["img-url"] = result.find_element(By.TAG_NAME, "img").get_attribute("src")
    product["url"] = result.find_element(By.CSS_SELECTOR, "a.product_icon_lnk").get_attribute("href")
    product["price-per-unit"] = result.execute_script("""
            return Array.from(document.querySelectorAll('span')).find(el => {
                const style = window.getComputedStyle(el);
                return style.color === 'rgb(255, 0, 0)' && 
                       style.fontSize === '16px' &&
                       style.fontWeight === '700' && 
                       style.paddingTop === '8px';
            });
            """).text
    products.append(product)

with open("products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=4, ensure_ascii=False)

