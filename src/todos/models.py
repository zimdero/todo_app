from django.db import models
from django.contrib.auth.models import User

# Create your models here.

HEIGHEST = 1
MEDIUM = 2
LOWEST = 3
PRIORITY_CHOICES = (
    (HEIGHEST, 'highest'),
    (MEDIUM, 'medium'),
    (LOWEST, 'lowest'),
)

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    due_time = models.DateField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES,
                                null=True, default=PRIORITY_CHOICES[1][0])

    def __str__(self):
        return self.title
