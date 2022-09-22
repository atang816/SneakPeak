# scrape for all model
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import psycopg2
from config import config

# Searching for a shoe
def scrape_goat_data_for_jordan_shoe(searched_shoe: str, goat_url: str)-> dict:
    # {
    #     'air jordan 1 military black': {
    #      'size_chart': {'10.5': 300,
    #                      '11': 400},
    #      'gender': 'M',
    #      'date': _convert_string_date_to_datetime('May')
    #
    #     }
    # }

    result = requests.get(goat_url)
    soup = BeautifulSoup(result.content, "lxml")
    shoes_names = soup.find_all('div', class_='GridCellProductInfo__Name-sc-17lfnu8-3 dEjkaY')
    shoes_prices = soup.find_all('div', class_="GridCellProductInfo__Price-sc-17lfnu8-6 loFpaM")
    shoes_dates = soup.find_all('div', class_="GridCellProductInfo__Year-sc-17lfnu8-2 eRJigJ")

    print("shoe name list: " + str(len(shoes_names)))
    print("shoe price list: " + str(len(shoes_prices)))
    print("shoe dates list: " + str(len(shoes_dates)))

    for i in range(len(shoes_names)):
        if shoes_names[i].text == searched_shoe:
            print(shoes_names[i].text)
            print(shoes_prices[i].text)
            print(shoes_dates[i].text)
            break

    shoes_dict = {
    }

    pass

def scrape_nike_data_for_specific_shoe(searched_shoe: str, nike_url: str):

    result = requests.get(nike_url)
    soup = BeautifulSoup(result.content, "lxml")
    shoes_names = soup.find_all('div', class_='product-card__title')
    shoes_prices = soup.find_all('div', class_="product-price is--current-price css-11s12ax")
    for i in range(len(shoes_names)):
        print(shoes_names[i].text)
        print(shoes_prices[i].text)

        """if shoes_names[i].text == searched_shoe:
            print(shoes_names[i].text)
            print(shoes_prices[i].text)
            break"""

    pass

def scrape_stockx_data_for_specific_shoe(searched_shoe: str):

    url = f'https://stockx.com/api/browse?_search={searched_shoe}'

    headers = {
        'accept': 'application/json',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-GB,en;q=0.9',
        'app-platform': 'Iron',
        'referer': 'https://stockx.com/en-gb',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    html = requests.get(url=url, headers=headers)
    output = json.loads(html.text)

    title = output['Products'][0]['title']
    url = "https://stockx.com/" + output['Products'][0]['shortDescription']
    shoe_model = output['Products'][0]['brand']
    img = output['Products'][0]['media']["smallImageUrl"]
    retail_price = output['Products'][0]["retailPrice"]
    size = output['Products'][0]['market']['lowestAskSize']
    gender = output['Products'][0]["gender"][0]
    color = output['Products'][0]["colorway"]
    condition = output['Products'][0]["condition"]

    return {
        "shoe_name": title,
        "url": url,
        "shoe_model": shoe_model, # Do we just want the brand?
        "cost": retail_price, # Which price do we want (retail, lowestAskPrice) # Add more columns for the prices
        "size": size, # Only able to get lowestAskSize
        "gender_or_identity": gender,
        "color": color,
        "condition": condition,
        "image": img

    }

def scrape_goat_data_for_specific_shoe(query):
    url = f"https://ac.cnstrc.com/search/{query}?c=ciojs-client-2.29.2&key=key_XT7bjdbvjgECO5d8&i=c471ae65-6195-427f-b9ff-45fa149d2d8c&s=15&num_results_per_page=25&_dt=1661714126100"

    html = requests.get(url=url)
    output = json.loads(html.text)

    return output['response']['results'][0]

# connect to db and insert data
def insert_to_db(shoe: dict):
    """

    :param shoe:
    :return:
    """

    sql = """INSERT INTO shoe_data (shoe_name, url, shoe_model, cost, size, gender_or_identity, color, condition) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING data_instance_id;"""
    conn = None
    shoes_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (shoe["shoe_name"], shoe["url"], shoe["shoe_model"], shoe["cost"], shoe["size"], shoe["gender_or_identity"], shoe["color"], shoe["condition"]))
        # get the generated id back
        shoes_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return shoes_id

    pass

def _convert_string_date_to_datetime(date: str) -> datetime:
    """ Converts string date to datetime format

    :param date:
    :return:
    """
    pass


# ADRIAN PART
def _get_all_shoes_and_info(name: str) -> dict:
    """ connect to db to fetch goat specific url

    ex: select goat_url from sp_shoe where shoe_name = ''

    :return:
    """
    pass

def clear_data_from_database():
    """ This clears data from sp_shoe_data, to clear any redundant data and fetch new data.

    :return: nothing
    """
    pass

def run_scrape():
    """

    :return:
    """
    pass



if __name__ == '__main__':

    # Scrape brand of shoes on goat website
    #scrape_goat_data_for_jordan_shoe("Air Jordan 3 Retro 'Dark Iris'", "https://www.goat.com/brand/air-jordan")

    # Scrape from nike website
    #scrape_nike_data_for_specific_shoe("Air Jordan 12 Retro", "https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok")

    # Scrape from stockx website
    print(scrape_stockx_data_for_specific_shoe("Air Jordan Dunks"))
    insert_to_db(scrape_stockx_data_for_specific_shoe("Air Jordan Dunks"))
    print("Finished")
    # Scrape a shoe from goat website
    #print(scrape_goat_data_for_specific_shoe("Air Jordan 3 Retro 'Dark Iris'"))
    #scrape_goat_data_for_jordan_shoe("Air Jordan 3 Retro 'Dark Iris'", "https://www.goat.com/brand/air-jordan")

