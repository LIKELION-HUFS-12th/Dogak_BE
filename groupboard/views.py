from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import GroupBoard
from .serializers import GroupBoardSerializer

class GroupBoardViewSet(viewsets.ModelViewSet):
    queryset = GroupBoard.objects.all().order_by('-created_at')  # 최신 글이 먼저
    serializer_class = GroupBoardSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def perform_create(self, serializer):
        # 게시글 작성 시 현재 로그인한 사용자 설정
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        group = self.get_object()  # 해당 그룹 찾기
        if request.user in group.participants.all():
            return Response({"detail": "이미 참여한 그룹입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        group.participants.add(request.user)  # 참여자 추가
        group.save()

        return Response(GroupBoardSerializer(group).data, status=status.HTTP_200_OK)