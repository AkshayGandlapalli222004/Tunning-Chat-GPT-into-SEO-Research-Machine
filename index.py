import requests
from bs4 import BeautifulSoup
import json
import re


def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_json_data(script_content):
    try:
        json_data_match = re.search(r'webPixelsManagerAPI.publish\("collection_viewed", (\{.*?\})\);', script_content)
        if json_data_match:
            json_data = json.loads(json_data_match.group(1))
            return json_data
        else:
            print("JSON data match not found in script content")
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def extract_product_info(json_data):
    product_info = []
    for variant in json_data["collection"]["productVariants"]:
        product_url = f"https://www.amazon.in/?tag=msndeskabkin-21&ref=pd_sl_7qhce485bd_e&adgrpid=1322714095756137&hvadid=82669897710514&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=148859&hvtargid=kwd-82670512756912:loc-90&hydadcr=14453_2334184{variant['product']['url']}"
        image_url = f"https:{variant['image']['src']}"
        price = variant['price']['amount']
        product_info.append({
            "title": variant['product']['title'],
            "url": product_url,
            "image_url": image_url,
            "price": f"€{price:.2f}"
        })
    return product_info


# URL of the category page
category_url = "https://www.amazon.in/?tag=msndeskabkin-21&ref=pd_sl_7qhce485bd_e&adgrpid=1322714095756137&hvadid=82669897710514&hvnetw=o&hvqmt=e&hvbmt=be&hvdev=c&hvlocint=&hvlocphy=148859&hvtargid=kwd-82670512756912:loc-90&hydadcr=14453_2334184"


# Fetch the HTML content of the category page
category_page_html = get_html(category_url)
if category_page_html:
    soup = BeautifulSoup(category_page_html, 'html.parser')
    script_tag = soup.find('script', {'id': 'web-pixels-manager-setup'})
    if script_tag:
        json_data = extract_json_data(script_tag.string)
        if json_data:
            product_info = extract_product_info(json_data)
            for info in product_info:
                print(info)
        else:
            print("Failed to extract JSON data from script")
    else:
        print("Script tag with the specified ID not found")
else:
    print("Failed to fetch category page HTML")
