#!/usr/bin/env python3
# coding: utf-8
# File: plot_main.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 19-1-26

import os
import matplotlib.pyplot as plt
from keywords_tfidf import *
from collections import Counter
import jieba.posseg as pseg
import urllib.request
from wordcloud import WordCloud, ImageColorGenerator
from newspaper import Article


class CreateWordCloud:
    def __init__(self):
        cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.outpath = os.path.join(cur, 'output')
        self.textdir = os.path.join(cur, 'text')
        self.background = os.path.join(cur, 'background')
        self.fontpath = os.path.join(cur, 'data/simhei.ttf')
        self.outpath = os.path.join(cur, 'output')
        self.pos_filters = ['n', 'v', 'a']
        self.limit_words = 100
        self.Keyworder =  TFIDF()
        return

    '''获取搜索页'''
    def get_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 Safari/600.5.17"}
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8')
        return html

    '''读取本地文件进行处理'''
    def read_local_file(self, textfile):
        textpath = os.path.join(self.textdir, textfile)
        content = open(textpath).read()
        return content

    '''统计词频'''
    def extract_words(self, content):
        words = []
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            words += [w.word for w in pseg.cut(line) if w.flag[0] in self.pos_filters and len(w.word) > 1]
        word_dict = {i[0]: i[1] for i in Counter(words).most_common()}
        return word_dict

    '''抽取关键词'''
    def extract_keywords(self, content, words_num=20):
        keywords_dict = {}
        keywords = self.Keyworder.extract_keywords(content, words_num)
        for key in keywords:
            word = key[0]
            value = int(key[1]*1000)
            keywords_dict[word] = value
        return keywords_dict

    '''创建关键词云图'''
    def show_cloud(self, word_dict, max_words, picturefile, save_name):
        self.backimage = os.path.join(self.background, picturefile)
        saveimage = os.path.join(self.outpath, save_name + '.jpg')
        backgroud_Image = plt.imread(self.backimage)
        cloud = WordCloud(font_path=self.fontpath,
                          background_color='white',
                          width=800,
                          height=600,
                          max_words= max_words,
                          max_font_size=500,
                          mask=backgroud_Image
                          )

        word_cloud = cloud.generate_from_frequencies(word_dict)
        img_colors = ImageColorGenerator(backgroud_Image)
        word_cloud.recolor(color_func=img_colors)
        plt.imshow(word_cloud)
        plt.axis('off')
        plt.savefig(saveimage)
        # plt.show()
        # plt.close()


    '''展示关键词云图'''
    def show_keywords(self, content, picturefile, words_num=20, save_name = 'test'):
        keywords_text = self.extract_keywords(content, words_num)
        self.show_cloud(keywords_text, words_num, picturefile, save_name)
        return

    '''展示高频词云图'''
    def show_topwords(self, content, picturefile, words_num=50, save_name = 'test'):
        topwords_text = self.extract_words(content)
        self.show_cloud(topwords_text, words_num, picturefile, save_name)
        return

    '''在线模式抓取新闻进行既定形状可视化'''
    def get_webcontent(self, url):
        news = Article(url, language='zh')
        news.download()
        news.parse()
        content = news.text
        return content

    '''根据用户输入载入本地文本进行处理'''
    def show_wordcloud_online(self, url, picturefile, words_num, save_name):
        content = self.get_webcontent(url)
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''根据用户输入文本进行处理'''
    def show_wordcloud_input(self, content, picturefile, words_num, save_name):
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''根据用户输入url进行处理'''
    def show_wordcloud_offline(self, textfile, picturefile, words_num, save_name):
        content = self.read_local_file(textfile)
        self.show_main(content, picturefile, words_num, save_name)
        return

    '''分别执行绘制关键词和高频词'''
    def show_main(self, content, picturefile, words_num, save_name):
        name = save_name + '-topwords'
        print('正在生成该文本的高频词云图.....')
        self.show_topwords(content, picturefile, words_num, name)
        print('已完成该文本的高频词云图.....')
        print('正在生成该文本的关键词云图.....')
        name = save_name + '-keywords'
        self.show_keywords(content, picturefile, words_num, name)
        print('已完成该文本的关键词云图.....')

def test():
    textfile = 'mao.txt'
    picturefile = 'jiangxi.jpeg'
    url = 'https://news.sina.com.cn/o/2019-01-26/doc-ihrfqzka1140567.shtml'
    content = '''
 江西之美
豫章故郡，洪都新府,星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰……。这是唐代著名诗人王勃《藤王阁序》中介绍江西首府“南昌”的诗，江西的情况从这儿可以略知一二，南昌还有世界动感都会、文明花园城市之称，更是中国人民解放军的诞生地，有英雄城之称。
江西，简称赣，是典型的江南鱼米之乡。因公元733年唐玄宗设江南西道而得省名。是人杰地灵、钟灵毓秀、物华天宝之处。江西是革命老区，江西人民为中国革命做出了卓著贡献，毛主席等老一辈无产阶级革命家创建的第一个革命根据地“井冈山”就在江西，经过解放后改革开放几十年的发展，江西成为中国经济比较发达的内陆对外开放省份。江西东邻浙江、福建，南嵌广东，西靠湖南，北毗湖北、安徽而共接长江，为长江三角洲、珠江三角洲和闽南三角洲经济发达地区的共同腹地，区位极为优越。省境内除北部较为平坦外，东西南部三面环山，中部丘陵起伏，成为一个整体向鄱阳湖倾斜而往北开口巨大盆地。全境有大小河流2400余条，赣江、抚河、信江、修河和饶河为江西五大河流，江西的风景形胜也是全国独特，李白的《望庐山瀑布》一诗描写了庐山的壮美，其实江西的三清山、龙虎山等与庐山是难分伯仲的，三清山是世界文化自然遗产，您只要上一回三清山，就感到它不亚于黄山，真是仙人之居所。不亏为世界第一的花岗岩山……大美的江西，人间的天堂
    '''
    save_name = 'jiangxi'
    words_num = 50
    handler = CreateWordCloud()
    handler.show_wordcloud_input(content, picturefile, words_num, save_name)
    # handler.show_wordcloud_online(url, picturefile, words_num, save_name)
    # handler.show_wordcloud_offline(textfile, picturefile, words_num, save_name)

if __name__ == '__main__':
    test()
