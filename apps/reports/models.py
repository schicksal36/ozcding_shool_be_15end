"""
통계 관련 모델

통계는 주로 다른 앱의 데이터를 집계하므로 별도의 모델이 필요하지 않을 수 있습니다.
하지만 통계 결과를 캐싱하거나 저장해야 한다면 모델을 추가할 수 있습니다.
"""
from django.db import models

# 통계 결과를 저장할 필요가 있다면 아래 모델을 사용할 수 있습니다.
# class StatisticsCache(models.Model):
#     """통계 결과 캐시 모델"""
#     pass
