from mongoengine import EmbeddedDocument, Document, CASCADE
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, ListField, StringField, ReferenceField


class Tags(Document):
    name = ListField()


class Authors(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags = ListField()
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True} # Чтоб разрешить наследование NumQuotes(Quotes) numeric_data=....


if __name__ == "__main__":
 pass
