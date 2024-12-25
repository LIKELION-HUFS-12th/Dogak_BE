from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from books.serializers import BookSerializer

# 응답 형식을 통일한 함수
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

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 사용자가 리뷰를 작성할 때, 현재 로그인한 사용자로 설정
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return success_response(response.data, msg="리뷰가 성공적으로 작성되었습니다.", code=status.HTTP_201_CREATED)
        except Exception as e:
            return error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return success_response(response.data, msg="리뷰가 성공적으로 업데이트되었습니다.", code=status.HTTP_200_OK)
        except Exception as e:
            return error_response(str(e), status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return success_response(None, msg="리뷰가 성공적으로 삭제되었습니다.", code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return error_response(str(e), status.HTTP_400_BAD_REQUEST)

class BookSearchView(APIView):
    """
    책을 제목, 저자 등으로 검색할 수 있는 API 뷰
    """

    def get(self, request):
        query = request.query_params.get('q', '')  # 쿼리 파라미터로 검색어 받기
        if not query:
            return error_response("검색어를 입력해주세요.", status.HTTP_400_BAD_REQUEST)

        # 제목, 저자, ISBN 등 여러 필드에서 검색
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        ) | Book.objects.filter(
            isbn__icontains=query
        )

        if not books.exists():
            return error_response("검색 결과가 없습니다.", status.HTTP_404_NOT_FOUND)

        # 검색된 책을 시리얼라이저로 변환 후 응답
        serializer = BookSerializer(books, many=True)
        return success_response(serializer.data, msg="책 검색 성공", code=status.HTTP_200_OK)