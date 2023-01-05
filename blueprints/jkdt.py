import os
from bs4 import BeautifulSoup
from flask import Flask, Blueprint, render_template, jsonify
import requests
import json

bp = Blueprint('jkyw', __name__, url_prefix='/jkyw')
content_list = []  # 爬取的网页数据，ｊｓｏｎ格式


@bp.route('/')
def jkyw():
    page_number = 2
    url = 'https://www.jxut.edu.cn/xyzx/jkyw/{}.htm'.format(page_number)
    print(content_list)
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')  # 需要安装lxml库哦
    page_number_a = soup.find_all('span', 'p_no')  # 获取最大的新闻页码
    for pna in page_number_a:
        if pna.a['href'] == '1.htm':
            page_number = pna.a.text
            print('找到了，最大页码：{}'.format(page_number))
            jkyw_pc(int(page_number))
        else:
            print('请检查href路径和主url')
    return content_list


def jkyw_pc(page_number):
    for page in range(page_number, 505, -1):
        url = 'https://www.jxut.edu.cn/xyzx/jkyw/{}.htm'.format(page)
        # url = 'https://www.jxut.edu.cn/xyzx/1.htm'
        url_host = 'https://www.jxut.edu.cn/'
        res = requests.get(url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')  # 需要安装lxml库哦
        result_list = soup.find_all('ul', {'class': 'list-text'})
        for i in result_list:
            # print(i.find_all('p')) # 获取ul标签下的所有p标签
            day = i.find_all('p', 'day')
            yea = i.find_all('p', 'yea')
            page_url = i.find_all('a')
            title = i.find_all('a')
            page_content = i.find_all('div', 'abst')
            for i, j, pt, t, pc in zip(day, yea, page_url, title, page_content):  # 获取指定的p标签class 遍历获取内容
                day = i.text
                yea = j.text
                page_url = url_host + pt.get('href')
                title = t['title']
                page_content = pc.text.strip()
                new_dict = {"day": day, "yea": yea, "page_url": page_url, "title": title, "page_content": page_content}
                content_list.append(new_dict)
                jkyw_json()
    print(content_list)


@bp.route('/jkyw.json')
def jkyw_json():
    path = os.getcwd() + '/' + 'json'
    if len(content_list) > 0:
        with open(path + '/' + 'jkyw.json', 'w', encoding='utf-8') as jkyw_json_file:
            jkyw_json_file.write(str(content_list))
            jkyw_json_file.close()
        file = open(path + '/' + 'jkyw.json', 'r', encoding='utf-8')
        return file
    else:
        return {"code": 404, "message": "json文件为空！"}
