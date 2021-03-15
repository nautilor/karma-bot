#!/usr/bin/env python3

# region
from root.model.configuration import Configuration
from mongoengine.errors import DoesNotExist
# endregion


def find_by_code(code: str, default: str = None):
    try:
        configuration: Configuration = Configuration.objects.get(code=code)
    except DoesNotExist:
        return default
