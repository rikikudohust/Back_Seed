from django.db import models
from django.db.models.enums import Choices

class Menu(models.Model):
    Daily = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
    ]
    food = models.CharField(max_length=100,default='')
    day = models.IntegerField(Choices=Daily,default='0')
    
    


