from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model with coordinate validation.
    """
    employee_id = serializers.IntegerField(write_only=True, required=False)
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'employee_id', 'employee_name', 'latitude', 
                  'longitude', 'accuracy', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'employee_name']
    
    def validate_latitude(self, value):
        """
        Validate that latitude is between -90 and 90 degrees.
        """
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90 degrees"
            )
        return value
    
    def validate_longitude(self, value):
        """
        Validate that longitude is between -180 and 180 degrees.
        """
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180 degrees"
            )
        return value
    
    def validate_accuracy(self, value):
        """
        Validate that accuracy is a positive number.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Accuracy must be a positive number"
            )
        return value
    
    def create(self, validated_data):
        """
        Create a new location record.
        Handle employee_id if provided, otherwise use request user.
        """
        employee_id = validated_data.pop('employee_id', None)
        
        # Get employee from context (set by viewset)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            employee = request.user
        elif employee_id:
            try:
                employee = User.objects.get(id=employee_id)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"employee_id": "Employee with this ID does not exist"}
                )
        else:
            raise serializers.ValidationError(
                {"employee_id": "Employee ID is required"}
            )
        
        validated_data['employee'] = employee
        return super().create(validated_data)
