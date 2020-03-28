from django.db import models


class TaskList(models.Model):
    task = models.TextField(max_length=300)
    is_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    time_left = models.DateTimeField()

    def __str__(self):
        return f"{self.task}"

    class Meta:
        ordering = ['is_completed', 'date_created']
