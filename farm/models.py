from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FarmModel(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=True)
    location=models.CharField(max_length=80)
    area=models.DecimalField(max_digits=8,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.name or self.name.strip() == '':
            farm_count = FarmModel.objects.count() + 1
            self.name = f"مزرعه شماره {farm_count}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class FieldModel(models.Model):
    farm=models.ForeignKey(FarmModel,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    area=models.DecimalField(max_digits=8,decimal_places=2)
    crop_name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name