# scrape for all model
import time
import base64
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import psycopg2
from config import config


# used just for testing
def html_image():
    f = open("test.html", "w")
    f.write(
        """
        <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxISEhURExIQERUSFhcXFRYSFxUYGRMYFxMYFxUVFRYaHCggGBolHRcTIT0hJikuLi4uFx8zODMtNygtLisBCgoKDQ0ODg8PECsZFRktKy0yKzcrLTc3NysrKysrKys3LS0rKy0tKysrKysrKysrKysrKysrKysrKysrKysrK//AABEIAOEA4QMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABwMEBQYIAgH/xABKEAABAwIEAgQJCAYIBwEAAAABAAIDBBEFEiExBkEHE1FhFCIycYGRobHRUlNicoKSk8EjM0JEc6I0VGODssLS4RckQ7Pi8PEl/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAH/xAAVEQEBAAAAAAAAAAAAAAAAAAAAEf/aAAwDAQACEQMRAD8AnFERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEXwFfUBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAUd9MnExp6YUkWZ01V4pDPKbGTY2Ha4+KPtdi3zEa1kEUk0hysiY57z2NaLn3KEOFsRjqKmbHcReIoY32p2O1zSAeK1jRq/q220G7iTyKDLU+N19DDFT13/ACccjWNiqI2NPUWt+jlDLsadQL25HvLdw4e40FTXTUkYbURMYJG1EJBY0EC7JDe181wCOzbQlRtxb0iV1ZA+SmjFJRXydbKGufUE6dW0G4J30bewBu4KP8HxqrpnXp5poXOtcROsHW2zNtZ2/PtVHXSKCcH6aKqKJ8c8MdRKAOre09Xf+K0Aj7tuyw3Wd4S6XXyyNbWwMijldkZNCHhgfcXa8OJuBmbdwOl9RzEEsoqUFQx98j2vsbHKQbHsNtiqqAiIgIiICIiAiIgIiICIiAiIgIiIPhNtTooS4j6aJY6xzaVsD6Ztgx0j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" />
        """
    )


# Searching for a shoe
def scrape_goat_data_for_jordan_shoe(searched_shoe: str, goat_url: str) -> dict:
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
    shoe_list = output['Products']

    for shoe in shoe_list:
        shoe_dict = dict(
            shoe_name=searched_shoe,
            url=url,
            description=shoe['shortDescription'],
            brand=shoe['brand'],
            gender=shoe['gender'],
            color_way=shoe['colorway'],
            condition=shoe['condition'],
            retail=shoe['retailPrice'],
            lowest_asked=shoe['market']['lowestAsk'],
            annual_high=shoe['market']['annualHigh'],
            annual_low=shoe['market']['annualLow'],
            deadstock_range_high=shoe['market']['deadstockRangeHigh'],
            deadstock_range_low=shoe['market']['deadstockRangeLow'],
            shoe_image_url=shoe["media"]["imageUrl"],
            last_sale=shoe['market']['lastSale'],
            last_sale_date=shoe['market']['lastSaleDate']
        )
        insert_to_db(shoe_dict)


def scrape_goat_data_for_specific_shoe(query):
    url = f"https://ac.cnstrc.com/search/{query}?c=ciojs-client-2.29.2&key=key_XT7bjdbvjgECO5d8&i=c471ae65-6195-427f-b9ff-45fa149d2d8c&s=15&num_results_per_page=25&_dt=1661714126100"

    html = requests.get(url=url)
    output = json.loads(html.text)
    shoe_list = output['response']['results']
    for shoe in shoe_list:
        if shoe['data']['category'] != 'shoes':
            continue

        shoe_dict = dict(
            shoe_name=query,
            url=shoe['data']['image_url'],
            description=shoe['value'].replace("'", ''),
            color_way=shoe['data']['color'],
            condition=shoe['data']['product_condition'],
            retail=float(shoe['data']['retail_price_cents']) / 100,
            lowest_price=(float(shoe['data']['lowest_price_cents']) / 100),
            redirect_url=f'goat.com/sneakers/{shoe["data"]["slug"]}'
        )

        scrape_goat_data_by_size(shoe['data']['slug'], shoe_dict)
        insert_goat_data_to_db(shoe_dict)


# SEARCHING FOR SHOE SIZES ON GOAT
def scrape_goat_data_by_size(shoe_slug, shoe_dict) -> dict:
    # f'https://www.goat.com/_next/data/Jvg3JY7OdL44a31avkLy_/en-us/sneakers/{shoe_slug}.json?pageSlug=sneakers&productSlug={shoe_slug}'

    # CAUTION: Make sure this url is the same found in developer tools
    # May have to clear cookies to get the url
    url = f'https://www.goat.com/_next/data/A2btdOVixyBfdMc5h7uVz/en-us/sneakers/{shoe_slug}.json?pageSlug=sneakers&productSlug={shoe_slug}'

    result = requests.get(url)
    output = json.loads(result.text)
    offers = output['pageProps']['offers']['offerData']

    size_prices = {float(offers[i]['size']) : float(offers[i]['price']) for i in range(len(offers))}
    shoe_dict.update({'size_prices': size_prices})
    return shoe_dict

# connect to db and insert data
def insert_goat_data_to_db(shoe: dict):
    """
    :param shoe:
    :return:
    """
    sql = """INSERT INTO shoe_data_goat (shoe_name, description, url, retail, lowest_asked, size, size_price, redirect_url,
    condition, color_way) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING data_instance_id;"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        for shoe_size in shoe['size_prices']:
            execute = cur.execute(sql, (shoe['shoe_name'], shoe['description'], shoe['url'],
                                        shoe['retail'], shoe['lowest_price'],
                                        shoe_size, shoe['size_prices'][shoe_size], shoe['redirect_url'],
                                        shoe['condition'], shoe['color_way']))

        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return True


# connect to db and insert data
def insert_to_db(shoe: dict):
    """
    :param shoe:
    :return:
    """
    sql = """INSERT INTO shoe_data (shoe_name, url, description, brand, gender, color_way, condition, retail, lowest_asked, annual_high,
    annual_low, deadstock_range_high, deadstock_range_low, last_sale, last_sale_date) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING data_instance_id;"""
    sql_2 = """ UPDATE sp_shoe SET image=%s, url=%s WHERE shoe_name=%s
    """
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
        execute = cur.execute(sql, (shoe['shoe_name'], shoe['url'], shoe['description'], shoe['brand'], shoe['gender'],
                                    shoe['color_way'], shoe['condition'], shoe['retail'], shoe['lowest_asked'],
                                    shoe['annual_high'], shoe['annual_low'], shoe['deadstock_range_high'],
                                    shoe['deadstock_range_low'], shoe['last_sale'], shoe['last_sale_date']))
        # execute UPDATE
        base64_image = base64.b64encode(requests.get(shoe['shoe_image_url']).content)
        execute_2 = cur.execute(sql_2, (base64_image, shoe['url'], shoe['shoe_name']))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# ADRIAN PART
def _get_all_shoe_names() -> list:
    """ connect to db to fetch goat specific url

    ex: select goat_url from sp_shoe where shoe_name = ''

    :return:
    """
    sql = """SELECT shoe_name FROM sp_shoe"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        execute = cur.execute(sql)
        # commit the changes to the database
        response = [r[0] for r in cur.fetchall()]
        # close communication with the database
        cur.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def _add_image_to_db(image: str):
    pass


def clear_data_from_database():
    """ This clears data from sp_shoe_data, to clear any redundant data and fetch new data.

    :return: not`hing
    """
    pass


def run_scrape():
    """

    :return:
    """
    # clear_data_from_database()
    shoe_query_list = _get_all_shoe_names()
    for shoe in shoe_query_list:
        scrape_stockx_data_for_specific_shoe(shoe)
        scrape_goat_data_for_specific_shoe(shoe)
        time.sleep(60)


if __name__ == '__main__':
    # Scrape brand of shoes on goat website
    # scrape_goat_data_for_jordan_shoe("Air Jordan 3 Retro 'Dark Iris'", "https://www.goat.com/brand/air-jordan")
    # Scrape from nike website
    # scrape_nike_data_for_specific_shoe("Air Jordan 12 Retro", "https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok")
    # Scrape from stockx website
    # html_image()
    run_scrape()
    # this = _get_all_shoe_names()
    # scrape_stockx_data_for_specific_shoe("Adidas Yeezy Foam RNR Onyx")
    # insert_to_db(scrape_stockx_data_for_specific_shoe("Air Jordan Dunks"))
    # Scrape a shoe from goat website
    # print(scrape_goat_data_for_specific_shoe("Air Jordan 3 Retro 'Dark Iris'"))
    # scrape_goat_data_for_jordan_shoe("Air Jordan 3 Retro 'Dark Iris'", "https://www.goat.com/brand/air-jordan")
    print("Finished")
