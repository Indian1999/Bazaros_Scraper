from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import json
import math


def remove_non_digit(string:str) -> int:
    """Removes any non-digit characters from the string and returns the remainder as an integer."""
    new_string = ""
    for char in string:
        if char.isdigit():
            new_string += char
    return int(new_string)

products = []

options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

driver = webdriver.Chrome(options = options)

driver.get("https://bazarosonline.hu/alex-store-hu/")
num_of_products = remove_non_digit(driver.find_element(By.CSS_SELECTOR, "span.ty-mainbox-title__right").text)
num_of_pages = math.ceil(num_of_products / 50)

num_of_pages = 3
for page_num in range(1, num_of_pages + 1):
    print(f"Opening https://bazarosonline.hu/alex-store-hu/?page={page_num}...")
    driver = webdriver.Chrome(options = options)

    driver.get(f"https://bazarosonline.hu/alex-store-hu/?page={page_num}")

    results = driver.find_elements(By.CSS_SELECTOR, "div.ut2-gl__body")


    for result in results:
        try:
            product = {}
            product["title"] = result.find_element(By.CSS_SELECTOR, ".product-title").text
            product["price"] = remove_non_digit(result.find_element(By.CSS_SELECTOR, ".ty-price-num").text)
            product["img-url"] = result.find_element(By.TAG_NAME, "img").get_attribute("src")
            product["url"] = result.find_element(By.CSS_SELECTOR, "a.product_icon_lnk").get_attribute("href")
            product["page"] = page_num
            
            dropdown = result.find_element(By.CSS_SELECTOR, "select[name*='amount']")
            
            try:
                select = Select(dropdown)
                quantities = [int(option.get_attribute("value")) for option in select.options]
                product["minimum"] = min(quantities)
            except Exception as e:
                print(e)

            ppu_elem = driver.execute_script("return arguments[0].querySelectorAll('span');", result)
            ppu = None
            for elem in ppu_elem:
                style = driver.execute_script("""
                let elem = arguments[0]; 
                    return {
                        color: window.getComputedStyle(elem).getPropertyValue('color'),
                        fontSize: window.getComputedStyle(elem).getPropertyValue('font-size'),
                        fontWeight: window.getComputedStyle(elem).getPropertyValue('font-weight'),
                        paddingTop: window.getComputedStyle(elem).getPropertyValue('padding-top')
                    };
                    """, elem)
                if (style["color"] == "rgb(255, 0, 0)" and 
                    style["fontSize"] == "16px" and
                    style["fontWeight"] == "700" and
                    style["paddingTop"]== "8px"):
                    ppu = elem.text
                    break
            if ppu:
                product["price-per-unit"] = remove_non_digit(ppu)
            else:
                product["price-per-unit"] = product["price"]
            products.append(product)
        except Exception as ex:
            print(f"ERROR: {ex}")

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)

