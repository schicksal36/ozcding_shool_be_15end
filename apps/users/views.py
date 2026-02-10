"""
사용자 관련 API 뷰 모듈
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest, OpenApiExample

from .models import CustomUser
from .services import (
    AuthService,
    UserService,
    EmailVerificationService,
    PasswordResetService,
)
from .utils import TokenService
from .exceptions import UserException
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LoginOutSerializer,
    UserSerializer,
    ProfileSerializer,
    DestroySerializer,
    EmailSendSerializer,
    EmailVerifySerializer,
    EmailExistCheckSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)


@extend_schema(
    tags=['인증'],
    summary='회원가입',
    description='사용자 계정을 생성합니다 (이메일 기반)',
    examples=[
        OpenApiExample(
            '회원가입 예시',
            value={
                'email': 'user@example.com',
                'password': 'password123',
                'nickname': '사용자'
            },
            request_only=True,
        ),
    ],
)
class RegisterView(generics.CreateAPIView):
    """회원가입 API"""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """사용자 생성"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            result = AuthService.register(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                nickname=serializer.validated_data.get('nickname', ''),
            )
            
            response = Response({
                'message': '회원가입이 완료되었습니다.',
                **result
            }, status=status.HTTP_201_CREATED, content_type='application/json')
            return response
        except UserException as e:
            response = e.to_response()
            response['Content-Type'] = 'application/json'
            return response


@extend_schema(
    tags=['인증'],
    summary='로그인',
    description='이메일과 비밀번호로 로그인하고 인증 토큰을 발급합니다',
    request=LoginSerializer,
    examples=[
        OpenApiExample(
            '로그인 예시',
            value={
                'email': 'user@example.com',
                'password': 'password123'
            },
            request_only=True,
        ),
    ],
)
class LoginView(APIView):
    """로그인 API"""
    permission_classes = [AllowAny]
    renderer_classes = [JSONRenderer]
    
    def get_parsers(self):
        """form-data와 JSON 모두 처리"""
        return [JSONParser(), FormParser(), MultiPartParser()]
    
    def get_renderers(self):
        """항상 JSON 렌더러만 사용"""
        return [JSONRenderer()]
    
    def perform_content_negotiation(self, request, force=False):
        """Content negotiation을 강제로 JSON으로 설정"""
        return (JSONRenderer(), 'application/json')
    
    def dispatch(self, request, *args, **kwargs):
        """Accept 헤더를 강제로 application/json으로 설정"""
        if request.method == 'POST':
            request.META['HTTP_ACCEPT'] = 'application/json'
            # Accept-Language도 제거하여 HTML 렌더링 방지
            if 'HTTP_ACCEPT_LANGUAGE' in request.META:
                del request.META['HTTP_ACCEPT_LANGUAGE']
        return super().dispatch(request, *args, **kwargs)
    
    def finalize_response(self, request, response, *args, **kwargs):
        """응답 최종화 시 Content-Type 강제 설정"""
        response = super().finalize_response(request, response, *args, **kwargs)
        # Content-Type을 강제로 application/json으로 설정
        response['Content-Type'] = 'application/json'
        return response
    
    def post(self, request, *args, **kwargs):
        """로그인 처리"""
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'error': '입력 데이터가 올바르지 않습니다.',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
        
        try:
            result = AuthService.login(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
            )
            
            response = Response({
                'message': '로그인 성공',
                **result
            }, status=status.HTTP_200_OK, content_type='application/json')
            return response
        except UserException as e:
            response = e.to_response()
            response['Content-Type'] = 'application/json'
            return response


@extend_schema(
    tags=['인증'],
    summary='로그아웃',
    description='현재 로그인된 사용자의 인증 정보를 무효화합니다',
    methods=['POST'],
    request=LoginOutSerializer,
    examples=[
        OpenApiExample(
            '로그아웃 예시',
            value={
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
            },
            request_only=True,
        ),
    ],
)
class LogoutView(APIView):
    """로그아웃 API"""
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @extend_schema(
        request=LoginOutSerializer,
        examples=[
            OpenApiExample(
                '로그아웃 예시',
                value={
                    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
                },
            ),
        ],
    )
    def post(self, request):
        """로그아웃 처리"""
        serializer = LoginOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=False)

        refresh_token = serializer.validated_data.get("refresh")

        if refresh_token:
            try:
                TokenService.blacklist_token(refresh_token)
            except Exception:
                pass

        return Response(
            {"message": "로그아웃되었습니다."},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
        
    def get(self, request):
        """GET 요청은 허용되지 않음"""
        return Response(
            {"error": "이 엔드포인트는 POST 메서드만 지원합니다."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@extend_schema(
    tags=['사용자 정보'],
    summary='유저 정보 조회/수정',
    description='로그인한 사용자의 기본 정보를 조회하거나 수정합니다',
    request=UserSerializer,
    examples=[
        OpenApiExample(
            '유저 정보 수정 예시',
            value={
                'nickname': '새 닉네임'
            },
            request_only=True,
        ),
    ],
)
class ProfileView(generics.RetrieveUpdateAPIView):
    """유저 정보 조회/수정 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        """현재 로그인한 사용자 반환"""
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """유저 정보 조회"""
        user = self.get_object()
        serializer = self.get_serializer({
            'email': user.email,
            'nickname': user.nickname,
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """유저 정보 수정"""
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        if 'nickname' in serializer.validated_data:
            user.nickname = serializer.validated_data['nickname']
            user.save(update_fields=['nickname'])
        
        return Response({
            'email': user.email,
            'nickname': user.nickname,
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['인증'],
    summary='회원탈퇴',
    description='사용자의 계정을 삭제합니다',
    methods=['DELETE'],
    request=None,
)
class UserDeleteView(generics.DestroyAPIView):
    """회원탈퇴 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = DestroySerializer
    
    def get_object(self):
        """삭제할 사용자 객체 반환"""
        return self.request.user
    
    def destroy(self, request, *args, **kwargs):
        """회원탈퇴 처리"""
        user = self.get_object()
        user.delete()
        return Response({'message': '회원탈퇴가 완료되었습니다.'}, status=status.HTTP_200_OK)


@extend_schema(
    tags=['사용자 정보'],
    summary='유저 프로필 조회/수정',
    description='로그인한 사용자의 프로필 정보를 조회하거나 수정합니다 (닉네임, 소개, 프로필 이미지 등)',
    request=ProfileSerializer,
    examples=[
        OpenApiExample(
            '프로필 수정 예시',
            value={
                'nickname': '새 닉네임',
                'bio': '자기소개 내용',
            },
            request_only=True,
        ),
    ],
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """유저 프로필 조회/수정 API"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get_object(self):
        """현재 로그인한 사용자 반환"""
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """프로필 정보 조회"""
        user = self.get_object()
        serializer = self.get_serializer({
            'nickname': user.nickname,
            'bio': user.bio,
            'profile_image': user.profile_image.url if user.profile_image else None,
        })
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        """프로필 정보 수정"""
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        if 'nickname' in serializer.validated_data:
            user.nickname = serializer.validated_data['nickname']
        if 'bio' in serializer.validated_data:
            user.bio = serializer.validated_data['bio']
        if 'profile_image' in serializer.validated_data:
            user.profile_image = serializer.validated_data['profile_image']
        
        user.save()
        
        return Response({
            'nickname': user.nickname,
            'bio': user.bio,
            'profile_image': user.profile_image.url if user.profile_image else None,
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['이메일 인증'],
    summary='이메일 인증 코드 발송',
    description='입력한 이메일로 인증 코드를 발송합니다',
    methods=['POST'],
    request=EmailSendSerializer,
    examples=[
        OpenApiExample(
            '이메일 인증 코드 발송 예시',
            value={
                'email': 'schicksal36@outlook.com'
            },
            request_only=True,
        ),
    ],
)
class EmailView(APIView):
    """이메일 인증 코드 발송 API"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=EmailSendSerializer,
        examples=[
            OpenApiExample(
                '이메일 인증 코드 발송 예시',
                value={
                    'email': 'schicksal36@outlook.com'
                },
            ),
        ],
    )
    def post(self, request):
        """인증 코드 발송"""
        serializer = EmailSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            code = EmailVerificationService.send_verification_code(
                email=serializer.validated_data['email']
            )
            
            return Response({
                'message': '인증 코드가 발송되었습니다.',
                'code': code
            }, status=status.HTTP_200_OK)
        except UserException as e:
            return e.to_response()


@extend_schema(
    tags=['이메일 인증'],
    summary='이메일 인증 확인',
    description='회원가입 또는 비밀번호 재설정 시 사용합니다',
    methods=['POST'],
    request=EmailVerifySerializer,
    examples=[
        OpenApiExample(
            '이메일 인증 확인 예시',
            value={
                'email': 'user@example.com',
                'code': '123456'
            },
            request_only=True,
        ),
    ],
)
class EmailVerifyView(APIView):
    """이메일 인증 확인 API"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=EmailVerifySerializer,
        examples=[
            OpenApiExample(
                '이메일 인증 확인 예시',
                value={
                    'email': 'user@example.com',
                    'code': '123456'
                },
            ),
        ],
    )
    def post(self, request):
        """인증 코드 확인"""
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            EmailVerificationService.verify_code(
                email=serializer.validated_data['email'],
                code=serializer.validated_data['code']
            )
            
            return Response({
                'message': '이메일 인증이 완료되었습니다.'
            }, status=status.HTTP_200_OK)
        except UserException as e:
            return e.to_response()


@extend_schema(
    tags=['이메일 인증'],
    summary='이메일 가입 여부 확인',
    description='이메일로 가입된 계정이 있는지 확인합니다',
    methods=['POST'],
    request=EmailExistCheckSerializer,
    examples=[
        OpenApiExample(
            '이메일 가입 여부 확인 예시',
            value={
                'email': 'user@example.com'
            },
            request_only=True,
        ),
    ],
)
class EmailExistCheckView(APIView):
    """이메일 가입 여부 확인 API"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=EmailExistCheckSerializer,
        examples=[
            OpenApiExample(
                '이메일 가입 여부 확인 예시',
                value={
                    'email': 'user@example.com'
                },
            ),
        ],
    )
    def post(self, request):
        """이메일 가입 여부 확인"""
        serializer = EmailExistCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        exists = UserService.check_email_exists(serializer.validated_data['email'])
        
        return Response({
            'email': serializer.validated_data['email'],
            'exists': exists
        }, status=status.HTTP_200_OK)


@extend_schema(
    tags=['비밀번호 재설정'],
    summary='비밀번호 재설정 요청',
    description='이메일 가입 여부를 확인하고 재설정 코드를 발송합니다',
    methods=['POST'],
    request=PasswordResetRequestSerializer,
    examples=[
        OpenApiExample(
            '비밀번호 재설정 요청 예시',
            value={
                'email': 'user@example.com'
            },
            request_only=True,
        ),
    ],
)
class PasswordResetRequestView(APIView):
    """비밀번호 재설정 요청 API"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=PasswordResetRequestSerializer,
        examples=[
            OpenApiExample(
                '비밀번호 재설정 요청 예시',
                value={
                    'email': 'user@example.com'
                },
            ),
        ],
    )
    def post(self, request):
        """비밀번호 재설정 요청"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            code = PasswordResetService.request_reset(
                email=serializer.validated_data['email']
            )
            
            return Response({
                'message': '비밀번호 재설정 코드가 발송되었습니다.',
                'code': code
            }, status=status.HTTP_200_OK)
        except UserException as e:
            return e.to_response()


@extend_schema(
    tags=['비밀번호 재설정'],
    summary='비밀번호 재설정 완료',
    description='이메일 인증 후 새로운 비밀번호로 변경합니다',
    methods=['POST'],
    request=PasswordResetConfirmSerializer,
    examples=[
        OpenApiExample(
            '비밀번호 재설정 완료 예시',
            value={
                'email': 'user@example.com',
                'new_password': 'newpassword123'
            },
            request_only=True,
        ),
    ],
)
class PasswordResetConfirmView(APIView):
    """비밀번호 재설정 완료 API"""
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=PasswordResetConfirmSerializer,
        examples=[
            OpenApiExample(
                '비밀번호 재설정 완료 예시',
                value={
                    'email': 'user@example.com',
                    'new_password': 'newpassword123'
                },
            ),
        ],
    )
    def post(self, request):
        """비밀번호 재설정 완료"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            PasswordResetService.confirm_reset(
                email=serializer.validated_data['email'],
                new_password=serializer.validated_data['new_password']
            )
            
            return Response({
                'message': '비밀번호가 재설정되었습니다.'
            }, status=status.HTTP_200_OK)
        except UserException as e:
            return e.to_response()
