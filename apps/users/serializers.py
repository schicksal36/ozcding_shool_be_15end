from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소 (로그인용, 고유값)"
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="비밀번호 (최소 8자)"
    )
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="닉네임 (옵션)"
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소 (로그인용)"
    )
    password = serializers.CharField(
        write_only=True,
        help_text="비밀번호"
    )


class LoginOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="리프레시 토큰 (블랙리스트에 추가할 토큰)"
    )


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        read_only=True,
        help_text="이메일 주소 (읽기 전용, 수정 불가)"
    )
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="닉네임 (수정 가능)"
    )


class ProfileSerializer(serializers.Serializer):
    nickname = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="닉네임 (프로필 표시용)"
    )
    bio = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="자기소개 (프로필 메시지)"
    )
    profile_image = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text="프로필 이미지 (이미지 파일 업로드 가능)"
    )


class EmailSendSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소 (인증 코드를 받을 이메일)"
    )


class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소"
    )
    code = serializers.CharField(
        help_text="이메일 인증 코드 (6자리 숫자)"
    )


class EmailExistCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="가입 여부 확인용 이메일"
    )


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소 (재설정 코드를 받을 이메일)"
    )


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="이메일 주소"
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="새 비밀번호 (최소 8자, 응답에 포함되지 않음)"
    )


class DestroySerializer(serializers.Serializer):
    pass
