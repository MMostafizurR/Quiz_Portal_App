from django.contrib.auth.models import User
from django.db import models


class Quiz(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()

  def __str__(self):
    return self.title


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
  question = models.TextField()

  def __str__(self):
    return self.question


class Option(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  option = models.CharField(max_length=255)
  is_correct = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.option} ({'Correct' if self.is_correct else 'Wrong'})"


class Participant(models.Model):
  GENDER_CHOICES = [
      ('Male', 'Male'),
      ('Female', 'Female'),
      ('Other', 'Other'),
  ]

  user = models.OneToOneField(User, on_delete=models.CASCADE)
  Name = models.CharField(max_length=100)
  Class = models.CharField(max_length=50)
  Age = models.IntegerField()
  Gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
  Institution = models.CharField(max_length=150)

  def __str__(self):
    return self.Name