from datetime import datetime
from enum import Enum

from tortoise import fields, models

class Items(models.model):
    id = fields.IntField(primary_key=True)
    item_name = fields.CharField()
