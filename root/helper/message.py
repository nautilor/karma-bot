#!/usr/bin/env python3

# region
from root.model.message_model import MessageModel
from mongoengine.errors import DoesNotExist
from telegram import Message, User

# endregion


def find_by_chat_and_message(message: Message, create: bool = True):
    # exctract the message_id and the chat_id
    message_id: int = message.message_id
    chat_id: int = message.chat_id
    user: User = message.from_user
    try:
        # extact the message stored in the database if present
        return MessageModel.objects.get(message_id=message_id, chat_id=chat_id)
    except DoesNotExist:
        if create:
            # if does not exists create it
            return MessageModel(
                message_id=message_id,
                chat_id=chat_id,
                upvotes=[],
                downvotes=[],
                user_id=user.id,
            )
        return None
