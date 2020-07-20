from database.user import User


def find_user_by_id(id: str) -> User:
    return User.objects(telegram_id=str(id)).first()

def change_user_subscribtion(id: str) -> User:
    user = find_user_by_id(id)
    user.subscribed = not user.subscribed
    user.save()
    return user



def add_location(id: str, location: str) -> User:
    user = find_user_by_id(id)
    user.locations.append(location)
    user.save()
    return user


def set_default_location(user_id: str, location: str) -> User:
    user = find_user_by_id(user_id)
    user.default_location = location
    user.save()
    return user


def create_user(user_id: int, username: str, language: str, chat_id: str) -> User:
    user = User(
        telegram_id=str(user_id),
        username=username,
        language=language,
        chat_id=chat_id
    )
    try:
        user.save()
    except:
        print("error in create user")

    return user
