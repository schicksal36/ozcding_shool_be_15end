#studycalender\core\api_spec.py
from rest_framework import serializers


# =====================================================
# 1. Users App (회원 / 인증)
# =====================================================

# 회원가입
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, help_text="사용자 아이디")
    email = serializers.EmailField(help_text="이메일 주소")
    password = serializers.CharField(write_only=True, min_length=8)
    nickname = serializers.CharField(required=False, help_text="닉네임")


# 로그인
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="아이디")
    password = serializers.CharField(write_only=True, help_text="비밀번호")


# 유저 기본 정보
class UserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    nickname = serializers.CharField(required=False, allow_blank=True)


# 유저 프로필 (화면 표시용)
class ProfileSerializer(serializers.Serializer):
    nickname = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)


# 이메일 인증 코드 발송
class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField()


# 이메일 인증 확인
class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(help_text="이메일 인증 코드")


# 이메일 가입 여부 확인
class EmailExistCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="가입 여부 확인용 이메일")


# 비밀번호 재설정 요청
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


# 비밀번호 재설정 완료
class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, min_length=8)




# =====================================================
# 2. Calendar App (일정 / 반복 일정)
# =====================================================

class CalendarCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    description = serializers.CharField(required=False)


class CalendarSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()
    description = serializers.CharField(required=False)


# 반복 일정
class RepeatCalendarSerializer(serializers.Serializer):
    rule = serializers.CharField(help_text="RRULE 반복 규칙")
    until = serializers.DateField(help_text="반복 종료일")


# =====================================================
# 3. Study App (스터디 / 타이머 / 공부내용)
# =====================================================

class StudySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(help_text="스터디 제목")
    goal = serializers.CharField(help_text="학습 목표")
    start_at = serializers.DateTimeField()
    end_at = serializers.DateTimeField()


# 타이머 시작
class TimerStartSerializer(serializers.Serializer):
    started_at = serializers.DateTimeField(read_only=True)


# 타이머 종료
class TimerEndSerializer(serializers.Serializer):
    ended_at = serializers.DateTimeField(read_only=True)
    total_minutes = serializers.IntegerField(read_only=True)


# 공부 내용
class StudyContentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(help_text="공부한 내용")
    duration_minutes = serializers.IntegerField(help_text="공부 시간(분)")
    created_at = serializers.DateTimeField(read_only=True)


# =====================================================
# 4. Exam App (시험)
# =====================================================

class ExamSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    subject = serializers.CharField()
    exam_date = serializers.DateField()
    score = serializers.IntegerField(required=False)
    max_score = serializers.IntegerField()



# =====================================================
# 7. Statistics App (통계)
# =====================================================

class StatisticsSerializer(serializers.Serializer):
    label = serializers.CharField(help_text="통계 항목")
    value = serializers.FloatField(help_text="계산된 값")
