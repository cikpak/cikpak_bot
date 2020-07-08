from database.user import User

def find_user_by_id(id: str) -> User:
	user = User.objects(telegram_id=str(id)).first()
	return user


def create_user(user_id: int, username: str, language: str) -> User:
	user = User(
		telegram_id = str(user_id),
		username = username,
		language = language
	)
	try:
		user.save()
	except:
		print("error in create user")

	return user
