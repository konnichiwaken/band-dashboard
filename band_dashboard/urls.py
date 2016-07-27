"""band_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from rest_framework_nested import routers

from attendance.views import AttendanceViewSet
from attendance.views import EventTypeViewSet
from attendance.views import EventViewSet
from attendance.views import GetUnassignedMembersView
from attendance.views import SubstitutionFormViewSet
from attendance.views import UnassignedAttendanceView
from authentication.views import AccountViewSet
from authentication.views import LoginView
from authentication.views import LogoutView
from band_dashboard.views import IndexView
from members.views import BandViewSet
from members.views import BandAssignmentView
from members.views import UnassignedMembersView


router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'attendance/event', EventViewSet, base_name='event')
router.register(r'attendance/event_type', EventTypeViewSet)
router.register(r'attendance/event_attendance', AttendanceViewSet, base_name='event_attendance')
router.register(r'members/band', BandViewSet)
router.register(
    r'attendance/substitution_form',
    SubstitutionFormViewSet,
    base_name='substitution_form')

urlpatterns = patterns(
     '',
    url(r'^api/v1/', include(router.urls)),
    url(
        r'^api/v1/attendance/unassigned/$',
        UnassignedAttendanceView.as_view(),
        name='unassigned_attendance'),
    url(r'^api/v1/auth/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/auth/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api/v1/band_assignments/$', BandAssignmentView.as_view(), name='band_assignments'),
    url(
        r'^api/v1/members/unassigned/$',
        UnassignedMembersView.as_view(),
        name='unassigned_members'),
    url(
        r'^api/v1/get_unassigned_members/$',
        GetUnassignedMembersView.as_view(),
        name='get_unassigned_members'),
    url('^.*$', IndexView.as_view(), name='index'),
)
