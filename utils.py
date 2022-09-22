import sqlite3


def get_value_from_database(sql: str) -> list[dict]:
    """
    This function establishes a database connection and gets values as requested
    Эта функция устанавливает соединение с базой данных и получает значения по запросу

    Args:
        sql(str): sql request

    Returns:
        list(dict): sqlite table netflix.db
    """

    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

        return result


def get_value_by_title(title: str) -> dict:
    """
    This function passes the SQL request in function get_value_from_database
    and returns the movie by title

    Эта функция передаёт SQL запрос в функцию get_value_from_database
    и возвращает фильм по его названию

    Args:
        title(str): film's title

    Returns:
        dict: information about film (title, country, release year, listed in, description)
    """

    sql = f'''
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE title = '{title}'
        ORDER BY release_year desc, date_added desc
        LIMIT 1'''

    result = get_value_from_database(sql)

    for item in result:
        return dict(item)


def get_value_by_release_year(year: int, next_year: int) -> list[dict]:
    """
    This function passes the SQL request in function get_value_from_database
    and returns the movie by release year

    Эта функция передаёт SQL запрос в функцию get_value_from_database
    и возвращает два фильма между запрошенными датами релиза

    Args:
        year(int): film's release year
        next_year(int)

    Returns:
        dict: information about films (title, release year) between requested years
    """

    sql = f'''
        SELECT title, release_year
        FROM netflix
        WHERE release_year BETWEEN {year} AND {next_year}
        LIMIT 2
    '''

    result = get_value_from_database(sql)
    result_list_of_dict = [dict(item) for item in result]

    return result_list_of_dict

def get_value_by_rating(rating) -> list[dict]:
    """
    This function passes the SQL request in function get_value_from_database
    and returns the movies by rating

    Эта функция передаёт SQL запрос в функцию get_value_from_database
    и возвращает все фильмы определенного рейтинга

    Args:
        year(int): film's release year
        next_year(int)

    Returns:
        dict: information about films (title, release year) between requested years
    """

    rating_designation = []

    if rating == "children".lower():
        rating_designation = ["G"]
    elif rating == "family".lower():
        rating_designation = ["G", "PG", "PG-13"]
    elif rating == "adult".lower():
        rating_designation = ["R", "NC-17"]


    sql = f"""SELECT title, rating, description
             FROM netflix
             WHERE rating IN {rating_designation}
             """

    result = get_value_from_database(sql)
    result_list_of_dict = [dict(item) for item in result]

    return result_list_of_dict

# title = "9"
# get_value_by_title(title)
