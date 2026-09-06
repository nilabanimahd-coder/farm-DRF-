from rest_framework import serializers
from .models import FarmModel,FieldModel



class MinAreaValidator:

    def __init__(self,min_price):
        self.min_price=min_price

    def __call__(self, value):
        if value <= self.min_price:
            raise serializers.ValidationError("price is not be 0")
        return value

class FieldSerializer(serializers.ModelSerializer):

    def validate(self,attrs):

        farm = attrs.get('farm')
        if not farm and self.instance:
            farm = self.instance.farm

        new_area = attrs['area']

        used_area= sum(field.area for field in farm.field.all())
        
        if self.instance:
            used_area -= self.instance.area

        remaining_area = farm.area - used_area

        if new_area > remaining_area :
           raise serializers.ValidationError("Area of fields cannot be greater than remaining farm area.")
    
        return attrs

    area=serializers.DecimalField(max_digits=8,decimal_places=2,validators=[MinAreaValidator(0)])

    class Meta:
        model=FieldModel
        fields=['id','name','area','crop_name','farm']
        read_only_fields = ["id","created_at"]



class FarmListSerializer(serializers.ModelSerializer):

    field_count=serializers.IntegerField(source="field.count")

    class Meta:
        model=FarmModel
        fields=['id','owner','name','area','location','field_count','created_at']
        read_only_fields = ["id","owner","created_at","field_count"]

    
class FarmDetaielSerializer(serializers.ModelSerializer):

    area=serializers.DecimalField(max_digits=8,decimal_places=2,validators=[MinAreaValidator(0)])
    field=FieldSerializer(many=True,read_only=True)
    field_count=serializers.IntegerField(source="field.count")

    class Meta:
        model=FarmModel
        fields=['id','owner','name','area','location','field_count','field','created_at']
        read_only_fields = ["id","owner","created_at","field_count"]