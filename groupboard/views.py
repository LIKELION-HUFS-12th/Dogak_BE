from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import GroupBoard
from .serializers import GroupBoardSerializer

# 응답 형식 통일을 위한 함수
def success_response(data, msg="Success", code=status.HTTP_200_OK):
    return Response({
        "code": code,
        "msg": msg,
        "data": data
    })

def error_response(msg, code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "code": code,
        "msg": msg,
        "data": None
    })

class GroupBoardViewSet(viewsets.ModelViewSet):
    queryset = GroupBoard.objects.all().order_by('-created_at')  # 최신 글이 먼저
    serializer_class = GroupBoardSerializer
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def perform_create(self, serializer):
        """
        게시글 작성 시 현재 로그인한 사용자 설정
        """
        group = serializer.save(user=self.request.user)
        return group

    def create(self, request, *args, **kwargs):
        """
        그룹을 생성할 때, 커스텀 응답 형식으로 반환
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            group = self.perform_create(serializer)  # 그룹 생성
            return success_response(
                data=GroupBoardSerializer(group).data,
                msg="그룹이 성공적으로 생성되었습니다.",
                code=status.HTTP_201_CREATED
            )
        else:
            return error_response(
                msg="잘못된 데이터입니다.",
                code=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        그룹 정보를 업데이트할 때, 커스텀 응답 형식으로 반환
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_group = serializer.save()
            return success_response(
                data=GroupBoardSerializer(updated_group).data,
                msg="그룹이 성공적으로 업데이트되었습니다.",
                code=status.HTTP_200_OK
            )
        else:
            return error_response(
                msg="업데이트에 실패했습니다.",
                code=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        """
        그룹을 삭제할 때, 커스텀 응답 형식으로 반환
        """
        group = self.get_object()
        group.delete()
        return success_response(
            data=None,
            msg="그룹이 성공적으로 삭제되었습니다.",
            code=status.HTTP_204_NO_CONTENT
        )

    def list(self, request, *args, **kwargs):
        """
        GET 요청에 대한 응답 형식 통일
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return success_response(
            data=serializer.data,
            msg="모든 그룹을 성공적으로 조회했습니다.",
            code=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        모임에 사용자가 참여할 때, 참여 추가
        """
        group = self.get_object()  # 해당 그룹 찾기

        # 이미 참여한 경우, 커스텀 예외 메시지 처리
        if request.user in group.participants.all():
            return error_response(
                msg="이미 참여한 그룹입니다.",
                code=status.HTTP_400_BAD_REQUEST
            )
        
        group.participants.add(request.user)  # 참여자 추가
        group.save()

        return success_response(
            data=GroupBoardSerializer(group).data,
            msg="참여가 완료되었습니다.",
            code=status.HTTP_200_OK
        )