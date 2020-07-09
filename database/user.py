from mongoengine import *


class User(Document):
	telegram_id = StringField(required=True)
	chat_id = StringField(required=True)
	username = StringField(required=True)
	language = StringField(required=True)
	locations = ListField()
	units = StringField(default='C')
	subscribed = BooleanField(default=True, required=True)
	default_location = StringField()

	meta = {
		"db_alias": "main",
		"collection": "users"
	}
