from urllib.request import urlopen
from lxml.html import fromstring, tostring
import time
import os


class narouDownloader():

    def __init__(self, ncode):
        """
        コンストラクタ.
        """
        self.encoding = 'utf-8'  # 文字コード
        self.url = 'https://ncode.syosetu.com/'+ncode  # 小説のURL
        self.novelTitle = ''  # 小説のタイトル.CreateFolderで中身を指定
        with urlopen(self.url) as response:
            # htmlデータ
            self.doc = fromstring(response.read())

    def Parser(self, ncode):
        """
        指定URLからhtmlをパースして,欲しい情報を抽出.今回では,小説の各話の題名とその本文を取ってきている.
        """
        # 変数の名前はhtml内の名前に準拠
        novel_sublist2 = self.doc.xpath('//dd/a')
        for i, n in enumerate(novel_sublist2):
            count = i + 1
            novel_subtitle = "第" + \
                str(count) + "話" + n.text
            novel_url = self.url+'/' + str(count)
            with urlopen(novel_url) as r:
                doc2 = fromstring(r.read())
                honbun_data = doc2.get_element_by_id('novel_honbun')
                honbun = tostring(
                    honbun_data, method='text', encoding=self.encoding)
                with open(novel_subtitle + '.txt', 'wb') as f:
                    f.write(honbun)
            print("\r{0}/{1}".format(count, len(novel_sublist2)), end="")

    def CreateFolder(self, ncode):
        """
        小説のタイトルを取得して,フォルダを作る.Parseメソッドで作られた各話をそのフォルダに移動させる.
        """
        pTag = self.doc.xpath("//*[@id=\"novel_color\"]/p")
        self.novelTitle = pTag[0].text

        for c in '><|":?* 　':
            self.novelTitle = self.novelTitle.replace(c, '')

        try:
            os.makedirs(self.novelTitle)
        except FileExistsError:
            print(self.novelTitle+"はすでに存在しています")
            print("内容をアップデートします")
            pass

        # 作業ディレクトリを対象の小説のフォルダーに移動
        os.chdir(self.novelTitle)
        self.Parser(ncode)

    def showinfo(self):
        """
        ダウンロードの終了を示す.timeはなくてもいい.
        """
        print()
        print(self.novelTitle + " のダウンロードが終了しました.")


if __name__ == '__main__':
    ncode = input("ダウンロードしたい小説のNコードを入力してください: ")
    dl = narouDownloader(ncode)
    dl.CreateFolder(ncode)
    dl.showinfo()
