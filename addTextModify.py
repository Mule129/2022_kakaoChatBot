import datetime as dt
import random
import re
import requests
import calendar as c
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFont, ImageDraw

def color_list(t):
    """
    color list

    :param t: 1-흰색 2-검정색 3-회색 4~15-연한무지개 16~27-진한무지개
    :return: color str(list)
    """
    color = ["#FFFFFF", "#000000", "#555555",
             "#FFD8D8", "#FAE0D4", "#FAECC5", "#FAF4C0", "#E4F7BA", "#CEFBC9",
             "#D4F4FA", "#D9E5FF", "#DAD9FF", "#E8D9FF", "#FFD9FA", "#FFD9EC",
             "#FFA7A7", "#FFC19E", "#FFE08C", "#FAED7D", "#CEF279", "#B7F0B1",
             "#B2EBF4", "#B2CCFF", "#B5B2FF", "#D1B2FF", "#FFB2F5", "#FFB2D9"]
    return color[t]
#print(color_list.__doc__)

def random_color()->int:
    """
    random color create

    :return: random color str(list)
    """
    t = random.randint(3,26)
    number = color_list(t)
    return number

def SAT_dday():
    """
    수능(korean SAT) dday 출력 함수

    :return:합산 날짜 출력
    """
    dday = dt.date(year=2022, month=11, day=17)
    today = dt.date.today()

    dday = dday - today
    dday = "D - " + str(dday).split()[0] + " day"

    return dday

def s_dday(o : int):
    """
    내신 시험(scholl exam) dday 출력 함수

    파라미터 o 제거 -> 가장 인접한 시험 출력

    :param o: 시험 종류 
    :return: 남은 날짜(dday)
    """
    day_list = ["2022-4-25","2022-6-27"]#스크래핑 하기
    d_year, d_month, d_day = day_list[o].split("-")
    dday = dt.date(year=int(d_year),month=int(d_month),day=int(d_day))
    today = dt.date.today()

    dday = dday - today
    dday = "D - " + str(dday).split()[0] + " day"

    return dday

def exam_day(t : int, o : int) ->int:
    """
    수능, 내신 dday 출력

    :param t: 시험 종류(0 = 내신, 1 = 수능
    :param o: 몇번째 시험인지 ..
    :return: date type로 출력
    """
    if t == 1:
        dday = SAT_dday()
    elif t == 0:
        dday = s_dday(o)

    return dday


def new_image(xy_size : tuple, color : int):
    """
    새 랜덤 배경색을 가진 이미지 생성

    xy_size = 크기(튜플형), color = 배경색
    """
    new_image = Image.new("RGB", xy_size, random_color())

    return new_image

def week_day(number):
    """
    번호:날짜(dictionary type)

    :param number:날짜에 해당하는 숫자
    :return: str 형식 날짜

    """
    data = {0: '월요일', 1:'화요일', 2:'수요일', 3:'목요일', 4:'금요일', 5:'토요일', 6:'일요일'}

    return data[number]

def lunch(to_month : str)->str:
    r"""
    1. 날짜 파라미터(매개변수)를 입력받으면 bs4와 requests 모듈을 이용하여 급식조회사이트에서 그 달의 급식정보 표 조회
    2. 가져온 급식정보 표에서 re모듈-줄바꿈(\n) 횟수를 공백으로 치환, 이를 이용하여 날짜별 데이터 분리 -> eat_list list에 저장
    3. datetime.date.today 함수를 이용하여 오늘의 날짜 탐색
    4. for문과 find 함수를 이용하여 eat_list 내에 오늘의 날짜와 일치하는 급식 데이터 검출

    수정예정 - to_month 파라미터 제거, today 함수를 이용하여 자체적으로 오늘의 날짜 탐색

    :param to_month: 오늘의 날짜(ex:2001년02월02일 -> 200102 #월까지만 입력)
    :return: 오늘의 급식정보
    """
    month = to_month +".html"
    url = "https://school.koreacharts.com/school/meals/B000012894/"+month

    res = requests.get(url)

    try: #res.status_code == 200
        html = res.text
        soup = bs(html, "html.parser")
        lyrics = soup.select_one("body > div > div > div > section.content > div:nth-child(6) > div > div > div.box-body")
        try:
            eat_text = lyrics.get_text()
        except:
            print("사이트 정보를 읽어들이지 못했습니다")
        eat_text = re.sub("&nbsp; | &nbsp;|\t|\r","",eat_text)
        #eat_text = re.sub("\n\n\n\n\n","\n\n\n\n\n",eat_text)
        eat_text = re.sub("\n\n\n", "\n", eat_text)
        eat_text = re.sub("\n\n", "\n", eat_text)
    except:
        print("사이트를 불러오는데 실패했습니다")

    eat_list = eat_text.split("\n\n")
    today = str(int(str(dt.date.today()).split("-")[2]))
    week = dt.date.today().weekday()
    week = week_day(week)

    x = 0

    find_t = str(today+"\n"+ week)

    print(today, week, find_t)

    for i in eat_list:
        if i.find(find_t) != -1:
            print("찾음")
            return eat_list[x]
        else:
            x = x + 1
        print(x)
    print("today",today,eat_list)
    return eat_list[int(today)]

print(lunch.__doc__)# r""" doc test

def lunch_slice():
    """
    데이터 전처리(당일 급식 데이터 뒤에 붙은 성분표시 제거, 날짜 삭제)
    
    :return: 전처리 완료된 급식데이터
    """
    name = lunch(str(today)).split('\n')
    data_list = []

    for i in range(len(name)):#name 리스트 길이만큼 for문 실행
        data_pros = re.sub(r'[0-9]+', '', name[i])#problem : 날짜 또한 제거되어버림.
        if i != 0:
            data_list.append(data_pros.replace('.','') + str('\n'))
    print("a result : ", data_list)

    result = ''.join(s for s in data_list)#

    return(result)

def day_()->list:
    """
    today 함수의 dt 타입을 str 형식으로 변환
    
    :return: list   ex) [2022,02,02]
    """
    to_day = dt.date.today()
    to_day = str(to_day).split("-")
    return to_day

def calen_day():

    calen_d = c.month(dt.date.today().year, dt.date.today().month)

    return(calen_d)

#fnt = ImageFont.load("BMJUA_ttf.ttf")#<-비트맵(픽셀)형식 글꼴 파일 오픈
image = new_image((1000, 1000), color_list(random.randint(3,26)))

fntSet = ImageFont.truetype("BMJUA_ttf.ttf", size=80)

draw = ImageDraw.Draw(image)
font_x, font_y = image.size
font_x = float(font_x) / 2
font_y = float(font_y) / 2
font_pos = font_x, font_y

#today
today = str(dt.date.today()).split("-")
today = today[0]+today[1]

#수능dday
draw.text((120, 70), str("수능 :"), color_list(0),
          font=ImageFont.truetype("BMJUA_ttf.ttf", size=80),
          anchor="mm", align=10, stroke_width=5, stroke_fill=color_list(2))
draw.text((460, 70), str(SAT_dday()), color_list(0),
          fntSet, anchor="mm", align=10, stroke_width=10, stroke_fill=color_list(2))
draw.text((880, 135), str("화이팅"), color_list(0),
          font=ImageFont.truetype("BMJUA_ttf.ttf", size=60),
          anchor="mm", align=10, stroke_width=5, stroke_fill=color_list(2))

#내신dday
draw.text((170, 195), str("1회고사 :"), color_list(0),
          font=ImageFont.truetype("BMJUA_ttf.ttf", size=80),
          anchor="mm", align=10, stroke_width=5, stroke_fill=color_list(2))
draw.text((520, 195), str(exam_day(0,0)), color_list(0),
          fntSet, anchor="mm", align=10, stroke_width=10, stroke_fill=color_list(2))

#오늘 날짜
draw.text((880,50), str(dt.date.today()), color_list(0),
          font=ImageFont.truetype("BMJUA_ttf.ttf", size=30),
          anchor="mm", align=10, stroke_width=5, stroke_fill=color_list(2))

#급식정보
draw.multiline_text((40,300), "오늘의 급식\n"+str(lunch(str(today))),
                    font=ImageFont.truetype("BMJUA_ttf.ttf", size=35),
                    spacing=1 , stroke_width=3, stroke_fill=color_list(2))

#달력
draw.text((650,300), str(calen_day()),
                    font=ImageFont.truetype("BMJUA_ttf.ttf", size=35),
                    spacing=1 , stroke_width=3, stroke_fill=color_list(2))

#공란
image.show()
image.save("test_image.png", format="png")
