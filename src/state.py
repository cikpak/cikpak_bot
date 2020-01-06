from typing import Optional

from database.models.user import User
from database.data_service import db_service as ds

active_user: Optional[User] = None


def update_account():
    global active_user
    if not active_user:
        return

    active_user = ds.find_user_by_id(active_user.id)
