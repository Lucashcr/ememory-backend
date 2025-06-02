from datetime import date
import re

from django.core.exceptions import ValidationError


def hexadecimal_color_validator(value: str):
    if not value.startswith("#") or not bool(
        re.fullmatch(r"[0-9a-f]+", value[1:].lower())
    ):
        raise ValidationError("Invalid hexadecimal format for subject color")


def initial_date_validator(value: date):
    if value < date.today():
        raise ValidationError("Initial date cannot be in the past")
