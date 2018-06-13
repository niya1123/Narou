#! user/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from lxml.html import fromstring, tostring
import subprocess, time

class narouDownloader():

    def __init__(self,ncode):
        """
        コンストラクタ.
        """
        self.encoding = 'utf-8'  #文字コード
        self.url = 'https://ncode.syosetu.com/'+ncode # 小説のURL
        self.novelTitle = '' # 小説のタイトル.CreateFolderで中身を指定
        with urlopen(self.url) as response:
            #htmlデータ
            self.doc = fromstring(response.read())
        response.close() 

    def Parser(self,ncode):
        """
        指定URLからhtmlをパースして,欲しい情報を抽出.今回では,小説の各話の題名とその本文を取ってきている.
        """
        with urlopen(self.url) as response:
            #変数の名前はhtml内の名前に準拠
            novel_sublist2 = self.doc.xpath('//dd/a')
            for i in range(len(novel_sublist2)):
                count = i + 1
                novel_subtitle = "第" + str(count) + "話" + novel_sublist2[i].text
                novel_url = self.url+'/' + str(count)
                with urlopen(novel_url) as r:
                    doc2 = fromstring(r.read())
                    honbun_data = doc2.get_element_by_id('novel_honbun')
                    honbun = tostring(honbun_data,method='text',encoding=self.encoding)
                    with open(novel_subtitle + '.txt','wb') as f:
                        f.write(honbun)
                    f.close()    
                r.close()
        response.close()

    def CreateFolder(self):
        """
        小説のタイトルを取得して,フォルダを作る.Parseメソッドで作られた各話をそのフォルダに移動させる.
        """
        with urlopen(self.url) as response:
            pTag = self.doc.xpath('//p')
        response.close()
        self.novelTitle = pTag[10].text

        try:
            subprocess.call('mkdir -p ' + self.novelTitle, shell=True)
            subprocess.call('mv *txt ' + self.novelTitle, shell=True)
        except FileExistsError:
            pass
    
    def showinfo(self):
        """
        ダウンロードの終了を示す.timeはなくてもいい.
        """
        print(self.novelTitle + " のダウンロードが終了しました.")
        time.sleep(0.3)


if __name__ == '__main__':
    ncode = input("ダウンロードしたい小説のNコードを入力してください: ")
    dl = narouDownloader(ncode)
    doTime = time.time()
    dl.Parser(ncode)
    dl.CreateFolder()
    dl.showinfo()