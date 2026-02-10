"""
스터디 관련 시리얼라이저
"""
from rest_framework import serializers
from .models import StudyEvent, StudyTimer, StudyContent


class StudySerializer(serializers.ModelSerializer):
    """스터디 이벤트 시리얼라이저"""
    
    class Meta:
        model = StudyEvent
        fields = ['id', 'title', 'goal', 'start_at', 'end_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """스터디 이벤트 생성 시 현재 사용자 자동 할당"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class TimerStartSerializer(serializers.ModelSerializer):
    """타이머 시작 시리얼라이저"""
    
    class Meta:
        model = StudyTimer
        fields = ['started_at']
        read_only_fields = ['started_at']


class TimerEndSerializer(serializers.ModelSerializer):
    """타이머 종료 시리얼라이저"""
    
    class Meta:
        model = StudyTimer
        fields = ['ended_at', 'total_minutes']
        read_only_fields = ['ended_at', 'total_minutes']


class StudyContentSerializer(serializers.ModelSerializer):
    """공부 내용 시리얼라이저"""
    
    class Meta:
        model = StudyContent
        fields = ['id', 'content', 'duration_minutes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
