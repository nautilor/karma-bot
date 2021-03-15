#!/usr/bin/env python

# region
from telegram_utils.utils.database import db_connect
from root.manager.bot import start_bot

# endregion


def main():
    db_connect()
    start_bot()


if __name__ == "__main__":
    main()
