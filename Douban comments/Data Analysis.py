import warnings
warnings.filterwarnings("ignore")
import jieba # 分词包
import pandas as pd
import codecs #codecs提供的open方法来指定打开的文件的语言编码，它会在读取的时候自动转换为内部unicode
import csv
import re
import numpy # 计算包
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (15.0,15.0)
from wordcloud import WordCloud, ImageColorGenerator # 词云包
from imageio import imread

with codecs.open(r'./comment_content.cvs', 'r', 'utf-8') as csvfile:
    content = ''
    reader = csv.reader(csvfile)
    i = 0
    for file in reader:
        if(i == 0 or i == 1):
            pass
        else:
            content = content + file[1]
        i += 1
    # 去除所有评论里面多余的字符
    content = re.sub('[… “ ” ）：《 》？！（ 、,，。. \r\n]', '', content)
    # 切词，用jieba库
    segment = jieba.lcut(content)

    # 去停用词（文本去噪）
    words_df = pd.DataFrame({'segment': segment})
    stopwords = pd.read_csv(r"./豆瓣影评/stopwords.txt", index_col=False,
                            quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]

    # 统计词频、降序排列
    words_stat = words_df.groupby('segment').agg(计数=pd.NamedAgg(
        column='segment', aggfunc='size')).reset_index().sort_values(by='计数', ascending=False)

     # 做词云
    bimg = imread(r'./豆瓣影评/hhh.jpg')
    matplotlib.rcParams['figure.figsize'] = (10.0,6.0)
    #设置中文字体 背景颜色等
    wordcloud = WordCloud(font_path='C:/Windows/Fonts/simfang.ttf',mask=bimg,background_color='white',max_font_size=80) 
    #字典推导式
    word_frequence  = {x[0]:x[1] for x in words_stat.head(1000).values} #取词频最高的前1000个词 (词，词频)->{词：词频}
    wordcloud = wordcloud.fit_words(word_frequence)
    bimgColors=ImageColorGenerator(bimg)
    result = wordcloud.recolor(color_func=bimgColors)
    plt.axis("off")
    plt.imshow(result)
    plt.show()
    result.to_file(r'./豆瓣影评/词云.jpg')
