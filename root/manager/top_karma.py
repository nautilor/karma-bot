#!/usr/bin/env python3

# region
from root.helper.user import find_by_user_id
from root.model.user_model import UserModel
from root.constant.constant import HREF, MESSAGE_LINK
from root.helper.message import find_top_messages
from typing import List
from root.model.message_model import MessageModel
from telegram import Update
from telegram.ext import CallbackContext
from telegram.message import Message
from telegram_utils.utils.tutils import delete_message, send_and_delete
from root.constant.messages import TOP_MESSAGES
# endregion

def top_messages(update: Update, context: CallbackContext):
    # extract the message along with it's id and the chat_id
    message: Message = update.message
    chat_id: int = message.chat_id
    message_id: int = message.message_id
    # delete the command from the chat
    delete_message(chat_id, message_id)
    # find the top messages for the chat
    messages: List[MessageModel] = find_top_messages(chat_id)
    # send a specific message if no messages has been found for the chat
    if not messages:
        return send_and_delete(chat_id=chat_id, message="NO MESSAGES AT ALL", timeout=5)
    # create the header of the message
    text: str = TOP_MESSAGES
    for msg in messages:
        # get the user who posted the message
        user: UserModel = find_by_user_id(msg.user_id)
        if user:
            # set the name to show if the user is still in the database
            name: str = user.first_name if user.first_name else user.username
        else:
            # set a generic name if not found
            name: str = "Unknown"
        # build the html <a/> tag for the message 
        # this will display a link to the message with the name of the username as a text
        message_link: str = MESSAGE_LINK % (msg.chat_id, msg.message_id)
        message_link: str = HREF % (MESSAGE_LINK, name)
        text += f"- {message_link}\n"
    # send the final message to the group
    send_and_delete(chat_id, text, timeout=120)
