"""
downloadXkcd.py - download all xksd comics
from https://xkcd.com/
"""

import os, time
import requests
import bs4


base_url = 'https://xkcd.com'
upload_dir = 'xkcd'
img_selector = '#comic > img'
prev_selector = 'a[rel="prev"]'
images_to_load = 100


def parse_page(response, img_selector, prev_selectorl, url):
    """
    Return image and previous page urls.
    """
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    
    img_elem = soup.select(img_selector)
    if not img_elem:
        return None, None

    img_elem = img_elem[0]
    img_url = 'http:' + img_elem.get('src')

    prev_elem = soup.select(prev_selector)[0]
    prev_url = url + prev_elem.get('href')

    return img_url, prev_url

def download_image(img_url, path):
    """Download image from 'img_url' to directory set in 'path'"""
    
    image = requests.get(img_url)
    image.raise_for_status()
    
    os.makedirs(path, exist_ok=True)

    name = os.path.basename(img_url)
    load_path = os.path.join(path, name)
    with open(load_path, 'wb') as imgf:
        for chunk in image.iter_content(100_000):
            imgf.write(chunk)

images_loaded = unreadable = 0
prev_url = base_url

START_TIME = time.perf_counter()
#while not prev_url.endswith('#'):
for _ in range(images_to_load):
    response = requests.get(prev_url)
    response.raise_for_status()
    
    img_url, previous = parse_page(response, img_selector, 
                                   prev_selector, base_url)
    if img_url is None:
        unreadable += 1
        continue

    download_image(img_url, upload_dir)
    images_loaded += 1
    print(f"Comics loaded: {images_loaded}/{images_to_load}", end='\r')
    prev_url = previous

END_TIME = time.perf_counter()

print(f"Loaded -- {images_loaded} comics, skipped -- {unreadable}")
print(f"Time taken: {END_TIME - START_TIME} seconds.")

