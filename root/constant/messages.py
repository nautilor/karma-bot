#!/usr/bin/env python3

# if a user tries to upvote/downvote without a message reply
MISSING_REPLY = "TO USE THIS FEATURE YOU NEED TO REPLY TO A USER YOU DONKEY!!!"

# message to print when a user got upvoted/downvoted
DOWNVOTED_USER = 'Karma decrementato per <a href="tg://user?id=%s">%s</a>.'

# message to print when a user got upvoted/downvoted
UPVOTED_USER = 'Karma incrementato per <a href="tg://user?id=%s">%s</a>.'

OPERATION_ALREADY_PERFORMED = '<a href="tg://user?id=%s">%s</a> Puoi eseguire questa azione una sola volta.'

# message when a user try to upvote/downvote themselves
CANNOT_MODIFY_SELF_KARMA = '<a href="tg://user?id=%s">%s</a>, non puoi modificare il tuo karma.'

# message when a bot send an upvote/downvote a user/bot
BOT_MODIFIED_KARMA = "Ora ti siedi e mi spieghi come un bot sia riuscito modificare il bot di una persona."

# message when a user try to upvote/downvote a bot
CANNOT_MODIFY_BOT_KARMA = '<a href="tg://user?id=%s">%s</a>, purtroppo i bot non hanno karma e quindi questa operazione non può essere eseguita.'

# please do nothing and continue with your life
YOU_SHALL_NOT_PASS = "Please do nothing and continue with your life."

# message to show when a user try to show the karma points of a bot
BOT_HAS_NO_KARMA = (
    '<a href="tg://user?id=%s">%s</a>, ricorca che i bot non hanno karma.'
)

# message to show the user current karma points
SELF_KARMA = '<a href="tg://user?id=%s">%s</a>, hai accumulato %s punti.'

# message to show uotes user karma points
USER_KARMA = "<i>%s</i> ha accumulato %s punti."
