import markdown as md
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter()
@stringfilter
def markdown(value: str) -> str:
    """
    Convert input `value` with Markdown markup to HTML using `markdown` library.

    :param value: text with Markdown markup.
    :return: input with Markdown markup converted to HTML.
    """
    return md.markdown(
        value, extensions=["markdown.extensions.nl2br", "tables", "fenced_code"]
    )


@register.filter
def get_dict_item_by_key(_dict: dict, key: str) -> any:
    """
    Return an element of the dictionary by key.

    :param _dict: dictionary to get an element from
    :param key: key of an element
    :return: element of the dictionary by key
    """
    return _dict[key]
