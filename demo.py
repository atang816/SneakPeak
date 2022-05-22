import requests
from bs4 import BeautifulSoup
import psycopg2
from config import config

def getNames(soup):
    shoes_list = []
    # Get shoes name
    shoes_grid = soup.find_all('div', class_='GridCellProductInfo__Name-sc-17lfnu8-3 hUVYBh')


    for shoe_name in shoes_grid:
        shoes_list.append(shoe_name.text)
        print(shoe_name.text)

    return shoes_list

def getPrices(soup):
    prices_list = []
    shoes_prices = soup.find_all('div', class_="GridCellProductInfo__Price-sc-17lfnu8-6 KlQNy")

    for shoe_price in shoes_prices:
        prices_list.append(shoe_price.text)
        print(shoe_price.text)

    return prices_list

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def insert_shoe(name, price, image):
    """ insert a new vendor into the vendors table """

    sql = """INSERT INTO shoes (name, price, image) VALUES(%s, %s, %s) RETURNING shoes.id;"""
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
        without_dollar_sign = price.replace('$', "")
        cur.execute(sql, (name,int(without_dollar_sign),image,))
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

if __name__ == '__main__':

    result = requests.get("https://www.goat.com/brand/air-jordan")  # stockx.com is blocked
    soup = BeautifulSoup(result.content, "lxml")

    names_list = getNames(soup)
    prices_list = getPrices(soup)
    connect()

    print(names_list[0])
    print(prices_list[0])

    insert_shoe(names_list[2], prices_list[2], "none")

# shoes_images = soup.find_all('img')
#
# for shoe_image in shoes_images:
#      print(shoe_image.attrs["src"])

#links = soup.find_all("a") # Print all the links of page

# for link in links:
#      if "Jordan" in link.text:
#          print(link)
#          print(link.attrs['href'])