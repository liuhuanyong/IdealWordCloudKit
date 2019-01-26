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
    textfile = 'china.txt'
    picturefile = 'china.jpg'
    url = 'https://www.hao123.com/mid?from=shoubai&key=9433923127627861739&type=rec'
    content = '''
        史蒂夫·乔布斯 [1]  （Steve Jobs，1955年2月24日—2011年10月5日 [2]  ），出生于美国加利福尼亚州旧金山，美国发明家、企业家、美国苹果公司联合创办人。 [3]
        1976年4月1日，乔布斯签署了一份合同，决定成立一家电脑公司。 [1]  1977年4月，乔布斯在美国第一次计算机展览会展示了苹果Ⅱ号样机。1997年苹果推出iMac，创新的外壳颜色透明设计使得产品大卖，并让苹果度过财政危机。 [4]  2011年8月24日，史蒂夫·乔布斯向苹果董事会提交辞职申请。 [5]
        乔布斯被认为是计算机业界与娱乐业界的标志性人物，他经历了苹果公司几十年的起落与兴衰，先后领导和推出了麦金塔计算机（Macintosh）、iMac、iPod、iPhone、iPad等风靡全球的电子产品，深刻地改变了现代通讯、娱乐、生活方式。乔布斯同时也是前Pixar动画公司的董事长及行政总裁。 [6]
        2011年10月5日，史蒂夫·乔布斯因患胰腺神经内分泌肿瘤 [7]  病逝，享年56岁。
    '''
    save_name = 'china'
    words_num = 50
    handler = CreateWordCloud()
    handler.show_wordcloud_input(content, picturefile, words_num, save_name)
    handler.show_wordcloud_online(url, picturefile, words_num, save_name)
    handler.show_wordcloud_offline(textfile, picturefile, words_num, save_name)

if __name__ == '__main__':
    test()
