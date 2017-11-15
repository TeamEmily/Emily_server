# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Weather(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=45)
    morn_temperature = models.CharField(max_length=45, blank=True, null=True)
    morn_weather = models.CharField(max_length=45)
    morn_rainfall = models.CharField(max_length=45, blank=True, null=True)
    noon_temperature = models.CharField(max_length=45, blank=True, null=True)
    noon_weather = models.CharField(max_length=45)
    noon_rainfall = models.CharField(max_length=45, blank=True, null=True)
    current_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'weather'
        unique_together = (('city_id', 'current_date'),)
