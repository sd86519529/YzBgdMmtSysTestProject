from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome()
url ='https://www.xsbiquge.com/68_68007/3500776.html'

# 'https://www.xsbiquge.com/10_10969/9270545.html'  仙界独尊
# 'https://www.xsbiquge.com/84_84291/629429.html'   九星毒奶
# 'https://www.xsbiquge.com/89_89807/1269720.html'  一不小心就无敌啦
# 'https://www.xsbiquge.com/34_34711/2151791.html'
# 'https://www.xsbiquge.com/87_87249/900256.html'  第一序列
driver.get(url)

print(driver.title)

# 获取文本内容
content = driver.find_element_by_id("content").text

print(content)

# 保存内容到指定文件
# for a in content:
#
#     with open('/Users/heshiliang/PycharmProjects/untitled/testfile/test.txt', 'a', encoding='utf-8') as f:
#         # print(a)
#         f.write(a)


# 获取页面所有的链接
# for link in driver.find_elements_by_xpath("//*[@href]"):
#     print (link.get_attribute('href'))

# 获取下一页的链接
# urls = driver.find_elements_by_xpath("html/body/div[1]/div[4]/div/div[2]/div[1]/a[3]")
#
# for url in urls:
#     print(url.get_attribute("href"))


url = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[2]/div[1]/a[3]")

nexturl = url.get_attribute("href")


i = 0

while i <30 :

    driver.get(nexturl)

    print(driver.title)

    content = driver.find_element_by_id("content").text

    # for a in content:
    #     with open('/Users/heshiliang/PycharmProjects/untitled/testfile/test.txt', 'a', encoding='utf-8') as f:
    #         # print(a)
    #         f.write(a)
    print(content)

    url = driver.find_element_by_xpath("/html/body/div[1]/div[4]/div/div[2]/div[1]/a[3]")

    nexturl = url.get_attribute("href")

    i = i+1

print("'%s'"%(url.get_attribute("href")))
# print("'"+url.get_attribute("href")+"'")



driver.quit()