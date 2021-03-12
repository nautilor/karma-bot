#!/usr/bin/env python3

# region
from root.model.user_model import UserModel
from mongoengine.errors import DoesNotExist
from telegram import User
# endregion

def find_by_username(user: User, create: bool = True):
    try:
        # extract th user stored in the database if present
        return UserModel.objects.get(user_id=user.id)
    except DoesNotExist:
        if create:
            # if does not exists create it
            return UserModel(
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
            )
        return None
