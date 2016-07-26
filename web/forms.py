from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from web.models import Player, Event, Attendee

import html5.forms.widgets as html5_widgets

class HostAttendeeForm(forms.ModelForm):
	UPDATE_STATUSES = (
		('IN', 'Interested'),
		('AP', 'Approved'),
	)

	CONFIRM_STATUSES = STATUSES = (
		('IN', 'Interested'),
		('CO', 'Confirmed'),
	)

	def __init__(self, *args, **kwargs):
		super(HostAttendeeForm, self).__init__(*args, **kwargs)
		self.fields['status'].label = str(self.instance.user)
		if self.instance.status == 'CO':
			self.fields['status'].choices = HostAttendeeForm.CONFIRM_STATUSES
		else:
			self.fields['status'].choices = HostAttendeeForm.UPDATE_STATUSES

	class Meta:
		model = Attendee
		fields = ['status']

class UserCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields and gamer tag, plus a repeated password."""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

	class Meta:
		model = Player
		fields = ('email', 'name_first', 'name_last')

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field.
	"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Player
		fields = ('email', 'name_first', 'name_last', 'password')

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ['start_time',
					'start_date',
					'num_confirmed',
					'capacity',
					'location',
					'notes',
					]
		exclude = ['num_confirmed']
		widgets = {
				'start_time': html5_widgets.TimeInput(attrs={'placeholder': 'Time'}),
					'start_date': html5_widgets.DateInput(attrs={'placeholder': 'Date'}),
					'num_confirmed': forms.NumberInput(attrs={'placeholder': 'Number confirmed'}),
					'location': forms.TextInput(attrs={'placeholder': 'Location'}),
					'capacity': forms.NumberInput(attrs={'placeholder': 'Capacity'}),
					'notes': forms.TextInput(attrs={'placeholder': 'Notes'}),
					}

class AttendeeForm(forms.ModelForm):
	NOT_APPROVED = ( ('IN', 'Interested'),)
	APPROVED = ( ('CO', 'Confirmed'),)
	def __init__(self, *args, **kwargs):
		super(AttendeeForm, self).__init__(*args, **kwargs)
		self.fields['status'].label = str(self.instance.user)
		self.fields['status'].choices = AttendeeForm.APPROVED if self.instance.status == 'AP' else AttendeeForm.NOT_APPROVED

	class Meta:
		model = Attendee
		fields = ['status',]
