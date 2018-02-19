#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import BeautifulSoup, urlparse, os, time, random

def getPeopleLinks(page):
	links = []
	for link in page.findAll('a'):
		url = link.get('href')
		if url:
			if '/profile.php?id=' in url:
				links.append(url)
	return links

def getID(url):
	pUrl = urlparse.urlparse(url)
	return urlparse.parse_qs(pUrl.query)['id'][0]

def view_friend():
	print "[+] 친구목록 탐색중"
	private_page = driver.find_element_by_class_name('fbxWelcomeBoxSmallRow')
	ActionChains(driver).move_to_element(private_page).click().perform()
	friend_page = driver.find_element_by_class_name('_39g5')
	ActionChains(driver).move_to_element(friend_page).click().perform()

def login_web():
	facebook_id = driver.find_element_by_name("email")
	facebook_pw = driver.find_element_by_name("pass")

	facebook_id.clear()
	facebook_pw.clear()
	
	facebook_id.send_keys("") #input ID
	facebook_pw.send_keys("") #input PW
	facebook_pw.send_keys(Keys.RETURN)
	print "[+] 로그인 성공! 봇을 시작합니다."
	
def write_timeline():
	facebook_write = driver.find_element_by_name("xhpc_message")
	facebook_write.clear()
	facebook_write.send_keys("`1234567890~!@#$%^&*()_+|")
	if facebook_write.send_keys(Keys.RETURN) == None:
		print "[+] 글 작성 완료!"

def viewbot(driver):
	visited = {}
	pList = []
	count = 0
#	while True:
	for i in range(10):
		#sleep to make sure everything loads.
		#add random to make us look human.
#	time.sleep(random.uniform(3.5,6.9))
		page = BeautifulSoup.BeautifulSoup(driver.page_source)
		people = getPeopleLinks(page)
		if people:
			for person in people:
				ID = getID(person)
				if ID not in visited:
					pList.append(person)
					visited[ID] = 1
		if pList: #If there is people to look at, then look at them
			person = pList.pop()
			driver.get(person)
			count += 1

		print "[+]"+driver.title[3:len(driver.title)]+" Visited! \n("\
			+str(count)+"/"+str(len(pList))+") Visited/Queue"
		driver.back()

def Main():
	os.system('clear')
	print """
	=====================**************************======================
	=====================Facebook Friends Search Bot======================
	=====================**************************======================
	"""
	web = 'https://facebook.com/login.php'	
	global driver
	driver = webdriver.Firefox()
	driver.get(web)
	print "[+] 웹 사이트 접근 성공(" + web + ")"
	assert "Facebook" in driver.title
	
	login_web()
	driver.implicitly_wait(10)

	view_friend()
	viewbot(driver)

	assert "No results found." not in driver.page_source

	print "[+] 자동탐색기 종료"
	driver.close()

if __name__ == "__main__":
	Main()
