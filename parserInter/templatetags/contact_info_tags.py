from django import template
from parserInter.models import SiteInfo

register = template.Library()


@register.simple_tag()
def get_contact_info():
    return SiteInfo.objects.get(id=1)

