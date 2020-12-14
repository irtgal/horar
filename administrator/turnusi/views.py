
from django.contrib.auth.decorators import login_required

from timetables.scripts import *
from administrator.scripts import *

from .models import *

@login_required
def get_turnusi(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')
	turnusi = Turnus.objects.filter(group=group)
	if turnusi.exists():
		turnus = turnusi[0]
		return redirect(f'/administrator/{group.id}/turnusi/{turnus.id}/')
	else:
		return render(request, 'turnusi_administrator.html', {'group': group})


@login_required
def turnus(request, group_id, turnus_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	turnusi = Turnus.objects.filter(group=group)
	current = get_object_or_404(Turnus, id=turnus_id)
	days = current.turnusshift_set.all()
	users = group.users.all()
	context = {
		'turnusi': turnusi,
		'group': group,
		'days': days,
		'current': current,
		'day_choices': DAY_CHOICES,
		'users': users,
	}
	return render(request, 'turnusi_administrator.html', context)

def turnus_add(request, group_id, turnus_id=False):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')
	turnus_name = request.POST.get('turnus-name')
	if 0 < len(turnus_name) < 21:
		new_turnus = Turnus(group=group, name=turnus_name)
		new_turnus.save()
		return redirect(f'/administrator/{group.id}/turnusi/{new_turnus.id}/')
	else:
		return render(f'/administrator/{group.id}/turnusi/?error=Poskusite ponovno')

def turnus_remove(request, group_id, turnus_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')
	print(turnus_id)
	turnus = Turnus.objects.get(id=turnus_id, group=group)
	turnus.delete()
	return redirect(f"/administrator/{group.id}/turnusi/")

@login_required
def turnusi_shift_remove(request, group_id, turnus_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	shift_id = request.POST.get('id')
	turnus = get_object_or_404(Turnus, id=turnus_id)
	shift = get_object_or_404(TurnusShift, id=shift_id, turnus=turnus)
	shift.delete()

	return redirect(f"/administrator/{group.id}/turnusi/{turnus.id}/")

def turnusi_shift_manage(request, group_id, turnus_id):
	group = get_object_or_404(Group, id=group_id)
	if group.administrator.user != request.user:
		return render(request, '404.html')

	day = request.POST.get('date')
	shift_id = request.POST.get('id', None)
	start = request.POST.get('edit-from')
	end = request.POST.get('edit-to')
	user_str = request.POST.get('select-user')
	user_id = int(user_str) if user_str else None
	turnus = get_object_or_404(Turnus, id=turnus_id)

	if shift_id:
		shift = TurnusShift.objects.get(id=shift_id, turnus=turnus)
		if user_id > 0:
			employee = group.users.get(id=user_id)#popravi da isce po ID
			shift.employee = employee
			shift.shift_class = "y"
		elif user_id == 0:
			shift.employee = None
			shift.shift_class = None
		shift.start = start
		shift.end = end
		shift.save()
		return redirect(f"/administrator/{group.id}/turnusi/{turnus.id}/")

	elif start < end:
		shift = TurnusShift(turnus=turnus, day=get_day_key(day))
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
		return redirect(f"/administrator/{group.id}/turnusi/{turnus.id}/")
	else:
		return redirect(f"/administrator/{group.id}/turnusi/{turnus.id}/?error=Poskusite ponovno")