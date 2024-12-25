from rest_framework import serializers
from .models import GroupBoard
from django.contrib.auth import get_user_model

class GroupBoardSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 작성자 이름 표시
    participants = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all(), many=True, required=False)  # 참여자 목록 추가 (필수 아님)

    class Meta:
        model = GroupBoard
        fields = [
            'id', 'user', 'book_title', 'group_name', 'meeting_type',
            'start_date', 'end_date', 'description', 'meeting_days',
            'created_at', 'updated_at', 'participants'
        ]