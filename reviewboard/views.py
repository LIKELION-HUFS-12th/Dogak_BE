from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
from books.models import Book
from books.serializers import BookSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 사용자가 리뷰를 작성할 때, 현재 로그인한 사용자로 설정
        serializer.save(user=self.request.user)

class BookSearchView(APIView):
    """
    책을 제목, 저자 등으로 검색할 수 있는 API 뷰
    """

    def get(self, request):
        query = request.query_params.get('q', '')  # 쿼리 파라미터로 검색어 받기
        if not query:
            return Response({"message": "검색어를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 제목, 저자, ISBN 등 여러 필드에서 검색
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        ) | Book.objects.filter(
            isbn__icontains=query
        )

        if not books.exists():
            return Response({"message": "검색 결과가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 검색된 책을 시리얼라이저로 변환 후 응답
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)