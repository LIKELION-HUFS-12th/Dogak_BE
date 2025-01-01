from django.db import models
from django.conf import settings
###

class GroupBoard(models.Model):
    BOOK_CHOICES = [
        ('Online', '온라인'),
        ('Offline', '오프라인'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 커스텀 사용자 모델 참조
        on_delete=models.CASCADE,
        related_name="group_boards"
    )
    book_title = models.CharField(max_length=255)  # 도서명
    group_name = models.CharField(max_length=255)  # 모임명
    meeting_type = models.CharField(max_length=20, choices=BOOK_CHOICES, default='Online')  # 모임 방식
    start_date = models.DateField()  # 모임 시작일
    end_date = models.DateField()  # 모임 종료일
    description = models.TextField()  # 모임 설명
    meeting_days = models.CharField(max_length=255)  # 모임 요일 (예: "월,수,금")

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="participated_groups",
        blank=True
    )  # 참여자가 없음으로도 모임을 만들 수 있도록 설정

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    def __str__(self):
        return f"{self.group_name} ({self.book_title})"