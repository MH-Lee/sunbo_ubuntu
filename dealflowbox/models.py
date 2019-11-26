from django.db import models

STATUS =  (
    ('0', '업데이트 필요'),
    ('1', '최신'),
)

# Create your models here.
class UpdateChecker(models.Model):
    recent_date = models.CharField(max_length=8, blank=True, null=True, \
                                   verbose_name='업데이트 날짜')
    status = models.CharField(max_length=1, choices=STATUS, blank=True, null=True, \
                              verbose_name='업데이트 여부')
    update_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '{}-{}'.format(self.update_date, self.status)

    class Meta:
        db_table = 'update_checker'
        verbose_name = '정보업데이트 확인'
        verbose_name_plural = '정보업데이트 확인'


class DealFlowBox(models.Model):
    date = models.CharField(max_length=10, blank=True, null=True, verbose_name='날짜')
    company_name = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name='회사명')
    file_url = models.CharField(max_length=255, blank=True, null=True, \
                                verbose_name='파일URL')
    sector = models.CharField(max_length=20, blank=True, null=True, \
                              verbose_name='회사업종')
    person_in_charge = models.CharField(max_length=100, blank=True, null=True,\
                                       verbose_name='담당자')
    funding_stage = models.CharField(max_length=100, blank=True, null=True,\
                                    verbose_name='투자단계')
    office = models.CharField(max_length=100, blank=True, null=True,\
                             verbose_name='담당오피스')
    business_detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'dealflowbox'
        verbose_name = 'dealflowbox 정보'
        verbose_name_plural = 'dealflowbox 정보'
