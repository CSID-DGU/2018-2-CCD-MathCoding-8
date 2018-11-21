# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# python manage.py inspectdb > frontpage/models.py 이용하여 DB 이식
# db생성한 후, db.sqlite3로 파일이름 바꿔줌. 그리고 django가 생성한 db.sqlite3 지우고 복사.

class Temp(models.Model):
    origin = models.TextField(blank=True, null=True)
    synonym = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp'
