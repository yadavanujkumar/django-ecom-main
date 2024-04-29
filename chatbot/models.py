
# chatbot/models.py

from django.db import models

class ChatMessage(models.Model):
    user = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
