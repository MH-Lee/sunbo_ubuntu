from django.db import models
# Create your models here.

class DartUpdateCheck(models.Model):
    recent_date = models.CharField(max_length=10, blank=True, null=True, \
                                   verbose_name='업데이트 날짜')
    update_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.recent_date

    class Meta:
        db_table = 'dart_update_checker'
        verbose_name = 'Dart 업데이트 확인'
        verbose_name_plural = 'Dart 업데이트 확인'


class RescueUpdateCheck(models.Model):
    recent_date = models.CharField(max_length=10, blank=True, null=True, \
                                   verbose_name='업데이트 날짜')
    update_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.recent_date

    class Meta:
        db_table = 'rescue_update_checker'
        verbose_name = 'Rescue 업데이트 확인'
        verbose_name_plural = 'Rescue 업데이트 확인'


class Dart(models.Model):
    company_name = models.CharField(max_length=128,
                                verbose_name="공시대상 회사")
    ticker = models.CharField(max_length=10, verbose_name="회사코드")
    date = models.CharField(max_length=10, verbose_name="공시접수일자")
    another_name = models.CharField(max_length=128, verbose_name="타법인명")
    contents = models.CharField(max_length=128, verbose_name="문서내용")
    contents_cat = models.CharField(max_length=128, verbose_name="문서종류")
    news_title = models.CharField(max_length=200, verbose_name="관련뉴스기사", null=True)
    news_url = models.CharField(max_length=500, verbose_name="관련뉴스 url", null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'dart'
        verbose_name = 'Dart 공시정보'
        verbose_name_plural = 'Dart 공시정보'


class Rescue(models.Model):
    date = models.CharField(max_length=10, verbose_name="공고일자")
    area = models.CharField(max_length=10, verbose_name="법원위치")
    case_num = models.CharField(max_length=30, verbose_name="사건번호")
    company_name = models.CharField(max_length=128, verbose_name="신청기업")
    company_address = models.CharField(max_length=128, verbose_name="신청기업주소", null=True)
    court = models.CharField(max_length=10, verbose_name="법정")
    subject = models.CharField(max_length=50, verbose_name="문서내용")
    category = models.CharField(max_length=300, verbose_name="카테고리")
    contents = models.TextField(verbose_name='판결문')
    ceo = models.CharField(max_length=30, verbose_name="ceoname", null=True)
    news_title = models.CharField(max_length=200, verbose_name="관련뉴스기사", null=True)
    news_url = models.CharField(max_length=500, verbose_name="관련뉴스 url", null=True)
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                            verbose_name='등록시간')

    def __str__(self):
        return self.case_num

    class Meta:
        db_table = 'rescue'
        verbose_name = '회생법인공고'
        verbose_name_plural = '회생법인공고'
