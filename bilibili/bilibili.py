#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import json
import os
import re
import time
from collections import Counter

import requests
from prettytable import PrettyTable
from tqdm import tqdm

from bilibili.sendemail import EmailSend


def _get_cookies_file(filename):
    '''get cookies

    :param filename: cookies file path
    :return: cookies
    '''
    if "COOKIES" in os.environ:
        return os.getenv('COOKIES')
    else:
        with open(filename, 'r') as f:
            cookies = f.read()
            return cookies


def get_header(referer, filename):
    '''get header

    :param referer: referer
    :param filename: cookies file path
    :return:
    '''
    cookie = _get_cookies_file(filename)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'api.bilibili.com',
        # 'Referer': 'https://www.bilibili.com/account/history',
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    return headers


def req_get(headers, url):
    '''GET method

    :param headers: header
    :param url:  url
    :return: json result
    '''
    resp = requests.get(url, headers=headers)
    return json.loads(resp.text)


def req_get_stat(headers, url):
    '''

    :param headers: header
    :param url: url
    :return: result
    '''
    resp = requests.get(url, headers=headers)
    result = json.loads(re.findall('\((.*?)\)', resp.text)[0])
    return result['data']


def get_bilibili_history(cookie_file):
    '''get history

    :param cookie_file: cookies file path
    :return: history data list
    '''
    referer = 'https://www.bilibili.com/account/history'
    headers = get_header(referer=referer, filename=cookie_file)
    # 这里只取300条记录，如想多取，设置 pn：页码 和 ps：每页多少条记录即可（每页最多300条）
    url = 'https://api.bilibili.com/x/v2/history?pn={pn}&ps={ps}&jsonp=jsonp'.format(pn=1, ps=300)
    result = req_get(headers, url)
    return result['data']


def get_stat(aid, cookie_file):
    '''get stat of like/coins/favoured

    :param aid: aid
    :param cookie_file: cookies file path
    :return: (bool) stat of baipiao
    '''
    referer = 'https://www.bilibili.com/video/{aid}'.format(aid=aid)
    headers = get_header(referer=referer, filename=cookie_file)
    time_stamp = int(round(time.time() * 1000))
    like_url = 'https://api.bilibili.com/x/web-interface/archive/has/like?jsonp=jsonp&aid={aid}&callback=__jp0'.format(
        aid=aid)
    like_result = req_get_stat(headers, like_url)
    if like_result == 1:
        return True
    coins_url = 'https://api.bilibili.com/x/web-interface/archive/coins?' \
                'callback=jqueryCallback_bili_5397496216695663&jsonp=jsonp' \
                '&aid={aid}&_={timeStamp}'.format(aid=aid, timeStamp=time_stamp)
    coins_result = req_get_stat(headers, coins_url)
    if coins_result['multiply'] != 0:
        return True
    favoured_url = 'https://api.bilibili.com/x/v2/fav/video/favoured?' \
                   'callback=jqueryCallback_bili_8465204478676807&jsonp=jsonp&' \
                   'aid={aid}&_={timeStamp}'.format(aid=aid, timeStamp=time_stamp)
    favoured_result = req_get_stat(headers, favoured_url)
    if favoured_result['favoured']:
        return True

    return False


def get_analysis(cookie_file):
    '''get analysis

    :param cookie_file: cookies file path
    :return:
    '''
    baipiao_num = 0
    ups = []
    ups_detail = {}
    history = get_bilibili_history(cookie_file)
    for item in tqdm(history, desc="进度", ascii=True):
        progress = item['progress']  # 观看进度，单位：秒
        if progress != -1 and progress < 60:
            continue
        aid = item['aid']  # av 号
        owner = item['owner']['name']  # up 主
        stat = get_stat(aid, cookie_file)
        if not stat:
            baipiao_num += 1
            ups.append(owner)
            ups_detail[owner] = item['owner']

    top3 = Counter(ups).most_common(3)
    print_table(top3)
    print("总白嫖数：{num}".format(num=baipiao_num))
    handel_ups(top3, ups_detail, baipiao_num)


def print_table(top3):
    '''print table of top3

    :param tops:
    :return:
    '''
    table = PrettyTable(['up主', '白嫖数'])
    for n in top3:
        table.add_row([n[0], n[1]])
    table.header_style = 'title'
    table.sort_key("白嫖数")
    table.padding_width = 7
    table.reversesort = True
    print("白嫖排行版")
    print(table)


def handel_ups(top3, ups_detail, total):
    img_list = ["img/book.png"]
    table_tr = ''
    for i, item in enumerate(top3):
        mid = ups_detail[item[0]]['mid']
        face = ups_detail[item[0]]['face']
        space_url = 'https://space.bilibili.com/{mid}'.format(mid=mid)
        r = requests.get(face)
        img_name = "{mid}.jpg".format(mid=mid)
        with open(img_name, "wb") as code:
            code.write(r.content)
        img_list.append(img_name)
        tr = """
          <tr>
            <td>{rank}</td>
            <td><img src="cid:image{count}" class="round_icon"  alt="">&nbsp;&nbsp;<a href="{url}">{name}</a></td>
            <td>{num}</td>
          </tr>
        """.format(rank=i + 1, url=space_url, name=item[0], num=item[1], count=i + 1)
        table_tr += tr

    email = EmailSend()
    email.title = '白嫖周报'
    email.html = """
                <html>
                  <head>
                      <style>
                        body {{
                          background-image:url("cid:image{{0}}");
                          background-repeat:no-repeat;
                        }}
                        .round_icon{{
                          width: 34px;
                          height: 34px;
                          display: flex;
                          border-radius: 50%;
                          align-items: center;
                          justify-content: center;
                          overflow: hidden;
                          float:left;
                        }}
                        table.dataintable {{
                           border: 1px solid #888888;
                           border-collapse: collapse;
                           font-family: Arial,Helvetica,sans-serif;
                           margin-top: 10px;
                           width: 100%;
                        }}
                        table.dataintable th {{
                           background-color: #CCCCCC;
                           border: 1px solid #888888;
                           padding: 5px 15px 5px 5px;
                           text-align: left;
                           vertical-align: baseline;
                        }}
                        table.dataintable td {{
                           background-color: #EFEFEF;
                           border: 1px solid #AAAAAA;
                           padding: 5px 15px 5px 5px;
                           vertical-align: middle;
                           line-height: 30px
                        }}
                      </style>
                  </head>
                  <body>
                    <h2>白嫖一时爽，一直白嫖一直爽</h2>
                    <h3>总白嫖数：{total}最近白嫖最多up主 TOP3</h3>
                    <table class="dataintable">
                      <tr>
                        <th>排名</th>
                        <th>up主</th>
                        <th>白嫖数</th>
                      </tr>
                      {table_tr}
                    </table>
                  </body>
                </html>
                """.format(table_tr=table_tr, total=total)
    email.send_email(img_list)
    print('send email finish!')
