import email
from pyexpat import model
from django.db import models

# Create your models here.


class zoomwebhookdata(models.Model):
    event = models.CharField(max_length=100)
    account_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    joining_time  = models.CharField(max_length=100)
    email = models.EmailField()


    def __str__(self):
        returnparameter = str(self.event)+"--id-->"+str(self.email)
        return returnparameter