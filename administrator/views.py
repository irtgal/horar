
from django.contrib.auth.decorators import login_required

from .scripts import *
from timetables.scripts import *

from administrator.turnusi.models import *

@login_required
def group(request, group_id):
	group = get_object_or_404(Group, pk=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	users = group.users.all()
	administrator = group.administrator

	all_messages = request.GET.get('all_messages', False)

	messages = Message.objects.filter(group=group).order_by('-date')
	if not all_messages:
		messages = messages[:3]

	finnished = True
	if group.finnished == False:
		finnished = None
	context = {
	'users': users,
	'administrator': administrator,
	'group': group,
	'group_id':group_id,
	'all_messages': all_messages,
	'finnished': finnished,
	'messages': messages,
	}
	return render(request, 'group_administrator.html', context)

def user_remove(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	administrator = group.administrator
	user = request.POST.get('employee')
	employee = group.users.get(id=user)
	group.users.remove(employee)
	group.save()
	return redirect("/administrator/"+ group_id+"/?success=Uporabnik odstranjen")

def user_add(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	try:
		user_id = request.POST.get('user_id')
		employee = User.objects.get(id=user_id)
		group.users.add(employee)
		return redirect("/administrator/"+ group_id+"/?success=Uporabnik dodan")
	except:
		return redirect("/administrator/"+ group_id+"/?error=Uporabnik ne obstaja")



@login_required
def timetable_administrator(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	users = group.users.all()
	scroll = request.GET.get('scroll', False)
	load_to = request.GET.get('load_to', False)
	load_days = get_days(group, load_to, scroll)
	turnuses = Turnus.objects.filter(group=group)
	context = {
	'group': group,
	'users': users,
	'load_days': load_days,
	'scroll':scroll,
	'turnuses': turnuses,
	}
	return render(request, 'timetable_index_administrator.html', context)


@login_required
def timetable_add(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	administrator = group.administrator
	start = request.POST.get('start_date')
	end = request.POST.get('end_date')
	turnus_id = request.POST.get('turnus-id', None)
	start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
	end_date = datetime.datetime.strptime(end, '%Y-%m-%d')

	if start_date <= end_date:
		#odstrani zdejsnje current
		current_days = Day.objects.filter(current=True, group=group)
		for day in current_days:
			day.current = False
			day.save()


		delta = end_date - start_date
		for i in range(0, delta.days + 1):
			date = start_date + timedelta(days=i)
			day = Day.objects.get_or_create(date=date, group=group)[0]
			day.current = True
			day.save()
			if turnus_id:
				create_shifts(day, turnus_id)

		return redirect("/administrator/"+ group_id+"/urnik/?success=Urnik pripravljen")
	else:
		return redirect("/administrator/"+ group_id+"/urnik/?error=Preverite vpisane podatke")

@login_required
def timetable_check(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	check_timetable(group)
	return redirect("/administrator/"+group_id+"/")


@login_required
def shift_remove(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	shift_id = request.POST.get('id')
	shift = get_object_or_404(Shift, id=shift_id)
	shift.delete()

	return redirect("/administrator/"+ group_id +"/urnik/"+get_query(request))


@login_required
def shift_manage(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	date = request.POST.get('date')
	shift_id = request.POST.get('id', None)
	start = request.POST.get('edit-from')
	end = request.POST.get('edit-to')
	user_str = request.POST.get('select-user')
	user_id = int(user_str) if user_str else None
	day = get_object_or_404(Day, date=date, group=group)

	if shift_id:
		shift = Shift.objects.get(id=shift_id, day=day)
		if user_id > 0:
			employee = group.users.get(id=user_id)#popravi da isce po ID
			shift.employee = employee
			shift.shift_class = "y"
			shiftstatuses = ShiftStatus.objects.filter(shift=shift)
			shiftstatuses.delete()
			shiftstatus = ShiftStatus(user=employee, shift=shift, shift_class="y")
			shiftstatus.save()
		elif user_id == 0:
			shift.employee = None
			shift.shift_class = None
			shiftstatuses = ShiftStatus.objects.filter(shift=shift)
			shiftstatuses.delete()
		shift.start = start
		shift.end = end
		shift.save()
		return redirect("/administrator/"+ group_id +"/urnik/")

	elif start < end:
		shift = Shift(day=day)
		try:
			employee = group.users.get(id=user_id)
			shift.employee = employee
			shift.shift_class = "y"
		except:
			shift.employee = None
			shift.shift_class = None
		shift.start = start
		shift.end = end
		shift.save()
		return redirect("/administrator/"+ group_id +"/urnik/")
	else:
		return redirect("/administrator/"+ group_id +"/urnik/?error=Poskusite ponovno")
