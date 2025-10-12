from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.username', read_only=True)
    recipient = serializers.CharField(source='recipient.username', read_only=True)
    target_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'target_str', 'read', 'timestamp')

    def get_target_str(self, obj):
        return str(obj.target) if obj.target else None
