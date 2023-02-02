from bson import ObjectId
from pathlib import Path
import json
from db_models import Authors, Quotes
from db_connection import db # To allow script to connect to db - shouldn`t be used in main.py


def get_authors_json(file_authors):
    with open(file_authors, "r", encoding="utf8") as fh:
        unpacked_authors = json.load(fh)
        #print(unpacked_authors)
    return unpacked_authors

def get_quotes_json(file_quotes):
    with open(file_quotes, "r", encoding="utf8") as fh:
        unpacked_quotes = json.load(fh)
        print(type(unpacked_quotes))
    return unpacked_quotes


if __name__ == "__main__":

    file_authors = Path(__file__).parent.parent.joinpath('authors.json')
    file_quotes = Path(__file__).parent.parent.joinpath('quotes.json')

    authors = get_authors_json(file_authors)
    quotes = get_quotes_json(file_quotes)

    for author in authors:
        Authors(fullname=author['fullname'], born_date=author['born_date'], born_location=author['born_location'],
                description=author['description']).save()

    for quote in quotes:
        try:
            query_single_autor = Authors.objects(fullname=quote['author']).first()
            print(query_single_autor.to_mongo())
            auth_id = ObjectId(query_single_autor._data['id'])
            print(auth_id)  # Already OBJECT ID
            Quotes(tags=quote['tags'], author=auth_id, quote=quote['quote']).save()
        except:
            print('DB UPLOAD FAIL!!!')
            print('DB UPLOAD FAIL!!!')
            print('DB UPLOAD FAIL!!!')