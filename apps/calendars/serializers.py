"""
일정 및 시험 관련 시리얼라이저
"""
from rest_framework import serializers
from .models import Event, RepeatEvent, Exam


class CalendarSerializer(serializers.ModelSerializer):
    """일정 시리얼라이저"""
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'start_at', 'end_at', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RepeatCalendarSerializer(serializers.ModelSerializer):
    """반복 일정 시리얼라이저"""
    
    class Meta:
        model = RepeatEvent
        fields = ['id', 'title', 'start_at', 'end_at', 'description', 'rule', 'until', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """반복 일정 생성 시 현재 사용자 자동 할당"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExamSerializer(serializers.ModelSerializer):
    """시험 시리얼라이저"""
    
    class Meta:
        model = Exam
        fields = ['id', 'subject', 'exam_date', 'score', 'max_score', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """시험 생성 시 현재 사용자 자동 할당"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
