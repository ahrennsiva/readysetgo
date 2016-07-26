from django.conf.urls import url
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
	url(r'^$', views.main, name='main'),
	url(r'^event_search/$', views.event_search, name='event_search'),
	url(r'^event_search/(?P<event_id>[0-9]+)$', views.event_details, name='event_details'),
	url(r'^event_create/$', views.event_create, name='event_create'),
	url(r'^menu/$', views.menu, name='menu'),
	url(r'^login/$', views.user_login, name='user_login'),
	url(r'^logout/$', views.user_logout, name='user_logout'),
	url(r'^new_user/$', views.new_user, name='new_user'),
	url(r'^my_events/$', views.my_events, name='my_events'),
	url(r'^my_events/(?P<event_id>[0-9]+)$', views.event_view, name='event_view'),
	url(r'^my_events/(?P<event_id>[0-9]+)/attendees$', views.attendees, name='attendees'),
	url(r'^approve/$', views.approve_attendee, name='approve_attendee'),
	url(r'^unconfirm/$', views.unconfirm_attendee, name='unconfirm_attendee'),
]
