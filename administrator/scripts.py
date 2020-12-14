from administrator.turnusi.models import *
from timetables.models import Shift, DayAbsent, ShiftStatus
import datetime

def get_query(request):
	url = request.get_full_path()
	try:
		query = "?"+url.split("?")[1]
	except:
		query = ""
	return query


def create_shifts(day, turnus_id):
	turnus = Turnus.objects.get(id=turnus_id)
	d = day.date.strftime("%a")
	shifts = TurnusShift.objects.filter(turnus=turnus, day=d)
	absents = DayAbsent.objects.filter(day=day)
	for s in shifts:
		shift = Shift(
			employee=s.employee,
			day=day,
			shift_class=s.shift_class,
			start=s.start,
			end=s.end
			)
		shift.save()
		for absent in absents:
			status = ShiftStatus(
				shift=shift,
				user=absent.user,
				shift_class="n",
			)
			status.save()

DAY_CHOICES = (
	('Mon', 'Pon'),
	('Tue', 'Tor'),
	('Wed', 'Sre'),
	('Thu', 'Čet'),
	('Fri', 'Pet'),
	('Sat', 'Sob'),
	('Sun','Ned')
)
def get_day_key(day):
	return [key for key,value in DAY_CHOICES if value == day][0]
