from django.db import models
from django.conf import settings
import os, json
from datetime import datetime
from django.contrib.auth.models import User
import datetime
from datetime import date, timedelta

SHIFT_CHOICES = (
    ('y', 'yes'),
    ('m', 'maybe'),
    ('n', 'no'),
)


class Administrator(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)


class Group(models.Model):
    administrator = models.OneToOneField(Administrator, on_delete=models.CASCADE, unique=False)
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=255, default="")
    finnished = models.BooleanField(default=False)

    def __str__(self):
    	return str(self.name)


    def get_first_day(self):
	    days = Day.objects.filter(current=True, group=self).order_by("date")
	    return str(days[0].date.strftime("%d.%m"))

    def get_last_day(self):
	    days = Day.objects.filter(current=True, group=self).order_by("-date")
	    return str(days[0].date.strftime("%d.%m"))

class Day(models.Model):
	group = models.ForeignKey(Group, default="", on_delete=models.CASCADE)
	current = models.BooleanField(default=True)
	finnished = models.BooleanField(default=False)
	date = models.DateField()

	def __str__(self):
		return str(self.group) + " - " + str(self.date)

	def get_shifts(self):
		shifts = Shift.objects.filter(day=self).order_by("start")
		return shifts

	def current_remove(self):
		current = False
	
	def is_past(self):
		last_current = Day.objects.filter(group=self.group, current=True).order_by("-date")[0]
		return True if self.date < last_current.date else False
	
	def has_absent(self):
		return len(DayAbsent.objects.filter(day=self)) > 0



class Shift(models.Model):
	employee = models.ForeignKey(User, blank=True, null=True, default="", on_delete=models.CASCADE)
	day = models.ForeignKey(Day, on_delete=models.CASCADE, blank=True)
	shift_class = models.CharField(max_length=1, choices=SHIFT_CHOICES, blank=True, null="True")
	start = models.TimeField(blank=True,null=True)
	end = models.TimeField(blank=True,null=True)

	def __str__(self):
		return  "Shift: " + str(self.id)


	def get_stamp(self):
		return datetime.datetime.strptime(self.time[:5], '%H:%M').time() > datetime.time(14, 55)


class ShiftStatus(models.Model):
	shift = models.ForeignKey(Shift, on_delete=models.CASCADE, blank=True, null=True, default="")
	user = models.ForeignKey(User, blank=True, null=True, default="", on_delete=models.CASCADE)
	shift_class = models.CharField(max_length=1, choices=SHIFT_CHOICES, blank=True, null="True")
	date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return  str(self.user) + " - " + str(self.shift_class)

	class Meta:
		verbose_name_plural = "Shift statuses"

class DayAbsent(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	day = models.ForeignKey(Day, blank=True, null=True, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
	group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
	text = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return str(self.group) + " - " + str(self.user) + " - " + str(self.text)



