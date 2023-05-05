from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class TradingBot(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    bot_response = models.TextField()
    
    def __str__(self):
        return str(f"{self.user.username} ({self.message})")
