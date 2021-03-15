#!/usr/bin/env python3

# region
from telegram.ext import Updater, Dispatcher
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram_utils.utils.misc import environment
from root.manager.karma import handle_downvote, handle_upvote, user_karma
from root.constant.constant import UPVOTE_REGEX, DOWNVOTE_REGEX
from root.constant.configuration_key import UPVOTE_REGEX_CODE, DOWNVOTE_REGEX_CODE
from root.helper.configuration import find_by_code

# endregion


def start_bot():
    """ create a bot instance and run it  """
    # retrieve the token from the environment variables
    token: str = environment("TOKEN")
    # create an updater object
    updater: Updater = Updater(token)
    # add al the required handlers to the bot
    add_handler(updater)
    # start to listen for uncoming updates ignoring the one where the bot was not on
    updater.start_polling(clean=True)


def add_handler(updater: Updater):
    # the dispatcher is where you would ad the various handlers
    dispatcher: Dispatcher = updater.dispatcher

    # search for a regex in the database for an upvote or stick to the default one
    upvote: str = find_by_code(UPVOTE_REGEX_CODE, UPVOTE_REGEX)
    # create a filter for the upvote based on the regex
    upvote: Filters = Filters.regex(upvote)
    # add the message handler and the command handler for the upvote
    dispatcher.add_handler(MessageHandler(upvote, handle_upvote))
    dispatcher.add_handler(CommandHandler("upvote", handle_upvote))

    # search for a regex in the database for a downvote or stick to the default one
    downvote: str = find_by_code(DOWNVOTE_REGEX_CODE, DOWNVOTE_REGEX)
    # create a filter fr the downvote based on the regex
    downvote: Filters = Filters.regex(downvote)
    # add the message handler and the command handler for the downvote
    dispatcher.add_handler(MessageHandler(downvote, handle_downvote))
    dispatcher.add_handler(CommandHandler("downvote", handle_downvote))

    dispatcher.add_handler(CommandHandler("karma", user_karma))
