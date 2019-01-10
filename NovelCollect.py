#!/user/bin/env python3
# -*- coding: utf-8 -*-

"""
requests:htmlかっぱらうのに使う.
os:フォルダを作るのに使う.
subprocess:コマンド実行に使う.
time:requestsとかで一気に送るとDos攻撃みたいになるからちょっと時間置くために使う.
Beautifulsoup:タグの切り出しに使う.
re:ディレクトリ（フォルダ）内のファイルの数を調べるのに使う.
sys: すでに存在するディレクトリがあり且つ更新がない場合プログラムを終了させるもの.

subprocess, Beautifulsoupは pip install xxxxでインストールできる.
"""
import requests
import os
import shutil
import time
import re
import sys
from bs4 import BeautifulSoup


# ダウンロードしたい小説のNコードを入力させてそれをURLにぶっこむ.
# NコードはなろうのサイトのDLしたい小説のとこに行ってhttps://ncode.syosetu.com/xxxxx/のxxxxxの部分.
ncode = input("ダウンロードしたい小説のNコードを入力してください: ")
URL = "https://ncode.syosetu.com" + "/" + ncode + "/"


# requestsを使ってhtmlを引っ張る.encodingをutf-8にしないと日本語読み込みに失敗するから必要.
# Beautifulsoupつかってhtmlを切り出す.
# get_html.textでタグの中にあるtext情報だけ抜き取る.
get_html = requests.get(URL)
get_html.encoding = 'utf-8'
soup = BeautifulSoup(get_html.text, 'html.parser')


# getstoryNum: 小説のタイトルと指定された小説の１話ずつのタイトルの数を取ってくる.
# サブタイトル取るときはfind_allで取得しないと一つしか取ってこれないので注意.
getstoryNum = []
getstoryNum = soup.find_all("dl", attrs={"class": "novel_sublist2"})
novelTitle = soup.find("p", attrs={"class": "novel_title"})


# os使ってディレクトリ（フォルダ）の作成.novelTitleはtextを指定しないとタグとかついたまんまなのでエラーが出る.
# 例外でFileExistsError(すでにフォルダが存在するときのエラー)が出た時には内部の処理をする.
# dir: os.getcwdで現在のこのファイル(NovelCollect)の絶対パスを取得する.
# files: os,listdir(xxx)でxxxディレクトリ内のファイルをlistにまとめる.
# index: re.search(拡張子, file)でfile内の指定した拡張子を持つファイルを調べる.
# そしてindexが見つかれば,countを1ずつ増やして,その数をcountsに保持する.
# count: 既存のディレクトリがある場合にそのディレクトリ内にあるファイルの数を調べるためのもの.
# counts: countは後々にURLALLに使うので,ファイルの数を保持するもの.
count = 0
counts = 0
try:
    os.mkdir(novelTitle.text)
except FileExistsError:
    dir = os.getcwd()
    files = os.listdir(novelTitle.text)
    for file in files:
        index = re.search('.txt', file)
        if index:
            count += 1
            counts = count


# 各話のURLの取得.iはint型なのでstr型に変更してURLに連結させる.
# iは0から始まっているのでi+1にしてあげないと0話を取得してしまうことになるので注意.
# また,最新話も取得できなくなるので注意.
# URLALL.appendとは,指定された配列に要素を付け加えていくという役割を果たす.
# 引数の中はstr型なのでしっかりとstr型にして置く必要あり.
URLALL = []
if count > 0 and len(getstoryNum) != count:
    for update in range(len(getstoryNum) - count):
        URLALL.append(URL + str(count + 1) + '/')
        count += 1
    print("Find Update...")
elif len(getstoryNum) == count:
    print("No Exists Update")
    sys.exit()
else:
    for i in range(len(getstoryNum)):
        URLALL.append(URL + str(i + 1) + "/")
    print("NowDownLoading" + " " + novelTitle.text)


# 本文と各話のタイトルを格納する配列を宣言する.
# URLALLの数だけfor文を回して,各話requestsでhtmlの情報を取ってくる.
# encodingも忘れずに指定.じゃないとタイトルが文字化け祭りになる.
# print文の最初にある'\r'は復帰と言って,実行したらポインタを行頭に戻すという作業をしてくれる.
# だから,for文が終わるまでprintの内容を改行でずっと表示するのではなくて１行で表示してくれる.
# ちなみにpython3ではprintの後には特に何も書かずにいると自動的に改行処理が入る.
# だからprint文の最後に[end=""]を入れてその処理をなくしている.
# これがないと\r使ってるのにずっと改行されるので注意.
honbuns = []
titles = []
for j in range(len(URLALL)):
    get_html_honbun = requests.get(URLALL[j])
    get_html_honbun.encoding = 'utf-8'
    soup2 = BeautifulSoup(get_html_honbun.text, 'html.parser')
    honbuns_E = soup2.find("div", attrs={"id": "novel_honbun"})
    title = soup2.find("p", attrs={"class": "novel_subtitle"})
    honbuns.append(honbuns_E)
    titles.append(title)
    time.sleep(0.05)
    print("\r{0}/{1}".format(j + 1, len(URLALL)), end="")
print()


# ここでは出来た本文の配列をtxt形式で１つずつ書き出すという作業をする.
# openのところの後ろの'w'はwriteを意味する書き出しのパーミションを設定している.
# ちなみにopen使ったら最後はcloseしておく.
# write使う時には中の引数を文字列にしないといけないのでstrに変換している.
saveName = ""
if count > 0:
    for updateName in range(len(getstoryNum) - counts):
        saveName = str(counts + updateName + 1) + "話 " + \
            titles[updateName].text + '.txt'
        for c in '\/><|":?*':
            saveName = saveName.replace(c, '')

        f = open(saveName, 'w')
        f.write(str(honbuns[updateName].text))
        f.close()
        shutil.move(saveName, novelTitle.text)
else:
    for k in range(len(honbuns)):
        saveName = str(k + 1) + "話 " + titles[k].text + '.txt'
        for c in '\/><|":?*':
            saveName = saveName.replace(c, '')
        f = open(saveName, 'w')
        f.write(str(honbuns[k].text))
        f.close()
        shutil.move(saveName, novelTitle.text)

"""
#subprocessを使ったコマンドの実行をしている.
#いつもコマンドを使う時に入れている空白もしっかり入れること.
cmd = 'mv ' + '*txt ' + novelTitle.text
subprocess.call(cmd, shell = True)
"""


# すでにDLしているものがあった場合に検索をかけて更新されていたら更新するというのを付け加える予定.
# 多分FileExistsErrorのところに処理を付け加えそう.
