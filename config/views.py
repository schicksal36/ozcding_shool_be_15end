"""
프로젝트 루트 레벨 뷰
"""
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class RootView(APIView):
    """
    루트 경로(/) API 정보 뷰
    
    엔드포인트: GET /
    인증 필요: 없음
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        API 정보 반환
        """
        return Response({
            'name': 'Study Calendar API',
            'version': '1.0.0',
            'description': 'Study Calendar 프로젝트의 REST API 서버입니다.',
            'endpoints': {
                'api_documentation': '/api/schema/swagger-ui/',
                'admin': '/admin/',
                'users': '/api/users/me/',
                'login': '/api/login/',
                'signup': '/api/signup/',
                'calendars': '/api/events/',
                'exams': '/api/exams/',
                'study': '/api/study-events/',
                'reports': '/api/statistics/',
            }
        })


class APIRootView(APIView):
    """
    API 루트 경로(/api/) 정보 뷰
    
    엔드포인트: GET /api/
    인증 필요: 없음
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """
        API 정보 반환
        """
        return Response({
            'name': 'Study Calendar API',
            'version': '1.0.0',
            'description': 'Study Calendar 프로젝트의 REST API 서버입니다.',
            'endpoints': {
                'api_documentation': '/api/schema/swagger-ui/',
                'admin': '/admin/',
                'authentication': {
                    'login': '/api/login/',
                    'signup': '/api/signup/',
                    'logout': '/api/logout',
                },
                'users': {
                    'profile': '/api/users/me/',
                    'profile_detail': '/api/users/me/profile/',
                    'account_delete': '/api/users/account/',
                },
                'email': {
                    'send_code': '/api/users/email/verify/',
                    'verify_code': '/api/users/email/verify/confirm/',
                    'check_exists': '/api/users/find/email/',
                },
                'password': {
                    'reset_request': '/api/users/password/reset/',
                    'reset_confirm': '/api/users/password/reset/confirm/',
                },
                'calendars': '/api/events/',
                'exams': '/api/exams/',
                'study': '/api/study-events/',
                'reports': '/api/statistics/',
            }
        })
