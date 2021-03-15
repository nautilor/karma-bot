#!/usr/bin/env python3

from mongoengine import IntField, ListField
from telegram_utils.model.base_model import BaseModel


class MessageModel(BaseModel):
    """ The representation of a message """

    message_id = IntField(required=True)
    chat_id = IntField(required=True)
    upvotes = ListField(IntField())
    downvotes = ListField(IntField())
    karma_points = IntField(default=0)
