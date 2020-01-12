from database.user import User
from database.db_service import find_user_by_id
from typing import Optional

active_user: Optional[User] = None


def get_active_user(id: str) -> User:
    global active_user
    if not active_user:
        return find_user_by_id(id)
    return active_user
