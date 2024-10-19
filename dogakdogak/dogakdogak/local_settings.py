from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = True

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'), # DB(스키마) 이름
        'USER': config('DB_USER'), # 유저 이름 (root)
        'PASSWORD': config('DB_PASSWORD'), # DB 비밀번호
        'HOST': config('DB_HOST'), # DB 엔드포인트
        'PORT': 3306,
    }
}