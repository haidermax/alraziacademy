import os
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from uuid import uuid4
import hashlib
from django.core.validators import FileExtensionValidator

class Speciality(models.Model):
    sp_name = models.CharField(max_length=200)
    N_of_grades = models.IntegerField()

    def __str__(self):
        return self.sp_name

    def clean(self):
        n_of_grades = int(self.N_of_grades)
        if n_of_grades < 2 or n_of_grades > 6:
            raise ValidationError('Number of grades should be between 2 and 6.')



class Grade(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    grade = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.speciality.sp_name} {self.grade}"


@receiver(post_save, sender=Speciality)
def create_grades(sender, instance, created, **kwargs):
    if created:
        grades_count = min(int(instance.N_of_grades), 6)  # Convert N_of_grades to integer
        for i in range(1, grades_count + 1):
            grade_name = f"{instance.sp_name} {ordinal(i)} grade"
            Grade.objects.create(speciality=instance, grade=grade_name)



def ordinal(n):
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = suffixes.get(n % 10, 'th')
    return f"{n}{suffix}"


class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250)
    paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=7, decimal_places=0,default=0)
    members = models.ManyToManyField(User, related_name="mycourses",blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.subject

class Lecture(models.Model):
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True)
    attachment = models.FileField(upload_to='attachments', validators=[FileExtensionValidator(['pdf'])], max_length=255,blank=True)
    drive = models.TextField()
    quiz = models.URLField(blank=True)

    def __str__(self):
        return self.title

def save(self, *args, **kwargs):
    if not self.pk:
        # New lecture, encrypt the filename
        encrypted_filename = self.attachment.name
        self.attachment.name = f"{self.pk}v{encrypted_filename}"
    else:
        # Existing lecture, check if attachment has been updated
        try:
            existing_lecture = Lecture.objects.get(pk=self.pk)
            if existing_lecture.attachment != self.attachment:
                # Attachment has been changed, encrypt the filename
                self.attachment.name = self.attachment.name
        except Lecture.DoesNotExist:
            pass

    super().save(*args, **kwargs)
    