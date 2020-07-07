'''
requests + xpath爬取豆瓣《隐秘的角落》评价
'''
import requests
import pandas as pd
from lxml import etree

# 爬取页面url
douban_url = 'https://movie.douban.com/subject/33404425/comments?status=P'
# 添加头部
headers = {
    'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
}


def reponse_data(url, headers):
    # requests发送请求
    get_reponse = requests.get(url, headers=headers)
    # 将返回的数据转换为文本
    get_data = get_reponse.text
    # 解析页面
    tree = etree.HTML(get_data)
    return tree


# 第一页
first_page = reponse_data(douban_url, headers)

'''
用户的xpath为： '/html/body/div[3]/div[1]/div/div[1]/div[4]/div/div[2]/h3/span[2]/a'
评论内容xpath为：'/html/body/div[3]/div[1]/div/div[1]/div[4]/div/div[2]/p/span'
看过的用户xpath为：'/html/body/div[3]/div[1]/div/div[1]/div[1]/ul/li[1]/span'
'''
# 看过电影的人数
comment_counts = first_page.xpath(
    '/html/body/div[3]/div[1]/div/div[1]/div[1]/ul/li[1]/span/text()')
comment_counts = int(comment_counts[0].strip("看过()"))
# 总的页面数(每页有20条评论)
pages = int(comment_counts / 20)

'''
理想情况下是全部都能爬到，但是很遗憾测试的时候只能爬到不到280条数据，为了方便起见，只爬了260条数据
'''

for i in range(13):
    # 当前页面url
    page_url = 'https://movie.douban.com/subject/33404425/comments?start={0}&limit=20&sort=new_score&status=P'.format(
        i*20)
    tree = reponse_data(page_url, headers)
    # 获取用户和评论的内容
    commentator = tree.xpath(
        '/html/body/div[3]/div[1]/div/div[1]/div[4]/div/div[2]/h3/span[2]/a/text()')
    comment_content = tree.xpath(
        '/html/body/div[3]/div[1]/div/div[1]/div[4]/div/div[2]/p/span/text()')
    # 解析内容
    content = [' ' for i in range(len(commentator))]
    for i in range(len(commentator)):
        comment_content[i].strip(r'\n')
        comment_content[i].strip(' ')
        content[i] = [commentator[i], comment_content[i]]
    name = ['用户', '评论内容']
    file = pd.DataFrame(columns=name, data=content)
    if i == 0:
        file.to_csv(r'./豆瓣影评/comment_content.cvs',
                    encoding='utf-8', index=False)
    else:
        # 表示追加写
        file.to_csv(r'./豆瓣影评/comment_content.cvs', mode='a+',
                    encoding='utf-8', index=False)
