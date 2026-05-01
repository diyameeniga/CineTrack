from django import template

register = template.Library()

@register.filter
def stars(value):
    try:
        rating = int(value)

        # Clamp between 0 and 10
        if rating < 0:
            rating = 0
        if rating > 10:
            rating = 10

        filled = "★" * rating
        #empty = "☆" * (10 - rating)

        return filled #+ empty
    except (ValueError, TypeError):
        return ""