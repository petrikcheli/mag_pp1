from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField  

class FurnaceCalculation(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calculations")
    name = models.CharField(max_length=100, blank=True, null=True)  
    input_data = models.JSONField()  # исходные данные
    result_data = models.JSONField()  # результаты расчета
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Расчет'} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
