from database.models.user import User


def find_user_by_id(id: str) -> User:
	user = User.objects(telegram_id=str(id)).first()
	return user


def create_user(user_id: int, name: str, lastname: str, username: str, language: str) -> User:

	user = User()
	user.telegram_id = str(user_id)
	user.name = name
	user.lastname = lastname
	user.username = username
	user.language = language
	user.locations = []

	try:
		user.save()
	except:
		print("error :( ")

	return user
