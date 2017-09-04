from __future__ import print_function
import analysis
import pickle
import glob
import pandas as pd
import datetime

def main():

    # posts = pickle.load(open("sevenday.pickle"))
    "postnum	title	time	writer	lines"
    print(get_weeks_filename(2017,9,3))

    flist = (glob.glob("crawled/2017-08*"))
    posts = []
    lens = []
    for i in range(len(flist)):
        fr = open(flist[i])
        count = 0
        for l in fr.readlines():
            tokens = l.split("\t")
            if len(tokens) != 5:
                continue
            if tokens[0] == "postnum":
                continue

            post = dict()
            post['postnum'] = tokens[0].strip()
            post['title'] = tokens[1].strip()
            post['time'] = datetime.datetime.strptime(tokens[2].strip(), '%Y-%m-%d %H:%M:%S')
            post['writer'] = tokens[3].strip()
            post['lines'] = tokens[4].split("@@@")
            posts.append(post)
            count += 1

        fr.close()
        lens.append(count)

    analysis.analysis(posts, "tests")

def get_weeks_filename(y,m,d):
    dtime = datetime.datetime.strptime("%s-%s-%s 14:00:00"%(y, m, d),
                                           '%Y-%m-%d %H:%M:%S')
    fnlist = []
    for i in range(7):
        pivot = dtime - datetime.timedelta(days=i)
        fn = str(pivot).split()[0]
        fnlist.append("crawled/%s.txt"%fn)
    return fnlist

if __name__ == '__main__':
    main()
    # get_weeks_filename(2017,9,3)
