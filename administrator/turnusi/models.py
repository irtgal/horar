from django.db import models
from django.conf import settings
import os, json
from datetime import datetime
from django.contrib.auth.models import User
import datetime
from datetime import date, timedelta

from timetables.models import *

DAY_CHOICES = (
	('Mon', 'Pon'),
	('Tue', 'Tor'),
	('Wed', 'Sre'),
	('Thu', 'Čet'),
	('Fri', 'Pet'),
	('Sat', 'Sob'),
	('Sun','Ned')
)
SHIFT_CHOICES = (
    ('y', 'yes'),
    ('m', 'maybe'),
    ('n', 'no'),
)

class Turnus(models.Model):
	group = models.ForeignKey(Group, default="", on_delete=models.CASCADE)
	name = models.CharField(max_length=30)

	def __str__(self):
		return "{} - {}".format(self.group, self.name)

	class Meta:
		verbose_name_plural = "Turnuses"


class TurnusShift(models.Model):
	turnus = models.ForeignKey(Turnus, on_delete=models.CASCADE, blank=True, null=True)
	day = models.CharField(max_length=3, choices=DAY_CHOICES, blank=True, null=True)
	start = models.TimeField(blank=True,null=True)
	end = models.TimeField(blank=True,null=True)
	shift_class = models.CharField(max_length=1, choices=SHIFT_CHOICES, blank=True, null=True)
	employee = models.ForeignKey(User, blank=True, null=True, default="", on_delete=models.CASCADE)

	def __str__(self):
		return "{}, {}".format(self.turnus, self.day)

	def get_day(self):
		for item in DAY_CHOICES:
			if item[0] == self.day:
				return item[1]

