import os
from bs4 import BeautifulSoup
from flask import Flask, Blueprint, render_template, jsonify
import requests
from exts import db
from models import JkywModel
import re

bp = Blueprint('jkyw', __name__, url_prefix='/')
# bp = Blueprint('jkyw', __name__, url_prefix='/jkyw')
content_list = []  # 爬取的网页数据，ｊｓｏｎ格式


@bp.route('/')
def jkyw():
    page_number = 2
    url = 'https://www.jxut.edu.cn/xyzx/jkyw/{}.htm'.format(page_number)
    # print(content_list)
    res = requests.get(url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')  # 需要安装lxml库哦
    page_number_a = soup.find_all('span', 'p_no')  # 获取最大的新闻页码
    for pna in page_number_a:
        if pna.a['href'] == '1.htm':
            page_number = pna.a.text
            print('找到了，最大页码：{}'.format(page_number))
            jkyw_pc(int(page_number))
            tag = "总页码数，获取成功"
    return tag


# @bp.route('/jkyw_url')
def jkyw_url(url):
    # url = 'https://www.jxut.edu.cn/info/1129/22908.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
        'Connection': 'close'}
    res = requests.get(url, headers=headers,
                       verify=False, proxies=None, timeout=3)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    form = soup.find_all('form', {'name': '_newscontent_fromname'})
    html = ''
    for i in form:
        h1 = i.find_all('h1')
        info = i.find_all('div', 'info')
        text = i.find_all('div', 'article-text')
        list = h1 + info + text
        image = i.find_all('img')
        for j in image:
            j['src'] = 'https://www.jxut.edu.cn' + j['src']
        for i in list:
            html = i
            # print(html)
    return str(html)


def jkyw_pc(page_number):
    for page in range(page_number, 505, -1):
        url = 'https://www.jxut.edu.cn/xyzx/jkyw/{}.htm'.format(page)
        # url = 'https://www.jxut.edu.cn/xyzx/1.htm'
        url_host = 'https://www.jxut.edu.cn/'
        res = requests.get(url, verify=False)
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
            for d, y, pt, t, pc in zip(day, yea, page_url, title, page_content):  # 获取指定的p标签class 遍历获取内容
                day = d.text
                yea = y.text
                page_url = url_host + pt.get('href')
                title = t['title']
                page_content = pc.text.strip()
                html = jkyw_url(page_url)
                new_dict = {"day": day, "yea": yea, "page_url": page_url, "title": title, "page_content": page_content,
                            "html": html.replace(u'\xa0', u' ')}
                content_list.append(new_dict)
                s = jkyw_json()
    if len(s) > 0:
        content_list.clear()
    return content_list


def jkyw_json():
    path = os.getcwd() + '/' + 'json'
    if len(content_list) > 0:
        with open(path + '/' + 'jkyw.json', 'w', encoding='utf-8') as jkyw_json_file:
            jkyw_json_file.write(str(content_list))
            jkyw_json_file.close()
        file = open(path + '/' + 'jkyw.json', 'r', encoding='utf-8').read()
        jkyw_update(file)
        # print(file)
        return file
    else:
        return {"code": 404, "message": "json文件为空！"}


def jkyw_update(jkyw_page):
    # s = JkywModel(tag="jkyw", jkyw_page=jkyw_page)
    jkyws = JkywModel.query.filter(JkywModel.tag == "jkyw").update({"jkyw_page": jkyw_page})
    # db.session.add(jkyws)
    db.session.commit()
    return jkyws


@bp.route('/jkyw.json')
def jkyw_query():
    jkyws = JkywModel.query.filter(JkywModel.tag == "jkyw")
    for i in jkyws:
        jkyw_page = i.jkyw_page
        # print(i.jkyw_page) #获取数据表jkyw的jkyw_page数据
        return jkyw_page
