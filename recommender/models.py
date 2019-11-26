from django.db import models

# Create your models here.
class Recommender(models.Model):
    company = models.CharField(max_length=50, null=True, blank=True)
    big_predict1 = models.CharField(max_length=100, null=True, blank=True)
    big_predict2 = models.CharField(max_length=100, null=True, blank=True)
    predicted_label1 = models.CharField(max_length=50, null=True, blank=True)
    predicted_label2 = models.CharField(max_length=50, null=True, blank=True)
    predicted_label3 = models.CharField(max_length=50, null=True, blank=True)
    establish = models.IntegerField(null=True, blank=True)
    invest = models.CharField(max_length=100, null=True, blank=True)
    tips = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    patent = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=5, null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    lable = models.FloatField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.company

    class Meta:
        db_table = 'recommender'
        verbose_name = '추천시스템_DB'
        verbose_name_plural = '추천시스템_DB'

class Result(models.Model):
    target = models.CharField(max_length=50)

    def __str__(self):
        return self.target
