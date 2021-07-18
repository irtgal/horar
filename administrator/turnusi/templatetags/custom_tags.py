from django import template
from ..models import *
register = template.Library()

@register.filter(name='find_turnusshifts')
def find_turnusshifts(d, turnus_id):
	turnus = Turnus.objects.get(id=turnus_id)
	return TurnusShift.objects.filter(day=d, turnus=turnus).order_by("start")


@register.filter(name='module_is')
def module_is(url, module):
    return url.split("/")[1] == module