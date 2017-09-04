#-*- coding:utf-8 -*-

from konlpy.tag import Twitter
from collections import Counter
import pytagcloud
import os
import datetime
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc, rcParams
from matplotlib.font_manager import FontProperties

# rc("HYGothic-Medium")

# lu = FontProperties('HYGothic-Medium')
# font = FontProperties(fname="C:/Windows/Fonts/MT.ttf")
# font = FontProperties(fname="C:/Windows/Fonts/Arial.ttf")
font = FontProperties("KorUM")

rcParams['font.family'] = font.get_name()

# rc("font", family="MBatang")
# rc('font', family='HYPost')

def analysis(posts, foldername):
    if not os.path.isdir(foldername):
        os.mkdir(foldername)

    # tagcloud(posts, foldername)
    regen_statistics(posts, foldername)
    # writer_statistics(posts, foldername)

    # post_chart(posts, foldername) # regen 으로 대체
    # daily_chart(posts, foldername)

def writer_statistics(posts, foldername):
    writers = []
    for p in posts:
        writers.append(p['writer'].strip())
    count = Counter(writers)


    writers = []
    counts = []

    fw = open("%s/writers.tsv"%(foldername), "w")
    for v,c in count.most_common(50):
        fw.write("%s\t%s\n"%(v,c))
        writers.append(v)
        counts.append(c)
    fw.close()

    writers = writers[1:] #except ㅇㅇ
    writers = writers[::-1]
    writers = [v.decode("utf-8") for v in writers]

    counts = counts[1:] #except ㅇㅇ
    counts = counts[::-1]

    plt.figure(figsize=(9,15))

    barlist = plt.barh(range(len(writers)), counts,
             align='center',
             alpha=0.4,
             color='green')

    barlist[-1].set_color("yellow")

    for rect in barlist:
        width = rect.get_width()
        plt.text(1+width, rect.get_y(),
                '%d' % int(width),
                ha='center', va='bottom')
    # plt.yticks(range(len(writers)), writers, fontproperties = font)
    plt.yticks(range(len(writers)), writers)
    # plt.yticklabels(people)
    # plt.invert_yaxis()  # labels read top-to-bottom
    plt.xlabel('Performance')
    plt.title("Weekly SC2Gall Writer Ranking")

    plt.savefig("%s/writers.png"%foldername)

def regen_statistics(posts, foldername):
    date_count = dict()
    for p in posts:
        dtime = p['time']
        date = "%s.%s"%(dtime.month, dtime.day)

        if date not in date_count:
            date_count[date] = 0

        date_count[date] += 1

    dates = sorted(date_count.keys())
    counts = [date_count[d] for d in dates]

    dates.append("Average")
    counts.append(round(sum(counts)/float(len(counts)),1))

    plt.figure(figsize=(9,9))
    # plt.xticks(range(len(dates)), dates, rotation=90, size=10)
    plt.xticks(range(len(dates)), dates, size=10)
    plt.title(u"Weekly SC2Gall REGEN Statistics [%s ~ %s]"%(str(dates[0]), str(dates[-2])))

    bar_width = 0.3
    opacity = 0.4

    barlist = plt.bar(range(len(dates)), counts, bar_width,
                 alpha=opacity,
                 color='b')

    barlist[-1].set_color('r')

    for rect in barlist:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., 1+height,
                '%d' % int(height),
                ha='center', va='bottom')

    plt.savefig("%s/regen.png"%foldername)


def post_chart(posts, foldername):
    starttime = posts[-1]['time']
    starttime = "%s-%s-%s %s:00:00"%(starttime.year, starttime.month, starttime.day, starttime.hour)
    starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
    print starttime
    endtime = posts[0]['time']
    endtime = "%s-%s-%s %s:00:00"%(endtime.year, endtime.month, endtime.day, endtime.hour)
    endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    print endtime

    pivot = starttime
    countdict = dict()
    for v in reversed(posts):
        if v['time'] > (pivot + datetime.timedelta(hours=1)):
            pivot = pivot + datetime.timedelta(hours=1)
        if str(pivot) not in countdict:
            countdict[str(pivot)] = 0
        countdict[str(pivot)] += 1

    dates = []
    counts = []
    for k in sorted(countdict.keys()):
        if "00:00:00" in k:
            dates.append(k.split()[0])
        else:
            dates.append("")
        counts.append(countdict[k])
    dates = dates[1:-1]
    counts = counts[1:-1] # remove first and last bias
    plt.figure(figsize=(9,9))
    plt.xticks(range(len(dates)), dates, rotation=90, size=10)
    plt.title(u"Thermal power by time [%s ~ %s]"%(str(starttime), str(endtime)))
    plt.plot(counts)
    plt.savefig("%s/thermal power.png"%foldername)

def daily_chart(posts, foldername):
    starttime = posts[-1]['time']
    starttime = "%s-%s-%s %s:00:00"%(starttime.year, starttime.month, starttime.day, starttime.hour)
    starttime = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S')
    print starttime
    endtime = posts[0]['time']
    endtime = "%s-%s-%s %s:00:00"%(endtime.year, endtime.month, endtime.day, endtime.hour)
    endtime = datetime.datetime.strptime(endtime, '%Y-%m-%d %H:%M:%S')
    print endtime

    pivot = starttime + datetime.timedelta(hours=1)
    linesdict = dict()
    for v in reversed(posts):
        if v['time'] > pivot:
            pivot = pivot + datetime.timedelta(days=1)
        if str(pivot) not in linesdict:
            linesdict[str(pivot)] = []

        linesdict[str(pivot)].append(v['title'].strip())
        for l in v['lines']:
            linesdict[str(pivot)].append(l.strip())

    for k in sorted(linesdict.keys()):
        oneday_onestr = "\n".join(linesdict[k])
        konlp = Twitter()
        nouns = konlp.nouns(oneday_onestr.decode("utf-8"))

        count = Counter(nouns)
        twochracter = []
        for v,c in count.most_common(200):
            if len(v) > 1:
                twochracter.append((v,c))
        commons = twochracter[:30]
        print k
        for v,c in commons:
            print v,c

        taglist = pytagcloud.make_tags(commons, maxsize=100)
        # fonts = ['NanumMyeongjo', 'NanumMyeongjoBold', 'NanumGothic', 'NanumGothicBold']
        fonts = ['NanumMyeongjoBold']

        for f in fonts:
            for b in [True,False]:
                pytagcloud.create_tag_image(taglist, "%s/%s_%s_%s.png"%(foldername,k.split()[0],f,b), fontname=f, size=(900,600), rectangular=b)

def tagcloud(posts, foldername):
    all_strs = []
    for p in posts:
        all_strs.append(p['title'].strip())
        for l in p['lines']:
            all_strs.append(l.strip())
    print len(all_strs)
    onestr = "\n".join(all_strs).decode("utf-8")
    # print(onestr)

    konlp = Twitter()
    nouns = konlp.nouns(onestr)

    count = Counter(nouns)

    twochracter = []
    for v,c in count.most_common(200):
        if len(v) > 1:
            twochracter.append((v,c))
    commons = twochracter[:50]

    for v,c in commons:
        print v,c

    taglist = pytagcloud.make_tags(commons, maxsize=100)
    print taglist

    fonts = ['NanumMyeongjo', 'NanumMyeongjoBold', 'NanumGothic', 'NanumGothicBold']
    fonts = ['NanumMyeongjoBold']

    for f in fonts:
        for b in [True,False]:
            pytagcloud.create_tag_image(taglist, "%s/tagcloud_%s_%s.png"%(foldername,f,b), fontname=f, size=(900,600), rectangular=b)
