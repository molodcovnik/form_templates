from django.db import models


class FormTypeEnum(models.TextChoices):
    EMAIL = 'EMAIL'
    PHONE = 'PHONE'
    DATE = 'DATE'
    TEXT = 'TEXT'


class Field(models.Model):
    name = models.CharField(max_length=64)
    field_type = models.CharField(choices=FormTypeEnum.choices,
                                  default=FormTypeEnum.TEXT,
                                  max_length=16)

    def __str__(self):
        return f'{self.name} {self.field_type}'


class Template(models.Model):
    name = models.CharField(max_length=64, unique=True)
    fields = models.ManyToManyField(Field, related_name='forms')

    def __str__(self):
        return f'{self.name} {self.fields}'

