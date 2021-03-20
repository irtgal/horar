from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import serializers


from .scripts import *
from .models import *

def login_user(request):
	if request.method == "GET":
		return render(request, 'login.html')
	username = request.POST['username']
	password = request.POST['password']
	next = request.POST['next']
	user = authenticate(username=username, password=password)
	if (user is None or not user.is_active):
		return render(request, 'login.html', {'error_message': 'Neveljaven vpis'})
	login(request, user)
	if next !="":
		return redirect(next)
	if Group.objects.filter(users=user).count() != 1:
		return redirect(f'/urniki/uporabnik/')
	group = get_object_or_404(Group, users=user)
	app = "administrator" if Administrator.objects.filter(user=user).exists() else "urniki"
	return redirect(f'/{app}/{group.id}/')

@login_required
def profile(request):
	user = request.user
	groups = Group.objects.filter(users=user)
	context = {'user': user, 'groups': groups}
	return render(request, 'profile.html', context)

def logout_user(request):
	logout(request)
	return redirect("/doma/")

@login_required
def group_index(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	check_user(request, group)
	administrator = group.administrator.user.username
	messages = Message.objects.filter(group=group).order_by('-date')
	finnished = "finnished" if group.finnished == True else None
	users = group.users.all()
	context = {'group': group, 'users': users, 'messages': messages, 'administrator': administrator,'finnished': finnished}
	return render(request, 'group_index.html', context)


@login_required
def message_add(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	check_user(request, group)
	message = request.GET['message']
	if 0 < len(message) < 255:
		t = Message(user=request.user, text=message, group=group)
		t.save()
		return JsonResponse({'success': 'success'})
	else:
		return JsonResponse({'error': 'Predolgo sporočilo'})


@login_required
def timetable_index(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	check_user(request, group)
	users = group.users.all()
	scroll = request.GET.get('scroll', False)
	load_to = request.GET.get('load_to', False)
	load_days = get_days(group, load_to, scroll)

	load_direction = None
	if load_to:
		first_date = min( (date for date, day  in load_days.items()) )
		first_current = Day.objects.filter(group=group, current=True).order_by("date")[0]
		load_direction = "future" if first_current.date <= first_date else "past"
		
	context = {
		'group': group,
		'users': users,
		'load_days': load_days,
		'load_direction': load_direction,
		'scroll': scroll,
	}
	return render(request, 'timetable_index.html', context)


@login_required
def add(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	check_user(request, group)
	shift_class = request.POST.get('shift_class')
	shift_id = request.POST.get('id')

	shift = get_object_or_404(Shift, id=shift_id)

	if DayAbsent.objects.filter(day=shift.day, user=request.user).exists():
		return JsonResponse({'error': 'Na ta dan ste označili, da ste odsotni'})

	shiftstatus = ShiftStatus.objects.get_or_create(shift=shift, user=request.user)[0]
	shiftstatus.shift_class = shift_class
	shiftstatus.date = datetime.datetime.now()
	shiftstatus.save()
	update_shift(group, shift)

	username = ''
	shift_class = 'a'
	if shift.employee:
		username = shift.employee.username
		shift_class = shift.shift_class

	return JsonResponse({'username': username, 'shift_class': shift_class})


def timetable_check(request, group_id):
	group = get_object_or_404(Group, id=group_id)
	check_user(request, group)
	check_timetable(group)
	return redirect("/urniki/" + group_id + "/")


@login_required
def get_status(request, group_id, shift_id):
	group = get_object_or_404(Group, id=group_id)
	check_user(request, group)
	shift = get_object_or_404(Shift, id=shift_id)
	data = json.dumps(order_statuses(group, shift)[0])
	return JsonResponse({'statuses': data})


@login_required
def absent(request, group_id):
	check_user(request, group_id)
	group = get_object_or_404(Group, id=group_id)
	date = request.POST.get('day_id')
	user = request.user
	day = Day.objects.get_or_create(date=date, group=group, defaults={'current': False})[0]

	try:
		DayAbsent.objects.get(user=user, day=day).delete()
		for shift in Shift.objects.filter(day=day):
			ShiftStatus.objects.get(shift=shift, user=user).delete()
			update_shift(group, shift)
		data = None
	except:
		DayAbsent(day=day, user=user).save()
		for shift in Shift.objects.filter(day=day):
			shift_status = ShiftStatus.objects.get_or_create(shift=shift, user=user)[0]
			shift_status.shift_class = "n"
			shift_status.save()
			if shift.employee == user:
				update_shift(group, shift)
		data = json.dumps(get_shift_users(day))

	return JsonResponse(data, safe=False)
	
@login_required
def get_absent(request, group_id, date):
	check_user(request, group_id)
	group = get_object_or_404(Group, id=group_id)
	try:
		day = Day.objects.get(date=date, group=group)
		absents = DayAbsent.objects.filter(day=day)
		users = [absent.user.username for absent in absents]
	except:
		users = None

	try:
		DayAbsent.objects.get(day=day, user=request.user)
		am_absent = True
	except:
		am_absent = False

	context = json.dumps([am_absent, users])
	return JsonResponse(context, safe=False)