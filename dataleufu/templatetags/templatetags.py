from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

register = template.Library()

ALLOWABLE_VALUES = ("WEB_APP_BASE_URL", "ADMIN_URL", "CONTACT_EMAIL")

# Permite usar las variables del settings en los templates

@register.simple_tag
def settings_value(name):
    print "settings_value ", name
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''
