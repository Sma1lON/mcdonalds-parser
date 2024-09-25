import json
import re
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

MENU_URL = "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html"

def clean_value(value):
    match = re.search(r'([\d.,]+)\s*(?:г|ккал|мл)', value)
    return match.group(1) if match else 'Невідомо'

def get_product_details(product_url, browser):
    page = browser.new_page()
    page.goto(product_url)
    time.sleep(2)
    html = page.content()
    page.close()
    product_soup = BeautifulSoup(html, 'html.parser')
    name = product_soup.find('span', class_='cmp-product-details-main__heading-title')
    name = name.get_text(strip=True) if name else 'Невідомий продукт'
    description_tag = product_soup.find('div', class_='cmp-product-details-main__description')
    description = description_tag.get_text(strip=True) if description_tag else 'Опис відсутній'

    try:
        nutrition_items = product_soup.find_all('li', class_='cmp-nutrition-summary__heading-primary-item')
        calories = clean_value(nutrition_items[0].get_text(strip=True)) if len(nutrition_items) > 0 else 'Невідомо'
        fats = clean_value(nutrition_items[1].get_text(strip=True)) if len(nutrition_items) > 1 else 'Невідомо'
        carbs = clean_value(nutrition_items[2].get_text(strip=True)) if len(nutrition_items) > 2 else 'Невідомо'
        proteins = clean_value(nutrition_items[3].get_text(strip=True)) if len(nutrition_items) > 3 else 'Невідомо'
    except (IndexError, AttributeError):
        calories, fats, carbs, proteins = 'Невідомо', 'Невідомо', 'Невідомо', 'Невідомо'

    try:
        secondary_items = product_soup.find_all('li', class_='label-item')
        unsaturated_fats = clean_value(secondary_items[0].get_text(strip=True)) if len(secondary_items) > 0 else 'Невідомо'
        sugar = clean_value(secondary_items[1].get_text(strip=True)) if len(secondary_items) > 1 else 'Невідомо'
        salt = clean_value(secondary_items[2].get_text(strip=True)) if len(secondary_items) > 2 else 'Невідомо'
        portion = clean_value(secondary_items[3].get_text(strip=True)) if len(secondary_items) > 3 else 'Невідомо'
    except (IndexError, AttributeError):
        unsaturated_fats, sugar, salt, portion = 'Невідомо', 'Невідомо', 'Невідомо', 'Невідомо'

    print(f"Назва: {name}")
    print(f"Опис: {description}")
    print(f"Калорійність: {calories}")
    print(f"Жири: {fats}")
    print(f"Вуглеводи: {carbs}")
    print(f"Білки: {proteins}")
    print(f"Насичені жири (НЖК): {unsaturated_fats}")
    print(f"Цукор: {sugar}")
    print(f"Сіль: {salt}")
    print(f"Порція: {portion}")

    return {
        'name': name,
        'description': description,
        'calories': calories,
        'fats': fats,
        'carbs': carbs,
        'proteins': proteins,
        'unsaturated_fats': unsaturated_fats,
        'sugar': sugar,
        'salt': salt,
        'portion': portion
    }

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(MENU_URL)
    time.sleep(2)
    html = page.content()
    page.close()
    product_soup = BeautifulSoup(html, 'html.parser')

    products = []
    for item in product_soup.find_all('li', class_='cmp-category__item'):
        product_link = item.find('a', class_='cmp-category__item-link')
        if product_link:
            product_url = f"https://www.mcdonalds.com{product_link['href']}"
            product_details = get_product_details(product_url, browser)
            products.append(product_details)
            time.sleep(1)

    with open('mcdonalds_products_full.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)

    print("Дані збережено в файл 'mcdonalds_products_full.json'.")
    browser.close()
