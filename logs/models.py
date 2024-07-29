from django.db import models

class Log(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]

    SOURCE_CHOICES = [
        ('system', 'System'),
        ('user', 'User'),
        ('network', 'Network'),
    ]

    message = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='info')
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='system')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} ({self.message_type}, {self.source})"