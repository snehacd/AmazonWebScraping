import requests
from bs4 import BeautifulSoup
import json
import re
import time

def clean_text(text):
    # Remove non-printable characters using regular expression
    return re.sub(r'[^\x20-\x7E]', '', text)

def scrape_laptop_data(product_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(product_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') 

        # Extracting data from the page
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

        selling_price_element = soup.find('span', class_='a-price-whole')
        selling_price = clean_text(selling_price_element.get_text(strip=True)) if selling_price_element else 'Selling Price not found'

        discount_element = soup.find('span', class_='a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage')
        discount = clean_text(discount_element.get_text(strip=True)) if discount_element else 'Discount not found'

        weight_element = soup.find('td', string='Item Weight')
        weight = clean_text(weight_element.find_next_sibling('td').get_text(strip=True)) if weight_element else 'Weight not found'

        brand_element = soup.find('span', class_='a-size-base po-break-word')
        brand = clean_text(brand_element.get_text(strip=True)) if brand_element else 'Brand Name not found'

        image_element = soup.find('div', class_='imgTagWrapper')
        image_url = image_element.find('img')['src'] if image_element else 'Image URL not found'

        laptop_specification_element = soup.find('div', id='productOverview_feature_div')
        laptop_specification = clean_text(laptop_specification_element.get_text(strip=True)) if laptop_specification_element else 'Laptop Specification not found'

        # Map the extracted data with categories and subcategories
        mapped_data = {
            'Category': {
                'Laptop': {
                    'Subcategory': category,
                    'Data': {
                        'SKU ID': sku_id,
                        'Product Title': product_title,
                        'Product Name': product_name,
                        'Description': description,
                        'MRP': mrp,
                        'Selling Price': selling_price,
                        'Discount': discount,
                        'Weight': weight,
                        'Brand': brand,
                        'Image URL': image_url,
                        'Laptop Specification': laptop_specification
                    }
                }
            }
        }

        return mapped_data
    else:
        print(str(response.status_code)+' - Error loading the page')
        return None

def scrape_multiple_pages(base_url, num_pages):
    all_laptop_data = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}&page={page}"
        print(f"Scraping data from page {page}: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            product_links = soup.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
            for link in product_links:
                product_url = "https://www.amazon.in" + link['href']
                laptop_data = scrape_laptop_data(product_url)
                if laptop_data:
                    all_laptop_data.append(laptop_data)
                time.sleep(2)  # Add a delay to avoid overwhelming the server
        else:
            print(f"Failed to fetch page {page}")
    return all_laptop_data

# Base URL for searching laptops on Amazon
base_url = 'https://www.amazon.in/s?k=laptop&ref=nb_sb_noss_1'

# Number of pages to scrape
num_pages = 5

# Scrape data from multiple pages
laptop_data = scrape_multiple_pages(base_url, num_pages)

# Save the scraped data to a JSON file
with open('category.json', 'w', encoding='utf-8') as json_file:
    json.dump(laptop_data, json_file, ensure_ascii=False, indent=4)

print('Data has been saved to laptop_data.json')
