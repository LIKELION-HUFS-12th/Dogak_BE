import pandas as pd
from books.models import Book

def run():
    # 엑셀 파일 경로
    file_path = ''

    try:
        # 엑셀 데이터 읽기
        df = pd.read_excel(file_path)
        print("엑셀 파일 읽기 성공")

        # 컬럼 이름 매핑
        df = df.rename(columns={
            '도서명': 'title',
            '저자': 'author',
            '출판사': 'publisher',
            '발행년도': 'publish_year',
            'ISBN': 'isbn',
            '주제분류번호': 'classification_number',
            '주제분류': 'classification'
        })

        # 데이터 삽입
        for _, row in df.iterrows():
            print(f"Inserting: {row['title']} by {row['author']}")
            Book.objects.create(
                title=row['title'],
                author=row['author'],
                publisher=row['publisher'],
                publish_year=row['publish_year'],
                isbn=row['isbn'],
                classification_number=row['classification_number'],
                classification=row['classification']
            )
        print("모든 데이터를 데이터베이스에 삽입했습니다!")
    except Exception as e:
        print(f"오류 발생: {e}")