# -*- coding: utf-8 -*-

import random
import pickle
import requests
import time
import re
import pandas
import copy
import threadpool


def random_each_header_IP():
    """
    随机取出header和IP
    :param header_list:header列表
    :param proxy_list: IP列表
    :return: 可用的header和IP
    """
    with open('./aviliable_IP.p', 'rb') as f:
        data = pickle.load(f)
    # print(data[0][0])
    # print(data[1][0])
    # print(len(data[0]))
    # print(type(data))
    header = data[0][random.randint(0, len(data[0])-1)]
    proxy = data[1][random.randint(0, len(data[1])-1)]
    print('当前使用的header是：', header)
    print('当前使用的IP地址是：', proxy)
    return header, proxy


def page_analysis(url_list):
    totaltable = []
    # 循环抓取数据
    page_count = 1
    header_proxy_use_count = 1
    header, proxy = random_each_header_IP()
    for url in url_list:
        onepage_try = 0
        while True:
            header_proxy_use_count += 1
            if header_proxy_use_count >= 4:
                header, proxy = random_each_header_IP()
                header_proxy_use_count = 0
            try:
                content = requests.get(url, headers=header, proxies=proxy).text
            except:
                onepage_try += 1
                if onepage_try >= 50:
                    print("访问页面失败")
                    break
                header, proxy = random_each_header_IP()
                header_proxy_use_count = 0
            time.sleep(2)
            # 借助正则表达式使用findall进行匹配查询
            try:
                myjson = re.findall('.*rateList":(\[.*\]),".*info":"","tags"', content)[0]
                print(page_count)
                print(proxy)
                break
            except:
                onepage_try += 1
                if onepage_try >= 50:
                    print("解析页面错误")
                    break
                header, proxy = random_each_header_IP()
                header_proxy_use_count = 0

        singletable = pandas.read_json(myjson)
        if page_count == 1:
            totaltable = copy.deepcopy(singletable)
        else:
            totaltable = pandas.concat([totaltable, singletable], ignore_index=True)
        page_count += 1
    print(totaltable)
    return totaltable


def get_max_page(url):
    first_url = url + '1'
    count = 0
    while(1):
        try:
            header, proxy = random_each_header_IP()
            # print(header, proxy)
            info = requests.get(first_url, headers=header, proxies=proxy).text
            # print(info)
            a = info.find('lastPage')
            # print(type(info))
            page = int(info[a+10:a+12])
            # print(page)
            print('最大页数', page)
            break
        except:
            count+=1
            # header, proxy = get_header_and_proxy(header_list=build_header(), proxy_list=find_IP_proxy_form_xicidaili())
            print("未找到最大页，尝试次数：", count)
    return page


def get_url(sellerid, itemid):
    url1 = 'https://rate.tmall.com/list_detail_rate.htm?itemId='
    url2 = '&spuId=607872203&sellerId='
    url3 = '&order=3&currentPage='
    url = url1 + str(itemid) + url2 + str(sellerid) + url3
    return url


def save_name(sellerid, itemid):
    ss = 'TMall'+str(sellerid)+str(itemid)
    sp = 'D:\Pycharm\PycharmProjects\Class\\2018_8_2\\'
    save_path = sp + ss + '.csv'
    return save_path


def get_comment(url, name,  page):
    url_list = []
    for i in list(range(1, page+1)):
        url_list.append(url+str(i))
    totaltable = page_analysis(url_list)
    totaltable.to_csv(name, encoding='gb18030')


def one_job(sellerid, itemid):
    print('开始了：')
    # pj_list.append(([data['sellerid'][i], data['itemid'][i]], None))

    # data = pandas.read_csv('./tmall_product_for_spyder/tmall_prduct_id.csv', encoding='utf-8')
    # for i in range(len(data)):
    #     url = get_url(data['sellerid'][i], data['itemid'][i])
    url_ = get_url(sellerid, itemid)
    print(url_)
    page = get_max_page(url_)
    get_comment(url_, save_name(sellerid, itemid), page=page)


def main():
    data = pandas.read_csv('./tmall_prduct_id.csv', encoding='utf-8')
    print(data)
    pj_list = []
    for i in range(len(data)):
        pj_list.append(([data['sellerid'][i], data['itemid'][i]], None))
    print(pj_list)
    # device_list=[object1,object2,object3......,objectn]#需要处理的设备个数
    pool = threadpool.ThreadPool(8)  # 8是线程池中线程的个数
    # 首先构造任务列表
    requests = threadpool.makeRequests(one_job, pj_list)

    [pool.putRequest(req) for req in requests]
    pool.wait()


if __name__ == '__main__':
    main()
    