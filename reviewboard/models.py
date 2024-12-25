from django.db import models
from django.conf import settings
from books.models import Book  # 기존 책 모델

class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        null=True,  # 검색된 책이 없을 경우 null 허용
        blank=True,
        related_name="reviews"
    )
    custom_book_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="DB에 책이 없을 경우 사용자가 직접 입력한 책 제목"
    )
    custom_book_author = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="DB에 책이 없을 경우 사용자가 직접 입력한 저자"
    )
    review_title = models.CharField(max_length=255)  # 리뷰 제목
    review_content = models.TextField()  # 리뷰 내용
    rating = models.PositiveSmallIntegerField()  # 별점 (1~5)

    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간

    def __str__(self):
        if self.book:
            return f"{self.book.title} - {self.review_title}"
        return f"{self.custom_book_title} - {self.review_title}"