
from database.models.user import User
from database.data_service import db_service as ds

from typing import Optional

active_user: Optional[User] = None

def get_active_user(id: str) -> User:
    global active_user
    if not active_user:
        return ds.find_user_by_id(id)
    return active_user