from rest_framework import serializers
from .models import Party, Case, ValidationResult, ProceduralRule

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class ValidationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationResult
        fields = ['is_accepted', 'rejection_reasons', 'ai_analysis', 'generated_reasoning', 'confidence_score']

class CaseSerializer(serializers.ModelSerializer):
    plaintiff = PartySerializer()
    defendant = PartySerializer()
    validation_result = ValidationResultSerializer(read_only=True)
    
    class Meta:
        model = Case
        fields = [
            'id', 'title', 'description', 
            'incident_date', 'grievance_date', 'submission_date',
            'plaintiff', 'defendant',
            'court_type', 'claim_amount', 'status', 'documents',
            'validation_result'
        ]

    def create(self, validated_data):
        # Handle nested writes for parties if needed, or assume IDs. 
        # For simplicity in this demo, we'll create parties if provided as dicts.
        plaintiff_data = validated_data.pop('plaintiff')
        defendant_data = validated_data.pop('defendant')
        
        plaintiff, _ = Party.objects.get_or_create(**plaintiff_data)
        defendant, _ = Party.objects.get_or_create(**defendant_data)
        
        case = Case.objects.create(plaintiff=plaintiff, defendant=defendant, **validated_data)
        return case
