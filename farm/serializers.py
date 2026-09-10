from rest_framework import serializers
from .models import FarmModel,FieldModel



class MinAreaValidator:

    def __init__(self,min_area):
        self.min_area=min_area

    def __call__(self, value):
        if value <= self.min_area:
            raise serializers.ValidationError("area is not be 0")
        return value

class FieldSerializer(serializers.ModelSerializer):

    def validate(self,attrs):

        farm = self.instance

        new_area = attrs.get('area')

        if new_area is None and self.instance:
            new_area = self.instance.area

        used_area= sum(field.area for field in farm.field.all())
        
        if self.instance:
            used_area -= self.instance.area

        remaining_area = farm.area - used_area

        if new_area > remaining_area :
           raise serializers.ValidationError("Farm area cannot be less than the total area of its fields.")
    
        return attrs


    
    area=serializers.DecimalField(max_digits=8,decimal_places=2,validators=[MinAreaValidator(0)])
    farm_name=serializers.StringRelatedField(source='farm',read_only=True)
    owner_name = serializers.StringRelatedField(source='owner',read_only=True)

    class Meta:
        model=FieldModel
        fields=['id','owner_name','name','area','crop_name','farm','farm_name','image']
        read_only_fields = ["id","created_at","farm_name",'owner_name']



class FarmListSerializer(serializers.ModelSerializer):

    area=serializers.IntegerField(validators=[MinAreaValidator(0)])
    field_count=serializers.IntegerField(source="field.count",read_only=True)
    owner_name = serializers.StringRelatedField(source='owner',read_only=True)

    class Meta:
        model=FarmModel
        fields=['id','owner','owner_name','name','area','location','field_count','created_at']
        read_only_fields = ["id","owner","owner_name","created_at","field_count"]

    
class FarmDetailSerializer(serializers.ModelSerializer):

    def validate(self,attrs):

        field = attrs.get('field')
        if not field and self.instance:
            field = self.instance.farm

        new_area = attrs.get('area')

        if new_area is None and self.instance:
            new_area = self.instance.area

        used_area= sum(field.area for field in field.field.all())

        if new_area > used_area :
           raise serializers.ValidationError("Area of fields cannot be greater than remaining farm area.")
    
        return attrs

    owner_name = serializers.StringRelatedField(source='owner',read_only=True)
    area=serializers.DecimalField(max_digits=8,decimal_places=2,validators=[MinAreaValidator(0)])
    field=FieldSerializer(many=True,read_only=True)
    field_count=serializers.IntegerField(source="field.count",read_only=True)

    class Meta:
        model=FarmModel
        fields=['id','owner','owner_name','name','area','location','field_count','field','created_at']
        read_only_fields = ["id","owner","owner_name","created_at","field_count"]