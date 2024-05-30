# The below code is to Extract details of single page 
import requests
from bs4 import BeautifulSoup
import json
import re

def clean_text(text):
    # Remove non-printable characters using regular expression
    return re.sub(r'[^\x20-\x7E]', '', text)

url = 'https://www.amazon.in/Dell-i5-1135G7-Processor-Spill-Resistant-Keyboard/dp/B0C15CDKTN/ref=sr_1_1_sspa?crid=28L3WDUP98Y2C&keywords=laptops&qid=1706346704&sprefix=laptops%2Caps%2C275&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    sku_id_element = soup.find('td', class_='a-size-base prodDetAttrValue')
    sku_id = clean_text(sku_id_element.get_text(strip=True)) if sku_id_element else 'SKU ID not found'

    product_title_element = soup.find('span', id='productTitle', class_='a-size-large product-title-word-break')
    product_title = clean_text(product_title_element.get_text(strip=True)) if product_title_element else 'Product Title not found'

    product_name_element = soup.find('span', id='productTitle', class_='a-size-large product-title-word-break')
    product_name = clean_text(product_name_element.get_text(strip=True)) if product_name_element else 'Product Name not found'

    description_element = soup.find('div', id='feature-bullets')
    description = clean_text(description_element.get_text(strip=True)) if description_element else 'Description not found'

    category_element = soup.find('p', class_='a-text-left a-size-base')
    category = clean_text(category_element.get_text(strip=True)) if category_element else 'Category not found'

    mrp_element = soup.find('span', class_='a-price a-text-price')
    mrp_text = clean_text(mrp_element.get_text(strip=True)) if mrp_element else 'MRP not found'

    # Split the MRP text into two equal parts and take the first part
    mrp_length = len(mrp_text)
    mrp = mrp_text[:mrp_length // 2]

    print("First half of MRP:", mrp)

    selling_price_element = soup.find('span', class_='a-price-whole')
    selling_price = clean_text(selling_price_element.get_text(strip=True)) if selling_price_element else 'Selling Price not found'

    discount_element = soup.find('span', class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage')
    discount = clean_text(discount_element.get_text(strip=True)) if discount_element else 'Discount not found'

    weight_element = soup.find('td', class_='a-size-base prodDetAttrValue')
    weight = clean_text(weight_element.get_text(strip=True)) if weight_element else 'Weight not found'

    brand_element = soup.find('span', class_='a-size-base po-break-word')
    brand = clean_text(brand_element.get_text(strip=True)) if brand_element else 'Brand Name not found'

    image_element = soup.find('div', class_='imgTagWrapper')
    image_url = image_element.find('img')['src'] if image_element else 'Image URL not found'

    laptop_specification_element = soup.find('div', id='productOverview_feature_div')
    laptop_specification = clean_text(laptop_specification_element.get_text(strip=True)) if laptop_specification_element else 'Laptop Specification not found'

    product_data = {
        'SKU ID': sku_id,
        'Product Title': product_title,
        'Product Name': product_name,
        'Description': description,
        'Category': category,
        'MRP': mrp,
        'Selling Price': selling_price,
        'Discount': discount,
        'Weight': weight,
        'Brand': brand,
        'Image URL': image_url,
        'Laptop Specification': laptop_specification
    }

    with open('product_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(product_data, json_file, ensure_ascii=False, indent=4)

    print('Data has been saved to product_data.json')
else:
    print(str(response.status_code)+' - Error loading the page')
