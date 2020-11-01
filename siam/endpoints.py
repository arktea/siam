from . import router
from .models import User, Group


@router.post(path="/groups/{group_id}/add-user")
def add_user(group_id: str, user_id: str):
    Group.add_user(group_id, user_id)


@router.post(path="/groups/{group_id}/remove-user")
def remove_user(group_id: str, user_id: str):
    Group.remove_user(group_id, user_id)

