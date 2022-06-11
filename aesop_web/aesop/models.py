from cgitb import text
from turtle import title
from django.db import models


class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

class Story(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    title = models.TextField()
    text = models.TextField()
    image = models.TextField()
