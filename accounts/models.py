from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# Create your models here.

class Profile(models.Model):
  user=models.ForeignKey(User,on_delete=CASCADE)
  auth_token=models.CharField(max_length=100)
  is_varified=models.BooleanField(default=False)
  created_at=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.user.username



