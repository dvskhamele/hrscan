from django.db import models

class ApplicantCV(models.Model):
    applicant_name = models.CharField(max_length=50)
    applicant_cv = models.FileField()
    upload_date = models.DateTimeField(auto_now=True)

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
