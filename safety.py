from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import calendar
from datetime import date, datetime
from workalendar.asia import SouthKorea

cal = SouthKorea()
holiday = []
holiday_date=[]

#2020년에 있는 모든 공휴일 가져오기
for i in range(len(cal.holidays(2020))):
	holiday.append(str(cal.holidays(2020)[i][0])[5:])

month = datetime.today().month #현재 달
safety_id = input("하영드리미 아이디 : ")
safety_pw = input("하영드리미 비밀번호 : ")

#현재 달에 공휴일이 있으면 holiday_date에 며칠이 공휴일인지 추가
for j in range(len(holiday)):
	if month == int(holiday[j][:2]):
		holiday_date.append(int(holiday[j][3:]))

#chrome driver
driver=webdriver.Chrome('chromedriver')
driver.get("http://safety.jejunu.ac.kr/")
time.sleep(1)

#safety에 로그인
search = driver.find_element_by_xpath('//*[@id="userId"]')
search.send_keys(safety_id)
time.sleep(1)
search = driver.find_element_by_xpath('//*[@id="userName"]')
search.send_keys(safety_pw)
search.send_keys(Keys.ENTER)

#일상점검 클릭
search = driver.find_element_by_xpath('//*[@id="main_bg_area_wrap"]/div[1]/div[1]/div[2]/ul/li[1]/a')
search.click()

tr = 1 #safety 달력에서 현재 달의 첫번째 행
td = calendar.weekday(2020, month, 1)+2 #safety 달력에서 현재 달의 첫번째 열
date = 1 # 날짜 계산용 변수
try:
	
	while(True):
		#1일부터 날짜 클릭
		search = driver.find_element_by_xpath('//*[@id="dtpicker"]/div/table/tbody/tr[{}]/td[{}]/a'.format(tr, td))
		search.click()
		
		data = driver.find_element_by_class_name("layout_right_940") #클릭된 날짜 점검 여부 크롤링
		if "일상점검을 실시하지 않았습니다" in data.text:
			for k in holiday_date: #date(날짜)가 공휴일이면 N/U설정
				if date == k:
					search = driver.find_element_by_xpath('//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[1]')
					search.click()
					break
				
			if td == 1 or td == 7 : #주말이면 N/U 설정	
				search = driver.find_element_by_xpath('//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[1]')
				search.click()
			
			else: #평일이면 점검
				search = driver.find_element_by_xpath('//*[@id="divList"]/div[3]/table/tbody/tr/td/p/a[2]') #점검 버튼
				search.click()
				search = driver.find_element_by_xpath('//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr[1]/th[2]/input') #일반안전 양호 버튼
				search.click()
				search = driver.find_element_by_xpath('//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr[6]/th[2]/input') #전기안전 양호 버튼
				search.click()
				search = driver.find_element_by_xpath('//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr[11]/th[2]/input') #소방안전 양호 버튼
				search.click()

				#사전유해인자위험분석 보고서 게시 부분은 해당없음
				for i in range(2,6):
					search = driver.find_element_by_xpath('//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr[{}]/td[1]'.format(i))
					if search.text == "사전유해인자위험분석 보고서 게시":
						no_check = driver.find_element_by_xpath('//*[@id="frmOn"]/div[1]/div/div[2]/table/tbody/tr[{}]/td[4]/input'.format(i))
						no_check.click()

				search = driver.find_element_by_xpath('//*[@id="frmOn"]/div[2]/a[1]') #저장버튼
				search.click()

		#다음 날짜로 넘어가기
		td+=1
		date+=1
		if td > 7: #행바꾸기
			tr+=1
			td=1

except:
	time.sleep(1)
	driver.quit()