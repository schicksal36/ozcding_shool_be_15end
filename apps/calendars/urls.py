"""
일정 및 시험 관련 URL 라우팅
"""
from django.urls import path
from . import views

app_name = 'calendars'

urlpatterns = [
    # 일정
    path('events/', views.CalendarCreateView.as_view(), name='event-create'),   # POST
    path('events/', views.CalendarListView.as_view(), name='event-list'),       # GET
    path('events/<int:pk>/', views.CalendarDetailView.as_view(), name='event-detail'),

    # 반복 일정
    path('events/repeat/', views.RepeatCalendarCreateView.as_view()),
    path('events/repeat/<int:pk>/', views.RepeatCalendarDetailView.as_view()),

    # 시험
    path('exams/', views.ExamView.as_view({'get': 'list', 'post': 'create'})),
    path('exams/<int:pk>/', views.ExamView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('exams/upcoming/', views.UpcomingExamView.as_view()),
]
