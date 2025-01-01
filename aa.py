import pandas as pd

# 엑셀 파일 경로를 정확히 입력하세요
file_path = '/Users/oesikgogi/Downloads/Dogak_BE-bankbook/final 2024-09.xlsx'

try:
    df = pd.read_excel(file_path)
    print("엑셀 파일 읽기 성공")
    print(df.head())
except Exception as e:
    print(f"엑셀 파일 읽기 중 오류 발생: {e}")