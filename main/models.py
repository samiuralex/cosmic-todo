from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Todo(models.Model):
    PRIORITY_CHOICES = [
        (1, 'Low Priority'),
        (2, 'Medium Priority'),
        (3, 'High Priority')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Temporarily nullable
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=1)

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_date:
            self.completed_date = timezone.now()
        elif not self.completed:
            self.completed_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.username if self.user else 'No User'}"

    class Meta:
        ordering = ['-priority', 'due_date', '-created_date']
