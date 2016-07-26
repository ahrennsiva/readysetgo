from django.contrib import admin
from .models import Player, Event, Attendee
from .forms import UserCreationForm 

# Register your models here.
class AttendeesInline(admin.TabularInline):
	model = Attendee
	extra = 0

class HostedEventInline(admin.TabularInline):
	model = Event
	extra = 0

class PlayerAdmin(admin.ModelAdmin):
	# form = UserChangeForm
	add_form = UserCreationForm
	fields = ['email', 'password', 'name_first', 'name_last','last_login']
	list_display = ('email', 'name_first', 'name_last',)
	inlines = [HostedEventInline]

class EventAdmin(admin.ModelAdmin):
	fields = ['host', 'start_time', 'start_date', 'num_confirmed', 'capacity', 'location', 'notes']
	list_display = ['host', 'start_time', 'start_date', 'num_confirmed', 'capacity', 'location', 'notes']
	inlines = [AttendeesInline]

# Register your models here.
admin.site.register(Player, PlayerAdmin)
admin.site.register(Event, EventAdmin)