from datetime import datetime
from enum import Enum

from tortoise import fields
from tortoise.models import Model

class Item(Model):
    id = fields.IntField(primary_key=True)
    item_name = fields.CharField(max_length=255)
