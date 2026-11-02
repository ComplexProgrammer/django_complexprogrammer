from django import template

from comments.moderation import mask_pii as _mask_pii

register = template.Library()


@register.filter
def mask_pii(text):
    """Izohdagi telefon, pasport, JŞŞIR va karta raqamlarini yaşiradi (comments.moderation.mask_pii)."""
    return _mask_pii(text)
