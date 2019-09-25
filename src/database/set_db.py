import mongoengine as me


def init_database():
	me.register_connection(alias='main', name='tlgr_users_db')


