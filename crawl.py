#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime
import time
import pickle
from selenium import webdriver
import os

def crawl_iter(postnum):
    targetUrl =  "http://gall.dcinside.com/board/view/?id=starcraft2_new&no=%s"%postnum
    # targetUrl =  "http://gall.dcinside.com/board/lists/?id=starcraft2_new"

    req = requests.get(targetUrl, headers={"User-Agent": "Requests"}) # User-Agent 헤더가 없으면 리턴이 안됨
    if req.status_code != 200:
        print("bad request")
        return -1
    soup = BeautifulSoup(req.text, "lxml")

    headers =  soup.find("div", attrs={"class":"re_gall_top_1"})

    title = headers.find("dl", attrs={"class":"wt_subject"}).find("dd").text

    timestr = headers.find("div", attrs={"class":"w_top_right"}).find("b").text
    writetime = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')

    writer = headers.find("span", attrs={"class":"user_nick_nm"}).text

    lines = []
    line_tags = soup.find("div", attrs={"class":"s_write"}).find("table").find_all("p") # Image post
    if len(line_tags) != 0:
        for l in line_tags:
            if len(l.text) != 0:
                lines.append(l.text)
    else:
        line_tags = soup.find("div", attrs={"class":"s_write"}).find("table").find_all("td") # No image post
        for l in line_tags:
            if len(l.text) != 0:
                lines.append(l.text)

    app_line_tags = soup.find("div", attrs={"class":"s_write"}).find("table").find("div", attrs={"app_paragraph":"Dc_App_text_0"})
    if app_line_tags != None:
        for l in app_line_tags:
            if "Tag" not in str(type(l)):
                if len(l) != 0:
                    lines.append(l)

    # comments = []
    # comment_tags = soup.find("td", attrs={"class":"reply"})
    # print comment_tags
    # for l in comment_tags:
    #     comments.append(l.text)

    post = dict()
    post["postnum"] = postnum
    post["title"] = title
    post["time"] = writetime
    post['writer'] = writer
    post["lines"] = list(set(lines))
    # post["comments"] = comments
    return post

def crawl_get_firstId():
    targetUrl =  "http://gall.dcinside.com/board/view/?id=starcraft2_new"
    # targetUrl =  "http://gall.dcinside.com/board/lists/?id=starcraft2_new"

    req = requests.get(targetUrl, headers={"User-Agent": "Requests"}) # User-Agent 헤더가 없으면 리턴이 안됨
    if req.status_code != 200:
        print("bad request")
        return -1
    soup = BeautifulSoup(req.text, "lxml")

    int_id = None

    tbs =  soup.find_all("tr", attrs={"class":"tb"})
    for tb in tbs:
        id = tb.find("td", attrs={"class":"t_notice"}).text
        try:
            int_id = int(id)
        except:
            continue
        break

    return int_id

def crawl(init, start=datetime.datetime.now()):
    endtime = datetime.datetime.now() - datetime.timedelta(days=1000)

    endtime = "%s-%s-%s %s:00:00"%(endtime.year, endtime.month, endtime.day, endtime.hour)
    endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')

    now = start
    now_pivot = datetime.datetime.strptime("%s-%s-%s 14:00:00"%(now.year, now.month, now.day),
                                           '%Y-%m-%d %H:%M:%S')
    pivot = now_pivot - datetime.timedelta(days=1)
    posts = []
    init = crawl_get_firstId()

    while(True):
        try_count = 0
        try:
            print(init)
            p = crawl_iter(init)
        except Exception, e:
            print("pass %s"%init, e)
            if try_count == 5:
                print("pass %s"%init, e)
                break
            try_count += 1
            init -= 1
            continue

        if p == -1:
            time.sleep(1)
            continue

        posts.append(p)
        init -= 1

        if p['time'] < pivot: # post 의 시간이 기준 시간 이전
            filename = "crawled/%s.txt"%(str(pivot).split()[0])
            breakbool = False
            if os.path.exists(filename):

                breakbool = True

            fw = open(filename, "w") # 파일이름 : 날짜
            fw.write("\t".join(["postnum", "title", "time", "writer", "lines"]) + "\n")
            for post in posts:
                writestr = "\t".join([str(post["postnum"]), post["title"],
                str(post["time"]),
                post['writer'],
                "@@@".join(post["lines"])]) + "\n"
                fw.write(writestr.encode("UTF-8"))
            fw.close()
            print filename, len(posts), "\t", "Current Time : ", datetime.datetime.now()

            if breakbool:
                print("%s , All End!"%filename)
                break

            posts = []
            pivot = pivot - datetime.timedelta(days=1)

        if p['time'] < endtime:
            break

    return posts

if __name__ == '__main__':
    # crawl_iter(1086705)
    start = datetime.datetime.strptime("%s-%s-%s 14:00:00"%(2017, 8, 2),
                                           '%Y-%m-%d %H:%M:%S')
    # crawl(1112404, start=start)
    crawl_get_firstId()