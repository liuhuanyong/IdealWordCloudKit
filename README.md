# 项目由来
最近接到一个对给定文本自动生成词云的任务,大致需求就是对给定文本进行关键词和高频词统计并根据指定图片形状来生成字符云.这个任务看起来很简单,但也折腾了许久.
关于字符云,目前打开百度,可以看到很多自动生成词云的网站,如wordart等,但这些网站大多都是收费,而且对与免费版本中用户可分析的文本字数是受限的,不支持关键词的可视化,此外在用户交互上还是比较费事, 在完成的这个任务的过程中,使尝试过可以通过用户上传图片并进行字符云形状生成的易词云,但由于字符限制,作罢,因此,打算写脚本进行处理.
在处理之前进行调研,主要有两种词云的生成方式,一种是使用echarts中的wordcloud类型进行生成,大致原理就是使用echarts.js和echarts-wordcloud.min.js这两个文件,使用base64对用户需要设定的图片进行转码,最终构造data字段的数据样式进行填充,从而生成html样式,但在尝试的过程中发现有两个问题:一是对背景图片的要求比较高,试了5张矢量图,只成功了2张,二在显示上比例等的设定不易控制,会出现图形无法展示的情况.
另一种使用python脚本,python脚本中通过调用wordcloud这个可视化组件,可以完成此类任务.该组件操作起来比较简单,对于图片的适用性也较强,也是本项目所采取的方式.
本项目面向本地文件, 在线网页, 程序输入的字符云自动生成组件,支持用户自定义图片字符形状, 生成给定网页,文本的高频词和关键词词云.


# 项目主要功能

本项目支持三种类型的高频词和关键词可视化接口,关键词采用通用的tfidf算法提取而成.
1) show_wordcloud_online, 根据用户输入指定网址,通过采集该网址文本进行处理


        '''根据用户输入载入本地文本进行处理'''
        def show_wordcloud_online(self, url, picturefile, words_num, save_name):
            content = self.get_webcontent(url)
            self.show_main(content, picturefile, words_num, save_name)
            return


2) show_wordcloud_input, 根据用户输入文本字符串进行处理



        '''根据用户输入文本进行处理'''
        def show_wordcloud_input(self, content, picturefile, words_num, save_name):
            self.show_main(content, picturefile, words_num, save_name)
            return


2) show_wordcloud_offline, 根据用户输入载入本地文本进行处理, 用户将所需处理文本文件放入text文件夹中,指定文件名称进行处理



        '''根据用户输入url进行处理'''
        def show_wordcloud_offline(self, textfile, picturefile, words_num, save_name):
            content = self.read_local_file(textfile)
            self.show_main(content, picturefile, words_num, save_name)
            return


# 运行方式

输入用户给定参数:
1) textfile: 放于text文件夹中, 为用户需要分析的文本
2) picturefile: 放于background文件夹中, 为用户给定的图片源文件
3) url: 用户需要进行分析网页文本的url
4) content: 用户需要分析的文本字符串
5) save_name: 用户对当前分析目标的命名
6) word_num: 用户希望展示的词数

输出: 在output文件夹下会生成以save_name开头的高频词云图和关键词云图


'''

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


'''

# 效果展示:
1) 用户本地文件
源文件:text/mao.txt
效果:
高频词
![image](https://github.com/liuhuanyong/IdealWordCloudKit/blob/master/image/mao-topwords.jpg)
关键词
![image](https://github.com/liuhuanyong/IdealWordCloudKit/blob/master/image/mao-keywords.jpg)


2) 用户指定网页url
原url:"https://news.sina.com.cn/o/2019-01-26/doc-ihrfqzka1140567.shtml"
效果:
高频词
![image](https://github.com/liuhuanyong/IdealWordCloudKit/blob/master/image/huawei-topwords.jpg)
关键词
![image](https://github.com/liuhuanyong/IdealWordCloudKit/blob/master/image/huawei-keywords.jpg)

2) 用户输入文本
原文本:
'''
江西之美
豫章故郡，洪都新府,星分翼轸，地接衡庐。襟三江而带五湖，控蛮荆而引瓯越。物华天宝，龙光射牛斗之墟；人杰地灵，徐孺下陈蕃之榻。雄州雾列，俊采星驰……。这是唐代著名诗人王勃《藤王阁序》中介绍江西首府“南昌”的诗，江西的情况从这儿可以略知一二，南昌还有世界动感都会、文明花园城市之称，更是中国人民解放军的诞生地，有英雄城之称。
江西，简称赣，是典型的江南鱼米之乡。因公元733年唐玄宗设江南西道而得省名。是人杰地灵、钟灵毓秀、物华天宝之处。江西是革命老区，江西人民为中国革命做出了卓著贡献，毛主席等老一辈无产阶级革命家创建的第一个革命根据地“井冈山”就在江西，经过解放后改革开放几十年的发展，江西成为中国经济比较发达的内陆对外开放省份。江西东邻浙江、福建，南嵌广东，西靠湖南，北毗湖北、安徽而共接长江，为长江三角洲、珠江三角洲和闽南三角洲经济发达地区的共同腹地，区位极为优越。省境内除北部较为平坦外，东西南部三面环山，中部丘陵起伏，成为一个整体向鄱阳湖倾斜而往北开口巨大盆地。全境有大小河流2400余条，赣江、抚河、信江、修河和饶河为江西五大河流，江西的风景形胜也是全国独特，李白的《望庐山瀑布》一诗描写了庐山的壮美，其实江西的三清山、龙虎山等与庐山是难分伯仲的，三清山是世界文化自然遗产，您只要上一回三清山，就感到它不亚于黄山，真是仙人之居所。不亏为世界第一的花岗岩山……大美的江西，人间的天堂
'''
效果:
高频词
![image](https://github.com/liuhuanyong/IdealWordCloudKit/blob/master/image/jiangxi-topwords.jpg)
关键词
![image](https://github.com/liuhuanyong/IdealWordCloudKit/blob/master/image/jiangxi-keywords.jpg)


# 总结
1) 本项目针对目前开源软件中缺少根据用户自定义图像进行词频与关键词分析形成词云的现状,完成了一个基于python与wordcloud组件的可视化项目.
2) 本项目支持用户本地文件,用户输入字符串,用户输入文本网址三种模式的词云生成接口
3) 本项目支持用户对本地文件进行高频词展示和关键词展示,使用了常用的TFIDF算法,支持用户对展示的词数进行设定
4) 使用Wordcloud和matplotlib的方式存在一定不足,如得到的图像清晰度不高等


如有自然语言处理、知识图谱、事理图谱、社会计算、语言资源建设等问题或合作，可联系我：
1、我的github项目介绍：https://liuhuanyong.github.io
2、我的csdn博客：https://blog.csdn.net/lhy2014
3、刘焕勇，中国科学院软件研究所，lhy_in_blcu@126.com