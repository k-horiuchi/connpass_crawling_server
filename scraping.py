from bs4 import BeautifulSoup
from time import sleep
import urllib.request as req
import urllib
import json
import sys
import socket
saveHtml = ""
saveJson = "["
for i in range(60):
    sleep(1)
    # ページのURL
    url = "https://connpass.com/explore/?page=" + str(i+1)

    # ページの情報を取得する
    try:
        res = req.urlopen(url)
    except socket.timeout:
        sys.exit()
    except urllib.error.URLError:
        sys.exit()
    except urllib.error.HTTPError:
        sys.exit()
    soup = BeautifulSoup(res , "html.parser")
    event_places = soup.select("#main > div > div > div > p > span.event_place > span")
    event_titles = soup.select("#main > div > div > div > p.event_title > a")
    disclosure_dates = soup.select("#main > div > div > div > span.publishtime")
    convenes = soup.select("#main > div > div > div > span.label_status_event")
    convene_monthes = soup.select("#main > div > div > div > a > p > span.month")
    convene_dates = soup.select("#main > div > div > div > a > p > span.date")
    capacitys = soup.select("#main > div > div > div > p.event_participants")
    for v in range(20): # 1ページに表示されるイベント数ループ

        # 開催状況が開催前でないなら取得しない
        convene = convenes[v]
        convene = convene.string
        if convene != "開催前":
            continue

        # 場所が札幌でないなら取得しない
        event_place = event_places[v]
        event_place = event_place.string
        event_place = event_place.replace(' ', '')
        event_place = event_place.replace('　', '')
        event_place = event_place.replace('\n', '')
        search = event_place.find('札幌')
        if search == -1:
            continue

        # 情報の公開日を取得
        disclosure_date = disclosure_dates[v]
        disclosure_date = disclosure_date.string
        disclosure_date = disclosure_date[-10:]

        # イベントの開催月を取得
        convene_month = convene_monthes[v]
        convene_month = convene_month.string
        convene_month = convene_month.replace('月', '')
        if int(convene_month) < 10:
            convene_month = "0" + str(convene_month)

        # イベントの開催日を取得
        convene_day = convene_dates[v]
        convene_day = convene_day.string

        # イベントの開催日付を取得
        convene_date = convene_month + "/" + convene_day

        # 勉強会の名前を取得
        event_title = event_titles[v]

        # 定員数を取得
        capacity = capacitys[v]
        capacity = capacity.text
        capacity = capacity.replace('\n', '')
        capacity = capacity.replace(' ', '')

        dic = {"題　名：":str(event_title), "開催地：":str(event_place), "開催日：":str(convene_date),"公開日：":str(disclosure_date),"定員数：":str(capacity)}

        print(event_title)
        print(event_place)
        print(capacity)
        print(convene_date)
        print(disclosure_date + "\n")

        # HTMLを保存
        saveHtml += "<div>題　名：" + str(event_title) + "<br>開催地：" + str(event_place) + "<br>開催日：" + str(convene_date) + "<br>公開日：" + str(disclosure_date) + "<br>定員数：" + str(capacity) + "</div><br>"

        # ダブルクォーテーションをエスケープ
        saveJson += json.dumps(dic, indent=2, ensure_ascii=False) + ","

# 保存先ファイル名
savename = "connpass.html"
with open(savename, mode="w") as f:
    f.write(saveHtml)

# 不要なカンマを消す
saveJson = saveJson[:-1] + ']'
# 保存先ファイル名
savename = "connpass.json"
with open(savename, mode="w") as f:
    f.write(saveJson)
