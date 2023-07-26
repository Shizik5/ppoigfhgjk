from rest_framework import serializers
from history_orders.models import History


class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = History
        fields = '__all__'
