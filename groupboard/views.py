from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import GroupBoard
from .serializers import GroupBoardSerializer

class GroupBoardViewSet(viewsets.ModelViewSet):
    queryset = GroupBoard.objects.all().order_by('-created_at')  # 최신 글이 먼저
    serializer_class = GroupBoardSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def perform_create(self, serializer):
        # 게시글 작성 시 현재 로그인한 사용자 설정
        serializer.save(user=self.request.user)