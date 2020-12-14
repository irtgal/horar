from django.contrib.auth.models import User
from timetables.models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

def check_user(request, group):
    try:
        group.users.get(request.user)
        return Trie
    except:
        return render(request, '404.html')



def order_statuses(group, shift):
    #da so urejeni po y m n in po datumu
    users = list(group.users.all())
    shiftstatus = ShiftStatus.objects.filter(shift=shift).order_by('date')
    y_status = {}
    m_status = {}
    n_status = {}
    no_status = {}
    for status in shiftstatus:
        users.remove(status.user)
        if status.shift_class == "y":
            y_status[status.user.username] = status.shift_class
        elif status.shift_class == "m":
            m_status[status.user.username] = status.shift_class
        else:
            n_status[status.user.username] = status.shift_class

    for user in users:
        no_status[user.username] = ""

    statuses = {**y_status, **m_status, **n_status, **no_status}
    ym_statuses = {**y_status, **m_status}
    return statuses, ym_statuses

def update_shift(group, shift):
	ordered_statuses = order_statuses(group, shift)[1]
	if ordered_statuses:
		username = next(iter(ordered_statuses))
		shift_class = next(iter(ordered_statuses.values()))
		user = User.objects.get(username=username)
		shift.employee = user
		shift.shift_class = shift_class
		shift.save()
	else:
		shift.employee = None
		shift.shift_class = None
		shift.save()

def get_shift_users(day):
	shifts = Shift.objects.filter(day=day).order_by('start')
	context =[ [shift.employee.username, shift.shift_class] if shift.employee else ['', 'a'] for shift in shifts ]
	return context





def get_days(group, load_to, scroll):
    timetable = Day.objects.filter(group=group, current=True).order_by('date')
    start_date = timetable[0].date
    end_date = timetable.last().date
    try:
        load_to = datetime.datetime.strptime(load_to, '%Y-%m-%d').date()
        if scroll:
            load_from = start_date
            load_to = load_to + datetime.timedelta(days=7)
        else:
            load_from = load_to - datetime.timedelta(days=7)
            load_to = end_date
    except TypeError:
        load_from = start_date
        load_to = end_date
    delta = load_to - load_from
    load_days = {}
    for i in range(delta.days + 1):
        date = load_from + timedelta(days=i)
        try:
            day = Day.objects.get(date=date, group=group)
            load_days[date] = day
        except:
            load_days[date] = ""
    return load_days


def check_timetable(group):
    days = Day.objects.filter(group=group, current=True)
    for day in days:
        shifts = Shift.objects.filter(day=day)
        day.finnished = True
        for shift in shifts:
            if shift.shift_class == "n" or not shift.shift_class:
                day.finnished = False
        day.save()
    group.finnished = True
    if len(Day.objects.filter(group=group, finnished=False, current=True)) > 0:
        group.finnished = False
    group.save()







