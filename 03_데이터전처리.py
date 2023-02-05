from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from bs4 import BeautifulSoup
import time
import pyautogui
import openpyxl


def text_to_num(text):
    text = text.replace('조회수', '').strip()

    if '만' in text:
        num = (text.replace('만회','0000'))

    elif '천' in text:
        num = (text.replace('천회','000'))

    elif '억' in text:
        num = (text.replace('억회','00000000'))

    elif '조회수 없음' == text:
        num = 0
    else:
        num= int(text)
    return num


#검색어 입력하기
search = pyautogui.prompt('검색어를 입력하세요')

#엑셀 생성
wb = openpyxl.Workbook()
ws = wb.create_sheet(search)
ws.append(['번호','제목', '조회수', '날짜'])


url = f'https://www.youtube.com/results?search_query={search}'
browser = webdriver.Chrome('C:/chromedriver.exe')
browser.implicitly_wait(10)
browser.maximize_window()
browser.get(url)

#7번 스크롤하기
scroll_count = 3

i = 1
while True:
    # 맨 아래로 스크롤 내리기
    browser.find_element_by_css_selector('body').send_keys(Keys.END)

    #스크롤 사이 시간
    time.sleep(2)

    if i == scroll_count:
        break
    i += 1

#selenium 연동 방법
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
infos = soup.select('div.text-wrapper')

for j, info in enumerate(infos, 1):
    #title 가져오기
    title = info.select_one('a#video-title').text

    try:
        #조회수 가져오기
        views = info.select('div#metadata-line > span.inline-metadata-item')
        view = views[0].text

        #날짜 가져오기
        date = views[1].text

    except:
        view = '조회수 없음'
        date = '날짜 없음'

    
    view = text_to_num(view)


    print(title, view, date)
    ws.append([j, title, view, date])

wb.save(f'Chapter09/{search}.xlsx')

