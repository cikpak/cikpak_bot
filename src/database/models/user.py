from mongoengine import *

class User(Document):
	telegram_id = StringField(required=True)
	username = StringField(required=True)
	language = StringField(required=True)
	locations = ListField()
	units = StringField(default='C')

	meta = {
		"db_alias": "main",
		"collection": "users"
	}
