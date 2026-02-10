from rest_framework import status
from rest_framework.response import Response


class UserException(Exception):
    default_message = "사용자 관련 오류가 발생했습니다."
    default_status = status.HTTP_400_BAD_REQUEST

    def __init__(self, message=None, status_code=None):
        self.message = message or self.default_message
        self.status_code = status_code or self.default_status
        super().__init__(self.message)

    def to_response(self):
        return Response(
            {'error': self.message},
            status=self.status_code,
            content_type='application/json'
        )


class UserNotFoundError(UserException):
    default_message = "해당 이메일로 가입된 사용자가 없습니다."
    default_status = status.HTTP_404_NOT_FOUND


class AuthenticationError(UserException):
    default_message = "아이디 또는 비밀번호가 올바르지 않습니다."
    default_status = status.HTTP_401_UNAUTHORIZED


class InvalidVerificationCodeError(UserException):
    default_message = "인증 코드가 올바르지 않습니다."
    default_status = status.HTTP_400_BAD_REQUEST


class ExpiredVerificationCodeError(UserException):
    default_message = "인증 코드가 만료되었습니다."
    default_status = status.HTTP_400_BAD_REQUEST


class InactiveUserError(UserException):
    default_message = "비활성화된 계정입니다."
    default_status = status.HTTP_403_FORBIDDEN


class InvalidPasswordError(UserException):
    default_message = "비밀번호가 올바르지 않습니다."
    default_status = status.HTTP_400_BAD_REQUEST


class EmailAlreadyExistsError(UserException):
    default_message = "이미 가입된 이메일입니다."
    default_status = status.HTTP_400_BAD_REQUEST
