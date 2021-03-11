#!/usr/bin/env python3

from mongoengine import IntField, ListField
from mongoengine.fields import StringField
from telegram_utils.model.base_model import BaseModel


class UserModel(BaseModel):
    """ The representation of a message """

    user_id = IntField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    username = StringField(required=True)
    karma_points = IntField(default=0)
