import requests
from bs4 import BeautifulSoup
import time

response =requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%EC%86%90%ED%9D%A5%EB%AF%BC&oquery=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&tqi=h9iWRdp0Jywss77HRL8ssssstms-156932')
html = response.text
soup = BeautifulSoup(html, 'html.parser')

articles = soup.select('div.info_group')

for article in articles:
    links = article.select('a.info')
    if len(links) >= 2:
        url = links[1].attrs['href']#링크가 2개이상이면 두 번째 링크의 href를 추출
        response = requests.get(url, headers = {'User-agent':'Mozila/5.0'})
        html = response.text
        soup= BeautifulSoup(html,'html.parser')

        #만약 연예뉴스라면
        if 'entertain' in response.url:
            title = soup.select_one('.end_tit') #기사 제목
            content = soup.select_one('#articeBody')
        elif 'sports' in response.url:
            title = soup.select_one('h4.title') #기사 제목 그냥 .title을 하면 50개가 나오므로 제목만 나오게 h4로 한정시켜줌
            content = soup.select_one('#newsEndContents')
            #본문 내용 안에 불필요한 div, p 삭제하기
            divs = content.select('div')
            for d in divs:
                d.decompose() #d태그 삭제

            ps = content.select('p')
            for p in ps:
                p.decompose() #p태그 삭제
    
        else:
            title = soup.select_one('.media_end_head_top')
            content = soup.select_one("#newsct_article") #뉴스 본문의 id값
        print("====링크====\n", url)
        print("====제목====\n", title.text) #텍스트만 가져오기
        print("====본문====\n", content.text)
        time.sleep(0.3)