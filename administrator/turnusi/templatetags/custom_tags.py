from django import template
from ..models import *
register = template.Library()

@register.filter(name='find_turnusshifts')
def find_turnusshifts(d, turnus_id):
	turnus = Turnus.objects.get(id=turnus_id)
	return TurnusShift.objects.filter(day=d, turnus=turnus)

