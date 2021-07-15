from rest_framework import serializers

from app.models import CsvData


class CsvSerializer(serializers.ModelSerializer):
    # If your <field_name> is declared on your serializer with the parameter required=False
    # then this validation step will not take place if the field is not included.
    class Meta:
        model = CsvData
        # fields = '__all__'
        fields = (
            'id', 'source_ip', 'source_port', 'destination_ip', 'destination_port', 'dns_record', 'datetime_record')
