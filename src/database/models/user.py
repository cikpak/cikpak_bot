import mongoengine as me

class User(me.Document):
	telegram_id = me.StringField()
	name = me.StringField()
	lastname = me.StringField()
	username = me.StringField()
	email = me.EmailField()
	language = me.StringField()

	default_location = me.GeoPointField()
	units = me.StringField(default='metric')

	meta = {
		"db_alias": "main",
		"collection": "users"
	}
