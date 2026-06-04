from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    intervention_status = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_intervention_status(self, obj):
        try:
            return obj.intervention.status
        except:
            return None


from .models import Message, Intervention

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

class InterventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intervention
        fields = '__all__'
