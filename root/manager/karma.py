#!/usr/bin/env python3

# region
from root.helper.user import find_by_username
from root.helper.message import find_by_chat_and_message
from telegram.message import Message
from root.model.user_model import UserModel
from telegram.user import User
from root.model.message_model import MessageModel
from root.constant.messages import (
    BOT_HAS_NO_KARMA,
    CANNOT_MODIFY_BOT_KARMA,
    DOWNVOTED_USER, OPERATION_ALREADY_PERFORMED,
    SELF_KARMA,
    CANNOT_MODIFY_SELF_KARMA,
    UPVOTED_USER,
    BOT_MODIFIED_KARMA,
    USER_KARMA,
    YOU_SHALL_NOT_PASS,
)
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram_utils.utils.tutils import send_and_delete, send_message
# endregion

"""
    This file handles the upvote and the downvote.
    Since they both have most of the code in common a default function `handle_karma` has been created.
    This function will take care of things like:
        - Check if the user replied to a message;
        - Find the relative message/user in the database;
        - Create them if not present;
        - Send the message to Telegram informing of the upvote/downvote;
    
    The rest like the upvote/downvote and the message formatting are declared as separated function that needs to be passed
    to the function `handle_karma`
"""


def upvote_message(message: MessageModel, user: User):
    """
    Add the user_id to the message.upvotes stored in the database
    this is used to check if the user has already upvoted the message
    """
    # if the user has already upvoted the message ignore
    if user.id in message.upvotes:
        name: str = user.username if user.username else user.first_name
        send_and_delete(OPERATION_ALREADY_PERFORMED % (user.id, name))
        return False
    # upvote the message
    message.upvotes.append(user.id)
    # if the user has previously downvoted the message
    if user.id in message.downvotes:
        # remove the user from the downvote list
        message.downvotes.remove(user.id)
    # update the document in the database
    message.save()
    return True


def handle_upvote(update: Update, context: CallbackContext):
    """ Handle an upvote """
    # lambda function to upvote the user
    upvote_user = lambda karma: karma + 1
    handle_karma(update, context, upvote_user, upvote_message, format_upvote_message)


def format_upvote_message(_: MessageModel, user: UserModel):
    """
    Format the message about the upvote that needs to be sent back to the chat
    """
    # extract the username or the first_name from the user
    name: str = user.username if user.username else user.first_name
    # build the message to print
    return UPVOTED_USER % (user.id, name)


##################################################################


def downvote_message(message: MessageModel, user: User):
    """
    Add the user_id to the message.downvotes stored in the database
    this is used to check if the user has already downvoted the message
    ...
    """
    # if the user has already downvoted the message ignore
    if user.id in message.downvotes:
        name: str = user.username if user.username else user.first_name
        send_and_delete(OPERATION_ALREADY_PERFORMED % (user.id, name))
        return False
    # downvote the message
    message.downvotes.append(user.id)
    # if the user has previously upvoted the message
    if user.id in message.upvotes:
        # remove the user from the upvote list
        message.upvotes.remove(user.id)
    # update the document in the database
    print(message)
    message.save()
    return True


def format_downvote_message(_: MessageModel, user: UserModel):
    """
    Format the message about the downvote that needs to be sent back to the chat
    """
    # extract the username or the first_name from the user
    name: str = user.username if user.username else user.first_name
    # build the message to print
    return DOWNVOTED_USER % (user.id, name)


def handle_downvote(update: Update, context: CallbackContext):
    """ Handle an upvote """
    # lambda function to downvote the user
    downvote_user = lambda karma: karma - 1
    handle_karma(
        update, context, downvote_user, downvote_message, format_downvote_message
    )


##################################################################


def handle_karma(
    update: Update,
    _: CallbackContext,
    user_callback: callable,
    message_callback: callable,
    message_format: callable,
):
    """
    This function will:
        - check if the matching regex has a reply message
        - store the user that upvoted/downvoted and the one he quoted
    """
    # extract the message or the edited_message
    message: Message = update.edited_message
    message: Message = message if message else update.message
    # ignore message without a reply
    reply: Message = message.reply_to_message
    if not reply:
        return YOU_SHALL_NOT_PASS

    # store the information about the user who upvoted the message
    upvote_user: User = message.from_user
    database_user: UserModel = find_by_username(upvote_user)

    # exctract the message_id and the chat_id
    chat_id: int = reply.chat_id
    user: User = reply.from_user

    # WTF?!
    if upvote_user.is_bot:
        return send_message(chat_id, BOT_MODIFIED_KARMA)

    # tell the user to f*** off if they try to upvote a bot
    if user.is_bot:
        name = (
            upvote_user.first_name if upvote_user.first_name else upvote_user.username
        )
        return send_and_delete(CANNOT_MODIFY_BOT_KARMA % (upvote_user.id, name), timeout=10)

    # tell the user to f*** off if they try to upvote themselves
    if user.id == upvote_user.id:
        name = (
            upvote_user.first_name if upvote_user.first_name else upvote_user.username
        )
        return send_and_delete(CANNOT_MODIFY_SELF_KARMA % (upvote_user.id, name), timeout=10)

    # find or create a message on the database
    database_message: MessageModel = find_by_chat_and_message(reply)

    # call the relative function to upvote/downvote
    if message_callback(database_message, upvote_user):
        # find or create the user on the database
        database_user: UserModel = find_by_username(user)

        # call the relative lambda function to upvote/downvote
        database_user.karma_points = user_callback(database_user.karma_points)
        database_user.save()

        # format the message to send
        text: str = message_format(database_message, database_user)

        # send the message with auto-desctruction set to 10 seconds
        return send_and_delete(chat_id, text, timeout=10)
    

##################################################################

def user_karma(update: Update, _: CallbackContext):
    """ Show the current user or a quoted one karma points """
    # extract the message or the edited_message
    message: Message = update.edited_message
    message: Message = message if message else update.message
    chat_id: int = message.chat_id
    is_reply: bool = True if message.reply_to_message else False
    # use the quoted user if the original user quoted someone
    user: User = message.reply_to_message.from_user if is_reply else message.from_user
    # if the user quoted a bot tell him
    if user.is_bot:
        user: User = message.from_user
        name: str = user.first_name if user.first_name else user.username
        return send_and_delete(BOT_HAS_NO_KARMA % (user.id, name))
    # find or create the user on the database
    database_user: UserModel = find_by_username(user)
    # extract the user karma point
    karma: int = database_user.karma_points
    name: str = user.first_name if user.first_name else user.username
    # create a different message if there's a quote
    # fmt: off
    text: str = USER_KARMA % (name, karma) if is_reply else SELF_KARMA % (user.id, name, karma)
    # fmt: on
    # send the message with auto-desctruction set to 10 seconds
    send_and_delete(chat_id, text, timeout=10)
