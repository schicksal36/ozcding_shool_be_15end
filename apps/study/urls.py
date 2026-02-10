"""
스터디 관련 URL 라우팅
"""
from django.urls import path
from . import views

app_name = 'study'

urlpatterns = [
    # 스터디 이벤트 관련
    path('api/study-events/', views.StudyListCreateView.as_view(), name='study-list-create'),
    path('api/study-events/<int:pk>/', views.StudyDetailView.as_view(), name='study-detail'),
    
    # 타이머 관련
    path('api/events/<int:event_id>/timer/start/', views.StudyTimerStartView.as_view(), name='timer-start'),
    path('api/events/<int:event_id>/timer/stop/', views.StudyTimerEndView.as_view(), name='timer-stop'),
    
    # 공부 내용 관련 (설계서 기준: RetrieveUpdateDestroyAPIView)
    path('api/study-events/<int:event_id>/contents/', views.StudyContentView.as_view(), name='study-content-list-create'),  # POST, GET
    path('api/study-contents/<int:content_id>/', views.StudyContentDetailView.as_view(), name='study-content-detail'),  # GET, PATCH, DELETE
]
