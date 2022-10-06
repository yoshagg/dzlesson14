from flask import Flask
from utils import get_value_by_title, get_value_by_release_year, get_value_by_rating, get_value_by_genre
import json

app = Flask(__name__)


@app.route('/movie/<title>/')
def view_title(title):
    result = get_value_by_title(title)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False
                            ),
        status=200,
        mimetype="application/json"


    )


@app.route('/movie/year/<int:year>/to/<int:next_year>/')
def view_release_year(year, next_year):
    result = get_value_by_release_year(year, next_year)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"


    )


@app.route('/movie/rating/<rating>/')
def view_rating(rating):
    result = get_value_by_rating(rating)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"


    )


@app.route('/movie/genre/<genre>/')
def view_genre(genre):
    result = get_value_by_genre(genre)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4,
                            ),
        status=200,
        mimetype="application/json"


    )


if __name__ == '__main__':
    app.run(host='localhost', port='8080', debug=True)
