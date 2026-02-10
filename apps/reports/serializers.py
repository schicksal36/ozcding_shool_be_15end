"""
통계 관련 시리얼라이저
"""
from rest_framework import serializers


class StatisticsSerializer(serializers.Serializer):
    """통계 시리얼라이저"""
    label = serializers.CharField(help_text="통계 항목 (예: 과목명)")
    value = serializers.FloatField(help_text="계산된 값 (예: 시간, 점수, 비율)")
