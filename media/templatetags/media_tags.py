from django import template
from clubs.utils import is_coordinator_or_member, get_media_center

from media.models import RED, GREEN, BLUE, AERO, GREY, ORANGE, YELLOW, PINK, PURPLE

register = template.Library()

@register.simple_tag
def convert_to_hex(color):
    """
    Return the hex value for the passed color string.
    The passed color is part of a class name required by the iCheck plugin.
    The hex values are based on the iCheck stylesheets.
    """
    hex_values = {
        RED: "#e56c69",
        GREEN: "#1b7e5a",
        BLUE: "#2489c5",
        AERO: "#9cc2cb",
        GREY: "#73716e",
        ORANGE: "#f70",
        YELLOW: "#FFC414",
        PINK: "#a77a94;",
        PURPLE: "#6a5a8c",
    }
    return hex_values[color]


@register.filter
def is_media_coordinator_or_member(user):
    return is_coordinator_or_member(get_media_center(), user)