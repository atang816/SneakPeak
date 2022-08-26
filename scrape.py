# scrape for all model
# test
from datetime import datetime



def scrape_data_for_specific_shoe(name: str, goat_url: str)-> dict:
    # {
    #     'air jordan 1 military black': {
    #      'size_chart': {'10.5': 300,
    #                      '11': 400},
    #      'gender': 'M',
    #      'date': _convert_string_date_to_datetime('May')
    #
    #     }
    # }
    pass

# connect to db and insert data
def insert_to_db(shoe: dict):
    """

    :param shoe:
    :return:
    """
    pass

def _convert_string_date_to_datetime(date: str) -> datetime:
    """ Converts string date to datetime format

    :param date:
    :return:
    """
    pass

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