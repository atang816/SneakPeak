import requests
from bs4 import BeautifulSoup
import base64


result = requests.get("https://www.goat.com/brand/air-jordan") # stockx.com is blocked
soup = BeautifulSoup(result.content, "lxml")

shoes_list = []
# Get shoes name
shoes_grid = soup.find_all('div', class_='GridCellProductInfo__Name-sc-17lfnu8-3 dwAEbs')


for shoe_name in shoes_grid:
    shoes_list.append(shoe_name.text)
    print(shoe_name.text)

shoes_prices = soup.find_all('div', class_="GridCellProductInfo__Price-sc-17lfnu8-6 tIvOr")

for shoe_price in shoes_prices:
    print(shoe_price.text)

#
# shoes_images = soup.find_all('img')
#
# for shoe_image in shoes_images:
#     print(shoe_image.attrs["src"])

#links = soup.find_all("a") # Print all the links of page

# for link in links:
#      if "Jordan" in link.text:
#          print(link)
#          print(link.attrs['href'])


#<div data-qa="grid_cell_product_price" class="GridCellProductInfo__Price-sc-17lfnu8-6 tIvOr"><span>$230</span></div>

#<img alt="Air Jordan 5 Retro 'Racer Blue'"
# data-qa="grid_cell_product_image"
# sizes="(min-width: 768px) 25vw, 50vw"
# class="sc-eCApnc intbbb Image__StyledImage-sc-1qwz99p-0 gJfnCb GridCellProductImage__Image-msqmrc-1 efCEgn"
# src="https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=750" srcset="https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=50 50w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=75 75w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=100 100w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=120 120w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=150 150w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=200 200w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=240 240w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=300 300w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=360 360w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=375 375w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=400 400w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=500 500w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=600 600w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=700 700w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=750 750w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=800 800w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=850 850w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=900 900w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=950 950w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=1000 1000w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=1250 1250w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=1500 1500w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=1600 1600w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=1800 1800w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=2000 2000w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=2200 2200w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=2400 2400w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=2600 2600w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=3000 3000w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=3200 3200w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=3500 3500w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=3700 3700w, https://image.goat.com/transform/v1/attachments/product_template_pictures/images/066/685/865/original/824865_00.png.png?action=crop&amp;width=4000 4000w">