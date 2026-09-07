from rest_framework.permissions import BasePermission
from .models import FarmModel

class IsFarmOwnerAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.owner == request.user

class IsFieldOwnerAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.user.is_staff:
            return True
        
        if view.action == "create":
            farm_id = request.data.get("farm")

            return FarmModel.objects.filter(id=farm_id,owner=request.user).exists()

        return True


    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.farm.owner == request.user