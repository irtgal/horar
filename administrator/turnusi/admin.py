from django.contrib import admin
from .models import *

class TurnusAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class TurnusShiftAdmin(admin.ModelAdmin):
	list_display = ['__str__']

admin.site.register(Turnus, TurnusAdmin)
admin.site.register(TurnusShift, TurnusShiftAdmin)
