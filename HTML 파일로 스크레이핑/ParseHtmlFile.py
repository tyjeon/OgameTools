""" 이 파일의 용도

맨날 웹 접속 - 소스 가져오기 - 파싱하는 작업은 시간 소요가 너무 심해서
그냥 한번 소스를 html로 가져오고, 파싱 부분만 따로 컴파일할 순 없을가

하는 아이디어로 시작함. 성공적.


### html 파싱용 파일 받는법
위의 경우, 동적 사이트의 경우 파싱용 파일이 아니라 다른 html 소스를 받는 경우가 있다.
나는 크롬 개발자 도구의 Elements에 있는 html 소스를 원한다.

방법은 이와 같다.
사이트에 접속 - F12로 Elements 탭을 열기 - 소스의 가장 위의 것을 오른쪽 클릭
(예를 들면, <!DOCTYPE html> 바로 아래에 있는 <html>같은 것)
- Edit as HTML 클릭 - 내용 모두 복사한 뒤 메모장에 붙여넣기 후 html로 저장

"""

from bs4 import BeautifulSoup 

def ParseHtmlFile():

        # 소스 가져오고 종료
        with open("ogamehtml.html",encoding="utf-8") as fp:
            bsObject = BeautifulSoup(fp, "html.parser")
            
        result = bsObject.findAll("div",{"id":"view_content"}) # 그냥 예시임.
        for text in result:
            print(text.get_text())

ParseHtmlFile()
