from mongoengine import connect


def init_database():
	connect(alias='main', name='tlgr_users_db')


