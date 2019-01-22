import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

name = ['楼盘名', '链接', '地址', '楼盘状态', '楼盘类型', '均价', '居室类型', '面积']


def getonepage(url, lists):
    response = requests.get(url)
    print(type(response.text))
    soup = bs(response.text, 'html.parser')
    houselist = soup.find_all('li', class_='item')
    print(houselist)
    for house in houselist:
        list = []
        list.append(house.find('h2').text)
        list.append(house.find('h2').find('a')['href'])
        list.append(house.find('div', class_='address').find('span').text)
        list.append(house.find('div', class_='label').find_all('span')[0].text)
        list.append(house.find('div', class_='label').find_all('span')[1].text)
        list.append(house.find('div', class_='price').find('span').text)

        if house.find('div', class_='info').find('span', class_='tag') == None:
            list.append('null')
        elif house.find('div', class_='info').find('span', class_='tag').text == '':
            list.append('null')
        else:
            list.append(house.find('div', class_='info').find('span', class_='tag').text)

        if house.find('div', class_='info').find('span', class_='area') == None:
            list.append('null')
        elif house.find('div', class_='info').find('span', class_='area').text == '':
            list.append('null')
        else:
            list.append(house.find('div', class_='info').find('span', class_='area').text)
        lists.append(list)
    return lists


def getallinfo():
    list_all = []
    list_one = []
    for i in range(1, 13):
        url_new = "http://gl.loupan.com/xinfang/t1-p" + str(i) + "/"
        print(url_new)
        list_all = list_all + getonepage(url_new, list_one)
    H = pd.DataFrame(columns=name, data=list_all)
    H.to_csv('F:/HouseInfo.csv', encoding='gb18030')
    print(list_all)


def run():
    getallinfo()


if __name__ == '__main__':
    run()
