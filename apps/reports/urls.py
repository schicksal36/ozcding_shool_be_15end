"""
통계 관련 URL 라우팅
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # 통계 조회 (타입별로 분기)
    path('api/statistics/<str:stat_type>/', views.StatisticsView.as_view(), name='statistics'),
    
    # 구체적인 엔드포인트 (편의를 위해)
    path('api/statistics/study-time/subjects/', views.StatisticsView.as_view(), {'stat_type': 'study-time/subjects'}, name='statistics-study-time'),
    path('api/statistics/average-score/subjects/', views.StatisticsView.as_view(), {'stat_type': 'average-score/subjects'}, name='statistics-average-score'),
    path('api/statistics/weak-parts/', views.StatisticsView.as_view(), {'stat_type': 'weak-parts'}, name='statistics-weak-parts'),
    path('api/statistics/quizzes/accuracy/', views.StatisticsView.as_view(), {'stat_type': 'quizzes/accuracy'}, name='statistics-quiz-accuracy'),
    path('api/statistics/pass-prediction/', views.StatisticsView.as_view(), {'stat_type': 'pass-prediction'}, name='statistics-pass-prediction'),
]
