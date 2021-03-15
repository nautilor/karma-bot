#!/usr/bin/env python3

from mongoengine.fields import StringField
from telegram_utils.model.base_model import BaseModel


class Configuration(BaseModel):
    """ The representation of a configuration """

    code = StringField(required=True)
    value = StringField()
    
