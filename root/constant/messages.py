#!/usr/bin/env python3

# if a user tries to upvote/downvote without a message reply
MISSING_REPLY = "TO USE THIS FEATURE YOU NEED TO REPLY TO A USER YOU DONKEY!!!"

# message to print when a user got upvoted/downvoted
DOWNVOTED_USER = 'Karma decrementato per <a href="tg://user?id=%s">%s</a>.'

# message to print when a user got upvoted/downvoted
UPVOTED_USER = 'Karma incrementato per <a href="tg://user?id=%s">%s</a>.'

# message when a user try to upvote/downvote themselves
SELF_UPVOTE = '<a href="tg://user?id=%s">%s</a>, non puoi darti karma da solo.'

# message when a bot send an upvote/downvote a user/bot
UPVOTE_FROM_BOT = "Ora ti siedi e mi spieghi come un bot sia riuscito modificare il bot di una persona."

# message when a user try to upvote/downvote a bot
BOT_UPVOTE = '<a href="tg://user?id=%s">%s</a>, purtroppo i bot non hanno karma e quindi questa operazione non può essere eseguita.'

# please do nothing and continue with your life
YOU_SHALL_NOT_PASS = "Please do nothing and continue with your life."

BOT_HAS_NO_KARMA = (
    '<a href="tg://user?id=%s">%s</a>, ricorca che i bot non hanno karma.'
)

SELF_KARMA = '<a href="tg://user?id=%s">%s</a>, hai accumulato %s punti.'

USER_KARMA = "<i>%s</i> ha accumulato %s punti."
