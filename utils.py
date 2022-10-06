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
    и возвращает все фильмы указанного рейтинга

    Args:
        rating(str)

    Returns:
        list[dict]: information about films (title, rating, description) by rating
    """

    rating_designation = []

    if rating == "children".lower():
        rating_designation = ",".join(['\"G\"'])
    elif rating == "family".lower():
        rating_designation = ",".join(['\"G\", \"PG\", \"PG-13\"'])
    elif rating == "adult".lower():
        rating_designation = ",".join(['\"R\", \"NC-17\"'])

    sql = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({rating_designation})
            """

    result = get_value_from_database(sql)
    result_list_of_dict = [dict(item) for item in result]

    return result_list_of_dict


def get_value_by_genre(genre) -> list[dict]:
    """
    This function passes the SQL request in function get_value_from_database
    and returns the movies by genre

    Эта функция передаёт SQL запрос в функцию get_value_from_database
    и возвращает все фильмы указанного жанра

    Args:
        genre(str)

    Returns:
        list[dict]: information about films (title, description) by genre
    """

    recieved_genre = genre.title()

    sql = f"""
            SELECT DISTINCT title, listed_in, description
            FROM netflix
            WHERE listed_in LIKE '%{recieved_genre}%'
            OR listed_in LIKE '{recieved_genre}%' 
            OR listed_in LIKE '%{recieved_genre}'
            ORDER BY release_year desc
            LIMIT 10
            """

    result = get_value_from_database(sql)
    result_list_of_dict = [dict(item) for item in result]

    return result_list_of_dict


def get_actors_names_from_user() -> list:  # creates actor's names list by user's input
    actor_names = []
    while True:
        actor_name = input("Введите имена актёров: \n").title()
        if actor_name != 'Stop':
            actor_names.append(actor_name)
            print("Имя добавлено в запрос! Введите ещё одно или напишите STOP")
        elif actor_name == 'Stop':
            print("Список сформирован")
            break
        for item in actor_name:
            if item in ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
                        'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
                        'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']:
                print("Имя должно быть на английском языке!")  # it can be removed if db created not by en language
                continue

    return actor_names

# print(get_actors_names_from_user())


def get_actors_who_acted_together_more_than_one_time() -> list:  # задание 5

    # names = ', '.join(get_actors_names_from_user())

    entered_names = get_actors_names_from_user()

    sql = f"""
            SELECT *
            FROM netflix
            WHERE 'cast' IN ({entered_names})
            """

    result = get_value_from_database(sql)

    tmp = []
    names_dict = {}

    for item in result:
        requested_names = set(dict(item).get('cast').split(', ')) - set(entered_names)

        for name in requested_names:
            names_dict[name.strip()] = names_dict.get(name.strip(), 0) + 1

    for key, value in names_dict.items():
        if value > 2:
            tmp.append(key)

    return tmp


# print(get_actors_who_acted_together_more_than_one_time())

def get_value_by_type(type='TV Show') -> list[dict]:
    """
    This function passes the SQL request in function get_value_from_database
    and returns the movies by type

    Эта функция передаёт SQL запрос в функцию get_value_from_database
    и возвращает все фильмы указанного типа

    Args:
        type(str)

    Returns:
        list[dict]: information about films (title, rating, description) by rating
    """

    sql = f"""
            SELECT type, release_year, listed_in
            FROM netflix
            WHERE type = {type}
            """

    result = get_value_from_database(sql)
    result_list_of_dict = [dict(item) for item in result]

    return result_list_of_dict

# title = "9"
# get_value_by_title(title)
