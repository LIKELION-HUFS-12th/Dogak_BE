from rest_framework import serializers
from .models import GroupBoard

class GroupBoardSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 작성자 이름 표시

    class Meta:
        model = GroupBoard
        fields = [
            'id', 'user', 'book_title', 'group_name', 'meeting_type',
            'start_date', 'end_date', 'description', 'meeting_days',
            'created_at', 'updated_at',
        ]