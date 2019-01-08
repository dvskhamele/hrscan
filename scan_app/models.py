from django.db import models
import os
import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class ApplicantCV(models.Model):
    applicant_name = models.CharField(max_length=50)
    applicant_cv = models.FileField()
    upload_date = models.DateTimeField(auto_now=True)
    cv_ext = models.CharField(max_length=5)

    def __str__(self):
        return self.applicant_name

class ApplicantCollege(models.Model):
    clg_name = models.CharField(max_length=100)
    clg_rank = models.CharField(max_length=3)

    def __str__(self):
        return self.clg_name

class ApplicantDegree(models.Model):
    degree = models.CharField(max_length=100)
    degree_rank = models.CharField(max_length=3)

    def __str__(self):
        return self.degree

class CVKeywords(models.Model):
    k_value = models.CharField(max_length=50)

    def __str__(self):
        return self.k_value

class Neg_keywords(models.Model):
    n_value = models.CharField(max_length=50)

    def __str__(self):
        return self.n_value


@receiver(models.signals.post_delete, sender=ApplicantCV)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ApplicantCV` object is deleted.
    """
    if instance.applicant_cv:
        if os.path.isfile(instance.applicant_cv.path):
            os.remove(instance.applicant_cv.path)


@receiver(models.signals.pre_save, sender=ApplicantCV)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `ApplicantCV` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = ApplicantCV.objects.get(pk=instance.pk).applicant_cv
    except ApplicantCV.DoesNotExist:
        return False

    new_file = instance.applicant_cv
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
