from django.contrib import admin

from .models import *


class ShiftAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class ShiftStatusAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class AdministratorAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class GroupAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class MessageAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class DayAdmin(admin.ModelAdmin):
	list_display = ['__str__']


class DayAbsentAdmin(admin.ModelAdmin):
	list_display = ['__str__']

class ChangeAdmin(admin.ModelAdmin):
    	list_display = ['__str__']

admin.site.register(Shift, ShiftAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(ShiftStatus, ShiftStatusAdmin)
admin.site.register(DayAbsent, DayAbsentAdmin)
admin.site.register(Change, ChangeAdmin)