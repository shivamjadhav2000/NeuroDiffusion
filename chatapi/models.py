from django.db import models

class PromptHistory(models.Model):
    prompt = models.TextField()
    image_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt[:30]}... @ {self.created_at.strftime('%Y-%m-%d %H:%M')}"
