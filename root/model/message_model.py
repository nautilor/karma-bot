#!/usr/bin/env python3

from root.constant.constant import LANG_EN
from mongoengine import IntField, ListField
from mongoengine.fields import StringField
from telegram_utils.model.base_model import BaseModel


class MessageModel(BaseModel):
    """ The representation of a message """

    message_id = IntField(required=True)
    user_id = StringField()
    chat_id = IntField(required=True)
    upvotes = ListField(IntField())
    downvotes = ListField(IntField())
    language = StringField(default=LANG_EN)
    karma_points = IntField(default=0)
