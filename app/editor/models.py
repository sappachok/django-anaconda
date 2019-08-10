from django.db import models
from django.contrib import admin

# Create your models here.
class Invite(models.Model):
    name = models.CharField(max_length=500)
    branch = models.CharField(max_length=500)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("?", "Unknown")
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="?"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    RACE_CHOICES = (
        ("ASIAN", "Asian"),
        ("BLACK", "Black"),
        ("LATINO", "Latino"),
        ("WHITE", "White"),
        ("OTHER", "Other"),
        ("?", "Unknown"),
    )
    race = models.CharField(
        max_length=10,
        choices=RACE_CHOICES,
        default="?"
    )
    notes = models.TextField(blank=True)

class LabCategory(models.Model):
    name = models.CharField(max_length=200)
    LAB_CHOICE = (
        ("ASIAN", "Asian"),
        ("BLACK", "Black"),
        ("LATINO", "Latino"),
        ("WHITE", "White"),
        ("OTHER", "Other"),
        ("?", "Unknown"),
    )
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, verbose_name="Category")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return str('%s' % self.name)

class PythonCode(models.Model):
    name = models.CharField(max_length=200)
    script = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

class PythonLab(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    # CATE_CHOICES = [(x.id, x.name(), ) for x in LabCategory.objects.all()]

    categories = models.ForeignKey(LabCategory, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Category")
    description = models.TextField(blank=True)
    script = models.TextField(blank=True)

    def __unicode__(self):
        return self.name