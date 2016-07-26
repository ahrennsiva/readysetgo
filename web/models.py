import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class PlayerManager(BaseUserManager):
	def _create_user(self, email, name_first, name_last, password, is_admin =''):
		if not email:
			raise ValueError('All Players Must Have A Valid E-mail Address!')

		player = self.model(
			email=self.normalize_email(email),
			name_first=name_first,
			name_last=name_last,
			is_admin=is_admin,
		)

		player.set_password(password)
		player.save(using=self._db)
		return player

	def create_user(self, email, name_first, name_last, password):
		return self._create_user(email, name_first, name_last, password, False,)

	def create_superuser(self, email, name_first, name_last, password):
		return self._create_user(email, name_first, name_last, password, True)

class Player(AbstractBaseUser):
	class Meta:
		verbose_name = "player"
		verbose_name_plural = "players"
	
	email = models.EmailField(unique=True)
	USERNAME_FIELD = 'email'
	
	name_first = models.CharField(max_length=50)
	name_last = models.CharField(max_length=50)

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	events = models.ManyToManyField('Event', through='Attendee') # many smashers may attend an event, and a smasher may attend many events
	friends = models.ManyToManyField('self') # future plans: smashers may have many friends, and also be friends to many smashers

	REQUIRED_FIELDS = ['name_first', 'name_last']
	objects = PlayerManager()

	def __str__(self):
		return self.email
	def get_full_name(self):
		return self.email
	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin
	def has_module_perms(self, app_label):
		return self.is_admin
	@property
	def is_staff(self):
		return self.is_admin

class Event(models.Model):
	host = models.ForeignKey(settings.AUTH_USER_MODEL) # many events may be hosted by a smasher

	start_time = models.TimeField('Time', default=timezone.now)
	start_date = models.DateField('Date', default=timezone.now)
	capacity = models.IntegerField('Capacity', default=0)
	num_confirmed = models.IntegerField('Number Confirmed', default=0)
	location = models.CharField(max_length=200)
	notes = models.CharField('Notes', max_length=200, blank=True)

	def __str__(self):
		return str(self.host) + ': ' + str(self.start_time) + " on " + str(self.start_date) + " at " + self.location

class Attendee(models.Model):
	STATUSES = (
		('IN', 'Interested'),
		('AP', 'Approved'),
		('CO', 'Confirmed'),
	)
	user = models.ForeignKey(Player)
	event = models.ForeignKey(Event)
	status = models.CharField('Status', max_length=100, choices=STATUSES)

	def __str__(self):
		return str(self.user) + " going to " + str(self.event) + " with status: " + str(self.status)
