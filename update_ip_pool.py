# -*- coding: utf-8 -*-

import time
from bs4 import BeautifulSoup
import requests
import pickle

def build_header():
    """
    建立一个header列表
    :return: header列表
    """
    header1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/53.0.2785.143 Safari/537.36'}
    header2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/53.0.2785.143 Safari/537.36'}
    header3 = {'Host': 'www.kuaidaili.com',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/49.0.2623.87 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch',
               'Accept-Language': 'zh-CN,zh;q=0.8', }
    header_list = [header1, header2, header3]
    return header_list


def find_IP_proxy_form_xicidaili():
    """
    从西池代理IP网站找到合适的代理IP
    :return: IP列表
    """
    proxy = []
    original_url = 'http://www.xicidaili.com/nn/'
    url_list = []
    for i in range(0, 2):
        url_list.append(original_url+str(i+1))
    for url in url_list:
        time.sleep(5)
        information = requests.get(url=url, headers=build_header()[0], timeout=30).content
        information = information.decode('utf-8')
        print(information)
        ips = BeautifulSoup(information).find_all('tr')
        print(ips)
        for i in range(1, len(ips)):
            tds = ips[i].find_all('td')
            proxy_host = "http://" + tds[1].contents[0] + ":" + tds[2].contents[0]
            proxy_temp = {"http": proxy_host}
            proxy.append(proxy_temp)
    print(proxy)
    return proxy


def find_IP_proxy_from_kuaidaili():
    """
    从快代理IP网站找到合适的代理IP
    :return: IP列表
    """
    proxy = []
    original_url = 'http://www.kuaidaili.com/free/inha/'
    url_list = []
    page_num = 2
    for i in range(0, page_num - 1):
        url_list.append(original_url + str(i+2) + '/')
    for url in url_list:
        time.sleep(5)
        information = requests.get(url=url, headers=build_header()[0], timeout=30).content
        information = information.decode("utf-8")
        ips = BeautifulSoup(information).find('div', id='list').find_all('tr')
        for i in range(0, len(ips)):
            if i == 0:
                continue
            tds = ips[i].find_all('td')
            proxy_host = "http://" + tds[0].text + ":" + tds[1].text
            proxy_temp = {"http": proxy_host}
            proxy.append(proxy_temp)
    print(proxy)
    return proxy


def check_proxy(proxy_list):
    """
    检查找到的IP是否可用
    :param proxy_list: 输入的原始IP
    :return: 可用的IP
    """
    aviliable_proxy = []
    url_for_test = 'https://rate.tmall.com/list_detail_rate.htm?itemId=521406153256&spuId=941158967&sellerId=2587124438&order=3&currentPage=1'
    header_for_test = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    for proxy in proxy_list:
        try:
            requests.get(url=url_for_test, headers=header_for_test, proxies=proxy, timeout=30)
            aviliable_proxy.append(proxy)
        except:
            continue
    print('找到的可以使用的代理IP：', len(aviliable_proxy))
    print(aviliable_proxy)
    return aviliable_proxy


def save_data(list1, list2):
    """
    保存可用的header和IP
    :param list1: header列表
    :param list2: IP列表
    :return: .p文件
    """
    with open('aviliable_IP.p', 'wb') as out_file:
        pickle.dump((list1, list2), out_file)


if __name__ == '__main__':
    header_list = build_header()
    proxy_list = []
    proxy_list.extend(find_IP_proxy_form_xicidaili())
    proxy_list.extend(find_IP_proxy_from_kuaidaili())
    print(proxy_list)
    useful_proxy = []
    useful_proxy.extend(check_proxy(proxy_list=proxy_list))
    print('header:', len(header_list), 'proxy:', len(useful_proxy))
    save_data(header_list, useful_proxy)