from django.shortcuts import render


from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import BookList
from rest_framework.decorators import api_view

@api_view(['POST'])
def fetch_book(request):
    if request.method == 'POST':
        book_title = request.data.get('title')  # 사용자가 입력한 책 이름 받기

        if book_title:
            # API 요청 URL (예시)
            # api_url = f'http://example.com/api/books?title={book_title}'  # 실제 API URL로 변경하세요
            cert_key="001427d2c2df598d87c3a8e5077728066257ed9a1ba695729508513e03c7b303"
            api_url=f"https://www.nl.go.kr/seoji/SearchApi.do?cert_key={cert_key}&
            result_style=json&
            page_no=1&page_size=10&
            title={book_title}"
            
            print(api_url)
            
            # response = requests.get(api_url)
            # print(response)
            # print("pass")

            try:
                response = requests.post(api_url)
                response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
                print(response)  # 응답 객체 출력
                print("pass")  # 이 메시지가 출력되면 요청이 성공한 것
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")  # 오류 메시지 출력
                return JsonResponse({'error': str(e)}, status=500)

            if response.status_code == 200:
                data = response.json()

                # 데이터 저장 (여기서는 첫 번째 책만 예시로 저장)
                if data:
                    book = data[0]  # 첫 번째 책 정보 가져오기
                    # BookList.objects.create(
                    #     title=book.get('title'),
                    #     author=book.get('author'),
                    #     cheonggu=book.get('cheonggu'),
                    #     publisher=book.get('publisher')
                    #     # print(title)
                    #     # print(author)
                    # )
                    title=book.get('title'),
                    author=book.get('author'),
                    # cheonggu=book.get('cheonggu'),
                    publisher=book.get('publisher')
                    print(title)
                    print(author)
                return JsonResponse({'message': 'Book saved successfully.'})
            else:
                return JsonResponse({'error': 'Failed to fetch data from API.'}, status=response.status_code)
    # return render(request, 'your_template.html')  # GET 요청 시 템플릿 렌더링






