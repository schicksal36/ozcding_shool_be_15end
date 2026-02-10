"""
통계 관련 API 뷰
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from apps.study.models import StudyEvent, StudyContent, StudyTimer
from apps.calendars.models import Exam
from .serializers import StatisticsSerializer


@extend_schema(
    tags=['통계'],
    summary='통계 조회',
    description='과목별 공부 시간 비율, 평균 점수, 취약 파트 등 다양한 통계를 조회합니다'
)
class StatisticsView(APIView):
    """통계 조회 API"""
    permission_classes = [IsAuthenticated]
    
    def dispatch(self, request, *args, **kwargs):
        """요청 처리 전 stat_type 저장"""
        self.stat_type = kwargs.get('stat_type')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """
        통계 타입에 따라 다른 통계 반환
        
        :param stat_type: 통계 타입 (URL에서 추출)
        """
        stat_type = self.stat_type or kwargs.get('stat_type')
        
        if stat_type == 'study-time/subjects':
            return self._get_study_time_by_subject(request)
        elif stat_type == 'average-score/subjects':
            return self._get_average_score_by_subject(request)
        elif stat_type == 'weak-parts':
            return self._get_weak_parts_analysis(request)
        elif stat_type == 'quizzes/accuracy':
            return self._get_quiz_accuracy(request)
        elif stat_type == 'pass-prediction':
            return self._get_pass_prediction(request)
        else:
            return Response(
                {'error': '알 수 없는 통계 타입입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _get_study_time_by_subject(self, request):
        """과목별 공부 시간 비율 조회"""
        user = request.user
        
        # 공부 내용에서 과목별 시간 집계
        # StudyContent에 subject 필드가 없다면 StudyEvent의 title이나 goal을 과목으로 사용
        study_contents = StudyContent.objects.filter(
            study_event__user=user
        ).values('study_event__title').annotate(
            total_minutes=Sum('duration_minutes')
        )
        
        # 전체 시간 계산
        total_time = sum(item['total_minutes'] for item in study_contents)
        
        # 비율 계산
        statistics = []
        for item in study_contents:
            if total_time > 0:
                ratio = (item['total_minutes'] / total_time) * 100
            else:
                ratio = 0.0
            
            statistics.append({
                'label': item['study_event__title'],
                'value': round(ratio, 2)
            })
        
        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_average_score_by_subject(self, request):
        """과목별 평균 점수 조회"""
        user = request.user
        
        # 시험에서 과목별 평균 점수 계산
        exams = Exam.objects.filter(
            user=user,
            score__isnull=False
        ).values('subject').annotate(
            avg_score=Avg('score'),
            max_score=Avg('max_score')
        )
        
        statistics = []
        for exam in exams:
            # 백분율로 변환
            if exam['max_score'] > 0:
                percentage = (exam['avg_score'] / exam['max_score']) * 100
            else:
                percentage = 0.0
            
            statistics.append({
                'label': exam['subject'],
                'value': round(percentage, 2)
            })
        
        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_weak_parts_analysis(self, request):
        """과목별 취약 파트 분석"""
        user = request.user
        
        # 시험에서 과목별 평균 점수 계산
        # 점수가 낮은 과목을 취약 파트로 판단
        exams = Exam.objects.filter(
            user=user,
            score__isnull=False
        ).values('subject').annotate(
            avg_score=Avg('score'),
            count=Count('id')
        ).order_by('avg_score')[:5]  # 점수가 낮은 상위 5개
        
        statistics = []
        for exam in exams:
            statistics.append({
                'label': exam['subject'],
                'value': round(exam['avg_score'], 2)
            })
        
        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_quiz_accuracy(self, request):
        """시험 정답률 통계 조회 (Quiz 앱이 없으므로 Exam 데이터 사용)"""
        user = request.user
        
        # 전체 시험의 평균 점수 계산
        exams = Exam.objects.filter(user=user, score__isnull=False)
        total_exams = exams.count()
        
        if total_exams > 0:
            # 시험의 평균 점수 계산
            avg_score = exams.aggregate(avg=Avg('score'))['avg'] or 0
            avg_max_score = exams.aggregate(avg=Avg('max_score'))['avg'] or 100
            
            if avg_max_score > 0:
                accuracy = (avg_score / avg_max_score) * 100
            else:
                accuracy = 0.0
        else:
            accuracy = 0.0
        
        statistics = [{
            'label': '전체 정답률',
            'value': round(accuracy, 2)
        }]
        
        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_pass_prediction(self, request):
        """합격 기준 대비 현재 점수 분석"""
        user = request.user
        
        # 시험 데이터에서 평균 점수 계산
        exams = Exam.objects.filter(
            user=user,
            score__isnull=False
        )
        
        if exams.exists():
            # 평균 점수와 만점 계산
            avg_score = exams.aggregate(avg=Avg('score'))['avg'] or 0
            avg_max_score = exams.aggregate(avg=Avg('max_score'))['avg'] or 0
            
            if avg_max_score > 0:
                current_percentage = (avg_score / avg_max_score) * 100
            else:
                current_percentage = 0.0
            
            # 합격 기준을 70%로 가정 (실제로는 설정 가능하도록 해야 함)
            pass_standard = 70.0
            gap = current_percentage - pass_standard
            
            statistics = [
                {
                    'label': '현재 평균 점수',
                    'value': round(current_percentage, 2)
                },
                {
                    'label': '합격 기준',
                    'value': pass_standard
                },
                {
                    'label': '차이',
                    'value': round(gap, 2)
                }
            ]
        else:
            statistics = [{
                'label': '데이터 없음',
                'value': 0.0
            }]
        
        serializer = StatisticsSerializer(statistics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
